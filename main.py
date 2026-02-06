import flet as ft
import os

# Importaciones del CORE
from CORE.ia import investigar
from CORE.calendario import mostrar_calendario
from CORE.camara import activar_camara

async def main(page: ft.Page):
    page.title = "Agente 2026 - Central Pro"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0F172A"
    
    chat_display = ft.Column(expand=True, scroll=ft.ScrollMode.ALWAYS)

    async def enviar_peticion(e):
        texto = input_field.value
        if not texto: return
        
        chat_display.controls.append(ft.Text(f"Tú: {texto}", color="white"))
        input_field.value = ""
        page.update()

        # Llamada al módulo CORE/ia.py
        respuesta = investigar(texto)
        chat_display.controls.append(ft.Text(f"Agente: {respuesta}", color="#38BDF8"))
        page.update()

    input_field = ft.TextField(hint_text="¿En qué te ayudo?", expand=True, on_submit=enviar_peticion)

    # Cabecera con botones vinculados a CORE
    header = ft.Row([
        ft.Text("AGENTE 2026", size=20, weight="bold", color="#38BDF8"),
        ft.Row([
            ft.IconButton(ft.icons.CAMERA_ALT, on_click=lambda _: activar_camara(page)),
            ft.IconButton(ft.icons.CALENDAR_MONTH, on_click=lambda _: mostrar_calendario(page)),
        ])
    ], alignment="spaceBetween")

    page.add(
        header,
        ft.Divider(),
        chat_display,
        ft.Row([input_field, ft.FloatingActionButton(icon=ft.icons.SEND, on_click=enviar_peticion)])
    )

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    ft.app(target=main, host="0.0.0.0", port=port)
