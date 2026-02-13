import flet as ft

def mostrar_calendario(page: ft.Page, input_field):
    def change_date(e):
        fecha = e.control.value.strftime('%Y-%m-%d')
        input_field.value = f"Agendar para el día: {fecha}"
        page.update()

    date_picker = ft.DatePicker(
        on_change=change_date,
        confirm_text="Seleccionar",
        cancel_text="Cancelar"
    )
    page.overlay.append(date_picker)
    page.update()
    date_picker.pick_date()
