import flet as ft

def activar_camara(page: ft.Page):
    def on_capture(e):
        page.snack_bar = ft.SnackBar(ft.Text("Imagen guardada"))
        page.snack_bar.open = True
        page.update()

    cam = ft.Camera(on_capture=on_capture)
    page.overlay.append(cam)
    page.update()
