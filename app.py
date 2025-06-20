import os
import sys
import time
from flask import Flask, render_template
from flask_socketio import SocketIO
from playwright.sync_api import sync_playwright, TimeoutError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui!'
socketio = SocketIO(app)

def run_automation_process(user, password, sis_list):
    
    def log(msg):
        print(time.strftime("[%H:%M:%S] "), msg, flush=True) 
        socketio.emit('log', {'data': time.strftime("[%H:%M:%S] ") + msg})
        socketio.sleep(0) # Permite que el mensaje se envíe

    with sync_playwright() as p:
        browser = None # Inicializar browser a None
        try:
            browser = p.chromium.launch(headless=True) # Se recomienda True para servidores
            ctx = browser.new_context()
            page = ctx.new_page()

            LOGIN_URL = "https://ruge.umss.edu.bo/index.php/login_admin"
            BUSCADOR_URL = "https://ruge.umss.edu.bo/reporte_estudiantil/"

            # 1. LOGIN
            log("Abriendo login…")
            page.goto(LOGIN_URL)
            page.fill('input[name="user"]', user)
            page.fill('input[name="pass"]', password)
            page.click('#ingresar')
            try:
                page.wait_for_url("**/menu_admin", timeout=8000)
            except TimeoutError:
                log("❌ Login falló – revisa las credenciales.")
                return # Termina la función si el login falla
            log("✅ Login OK")

            # 2. BUCLE DE PROCESAMIENTO
            page.goto(BUSCADOR_URL)
            for sis in sis_list:
                if not sis: continue # Ignorar lineas vacías
                log(f"▶︎ Buscando SIS {sis}...")
                page.fill('#sis', sis)
                page.press('#sis', 'Enter')
                try:
                    page.wait_for_selector('a:text("Verificacion Fisica")', timeout=7000)
                except TimeoutError:
                    log(f"⚠️  No se encontró resultado para SIS {sis}")
                    continue

                with page.expect_navigation():
                    page.locator('a:text("Verificacion Fisica")').first.click()

                # ACEPTAR TODOS LOS REQUISITOS (Lógica de procesar.py integrada)
                while True:
                    for btn in page.locator('button.aceptar:visible').all():
                        btn.click()
                        page.wait_for_load_state('networkidle')
                    
                    if page.locator('form[action*="aceptado_fisica"]').count():
                        page.evaluate("() => { document.querySelector('form[action*=\"aceptado_fisica\"]').requestSubmit(); }")
                        page.wait_for_load_state('networkidle')
                        break # Salir del while para este SIS

                    if page.locator('button.sw-btn-next:visible').count():
                        page.locator('button.sw-btn-next:visible').first.click()
                        page.wait_for_timeout(400)
                    else:
                        raise RuntimeError("Wizard atascado: No hay botón 'siguiente' ni formulario final.")

                log(f"✔️  Trámite para SIS {sis} procesado.")
                page.goto(BUSCADOR_URL)

            log("🏁 Proceso terminado.")

        except Exception as e:
            log(f"🚨 ERROR INESPERADO: {e}")
        finally:
            if browser:
                browser.close()
            socketio.emit('process_finished') # Avisa al frontend que terminó


# --- Rutas del Servidor Web ---

@app.route('/')
def index():
    """Sirve la página principal (nuestro frontend)."""
    return render_template('index.html')

@socketio.on('start_process')
def handle_start_process(json_data):
    """Recibe la orden de empezar desde el frontend."""
    user = json_data.get('user')
    password = json_data.get('password')
    # Convertir el string de SIS en una lista limpia
    sis_list = [sis.strip() for sis in json_data.get('sis_list', '').split('\n')]
    
    print(f"Recibida petición para usuario: {user} con {len(sis_list)} códigos SIS.")
    
    # Inicia el proceso de automatización en un hilo separado
    socketio.start_background_task(run_automation_process, user, password, sis_list)

if __name__ == '__main__':
    print("Servidor iniciado en http://127.0.0.1:5000")
    # debug=True permite recargar el servidor automáticamente al guardar cambios
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)