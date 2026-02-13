import flet as ft

def activar_escucha(page: ft.Page):
    # Placeholder visual para la función de escucha
    page.snack_bar = ft.SnackBar(ft.Text("Escuchando... (Hable ahora)"))
    page.snack_bar.open = True
    page.update()
    return "Micro activo"
