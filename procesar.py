# procesar.py
def procesar_tramite(page):
    """
    Recorre el Smart-Wizard y envía la aceptación final,
    aunque el botón #aceptar esté disabled.
    """
    while True:
        # 1) Acepta requisito del paso actual (si hay botón visible)
        for btn in page.locator('button.aceptar:visible').all():
            btn.click()
            page.wait_for_load_state('networkidle')

        # 2) Si ya existe el form final → enviarlo y salir
        if page.locator('form[action*="aceptado_fisica"]').count():
            page.evaluate("""() => {
                const f = document.querySelector('form[action*="aceptado_fisica"]');
                if (f) f.requestSubmit();
            }""")
            page.wait_for_load_state('networkidle')
            return

        # 3) Avanza al siguiente paso del wizard
        nxt = page.locator('button.sw-btn-next:visible').first
        if nxt.count():
            nxt.click()
            page.wait_for_timeout(400)        # pequeña pausa
        else:
            throw_msg = "No Next y sin form final: wizard atascado"
            raise RuntimeError(throw_msg)
