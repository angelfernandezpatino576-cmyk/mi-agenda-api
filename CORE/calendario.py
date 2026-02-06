import flet as ft

def mostrar_calendario(page: ft.Page):
    def on_date_change(e):
        page.snack_bar = ft.SnackBar(ft.Text(f"Fecha: {e.control.value}"))
        page.snack_bar.open = True
        page.update()

    dp = ft.DatePicker(on_change=on_date_change)
    page.overlay.append(dp)
    page.update()
    dp.pick_date()
