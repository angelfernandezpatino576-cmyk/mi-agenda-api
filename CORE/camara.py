import flet as ft

def activar_camara(page: ft.Page):
    # Función simple para probar hardware
    def on_capture(e):
        page.snack_bar = ft.SnackBar(ft.Text("¡Captura simulada con éxito!"))
        page.snack_bar.open = True
        page.update()

    # En APK real, esto abre la interfaz de cámara
    page.snack_bar = ft.SnackBar(ft.Text("Inicializando Cámara..."))
    page.snack_bar.open = True
    page.update()
    return "Cámara activa"
