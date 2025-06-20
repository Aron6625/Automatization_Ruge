from playwright.sync_api import sync_playwright, TimeoutError
import csv, time, os, sys
from procesar import procesar_tramite

USER      = os.getenv("RUGE_USER")      or "c.calderon"
PASSWORD  = os.getenv("RUGE_PASS")      or "ma7ia5cald3r0n"
HEADLESS  = False                        # False  navegador
SIS_LISTA = ["202505535", "202505536"] 

LOGIN_URL     = "https://ruge.umss.edu.bo/index.php/login_admin"
BUSCADOR_URL  = "https://ruge.umss.edu.bo/reporte_estudiantil/"

def log(msg): print(time.strftime("[%H:%M:%S] "), msg, flush=True)

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        ctx      = browser.new_context()       
        page     = ctx.new_page()

        # 1. LOGIN 
        log("Abriendo login…")
        page.goto(LOGIN_URL)
        page.fill('input[name="user"]', USER)
        page.fill('input[name="pass"]', PASSWORD)
        page.click('#ingresar')
        try:
            page.wait_for_url("**/menu_admin", timeout=8000)
        except TimeoutError:
            log("❌ Login falló – revisa credenciales")
            sys.exit(1)
        log("✅ Login OK")

        # 2. ABRIR BUSCADOR 
        page.goto(BUSCADOR_URL)

        for sis in SIS_LISTA:
            log(f"▶︎ Buscando SIS {sis}")
            page.fill('#sis', sis)
            page.press('#sis', 'Enter')        
            try:
                page.wait_for_selector('a:text("Verificacion Fisica")', timeout=7000)
            except TimeoutError:
                log(f"⚠️  No se encontró resultado para {sis}")
                continue

            # 3. IR A VERIFICACIÓN FÍSICA 
            link = page.locator('a:text("Verificacion Fisica")').first
            href = link.get_attribute('href')
            estudiante_id = href.split("/")[2]   
            log(f"  ↳ ID estudiante {estudiante_id}")

            with page.expect_navigation():
                link.click()

            # 4. ACEPTAR TODOS LOS REQUISITOS FÍSICOS 
            procesar_tramite(page)
            log("  ✔️  Requisitos aceptados")

            # 5. VOLVER AL BUSCADOR PARA EL SIGUIENTE SIS 
            page.goto(BUSCADOR_URL)

        log("🏁 Proceso terminado")
        browser.close()

if __name__ == "__main__":
    main()
