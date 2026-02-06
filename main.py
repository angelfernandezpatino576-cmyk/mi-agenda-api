import flet as ft
import os
from CORE.ia import investigar
from CORE.calendario import mostrar_calendario
from CORE.camara import activar_camara

async def main(page: ft.Page):
    page.title = "Agente 2026 - Central"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0F172A"
    
    chat_display = ft.Column(expand=True, scroll=ft.ScrollMode.ALWAYS)

    async def enviar_accion(e):
        user_text = input_field.value
        if not user_text: return
        
        chat_display.controls.append(ft.Container(content=ft.Text(f"Tú: {user_text}"), alignment=ft.alignment.center_right, padding=10, bgcolor="#1E293B", border_radius=10))
        input_field.value = ""
        page.update()

        # Respuesta desde CORE/ia.py
        respuesta = investigar(user_text)
        chat_display.controls.append(ft.Container(content=ft.Text(f"Agente: {respuesta}"), alignment=ft.alignment.center_left, padding=10, bgcolor="#38BDF8", border_radius=10))
        page.update()

    input_field = ft.TextField(hint_text="Comando...", expand=True, on_submit=enviar_accion)

    page.add(
        ft.Row([
            ft.Text("AGENTE 2026", size=20, weight="bold", color="#38BDF8"),
            ft.IconButton(ft.icons.CAMERA_ALT, on_click=lambda _: activar_camara(page)),
            ft.IconButton(ft.icons.CALENDAR_MONTH, on_click=lambda _: mostrar_calendario(page)),
        ], alignment="spaceBetween"),
        ft.Divider(),
        chat_display,
        ft.Row([input_field, ft.FloatingActionButton(icon=ft.icons.SEND, on_click=enviar_accion)])
    )

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    ft.app(target=main, host="0.0.0.0", port=port)
