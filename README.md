

### Guía de Instalación

1.  **Clona o descarga el repositorio:**
    ```bash
    git clone [https://github.com/tu-usuario/ruge-automatization.git](https://github.com/tu-usuario/ruge-automatization.git)
    cd ruge-automatization
    ```

2.  **Crea un entorno virtual:**
    Esto aísla las dependencias del proyecto para no interferir con otros proyectos de Python en tu sistema.
    ```bash
    python -m venv .venv
    ```

3.  **Activa el entorno virtual:**
    -   En Windows:
        ```bash
        .venv\Scripts\activate
        ```
    -   En macOS y Linux:
        ```bash
        source .venv/bin/activate
        ```
    *Verás `(.venv)` al principio de la línea de tu terminal si se activó correctamente.*

4.  **Crea el archivo `requirements.txt`:**
    Crea un archivo llamado `requirements.txt` en la raíz del proyecto y pega el siguiente contenido:
    ```txt
    Flask
    Flask-SocketIO
    playwright
    simple-proxy
    ```

5.  **Instala las dependencias:**
    Este comando leerá el archivo `requirements.txt` e instalará todas las librerías necesarias.
    ```bash
    pip install -r requirements.txt
    ```

6.  **Instala los navegadores para Playwright:**
    Este es un paso único para descargar los navegadores que Playwright controlará.
    ```bash
    playwright install
    ```

¡Listo! La instalación ha finalizado.

## ¿Cómo Usar la Aplicación?

1.  **Inicia el servidor:**
    Asegúrate de que tu entorno virtual esté activado y ejecuta el siguiente comando:
    ```bash
    python app.py
    ```
    Verás un mensaje en la terminal indicando que el servidor está corriendo en `http://127.0.0.1:5000`.

2.  **Abre la aplicación en tu navegador:**
    Ve a la dirección [http://127.0.0.1:5000](http://127.0.0.1:5000).

3.  **Completa el formulario:**
    -   Ingresa tu **Usuario** y **Contraseña** del sistema RUGE.
    -   En el área de texto, pega la **lista de códigos SIS** que deseas procesar, asegurándote de que haya un código por línea.

4.  **Inicia el proceso:**
    Haz clic en el botón "Iniciar Proceso". El panel de "Logs en Tiempo Real" a la derecha comenzará a mostrar el progreso de la automatización.

## Estructura del Proyecto