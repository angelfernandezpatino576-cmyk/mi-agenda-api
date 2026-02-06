import flet as ft

def seleccionar_fecha(page: ft.Page, text_field):
    def handle_change(e):
        text_field.value = f"Evento para el: {e.control.value.strftime('%Y-%m-%d')}"
        page.update()

    date_picker = ft.DatePicker(
        on_change=handle_change,
    )
    page.overlay.append(date_picker)
    date_picker.pick_date()
