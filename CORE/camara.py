import flet as ft

def mostrar_calendario(page):
    def on_date_change(e):
        page.snack_bar = ft.SnackBar(ft.Text(f"Fecha seleccionada: {e.control.value}"))
        page.snack_bar.open = True
        page.update()

    dp = ft.DatePicker(on_change=on_date_change)
    page.overlay.append(dp)

    return ft.IconButton(icon=ft.icons.CALENDAR_MONTH, on_click=lambda _: dp.pick_date())
