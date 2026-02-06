import flet as ft

def abrir_camara(page: ft.Page):
    # En Flet, la cámara se maneja mediante el control Camera
    def on_capture(e):
        print("Imagen capturada")

    cam = ft.Camera(
        on_update=lambda e: print("Cámara lista"),
        on_capture=on_capture,
    )
    
    # Añadimos la cámara al overlay para que sea visible
    page.overlay.append(cam)
    page.update()
    return "Cámara inicializada"
