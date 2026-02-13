import flet as ft
import os

# Importaciones del CORE
from CORE.ia import investigar
from CORE.camara import activar_camara
from CORE.calendario import mostrar_calendario
from CORE.microfono import activar_escucha

async def main(page: ft.Page):
    page.title = "Agente 2026 Pro"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0F172A"
    page.window_width = 400
    
    chat_display = ft.Column(expand=True, scroll=ft.ScrollMode.ALWAYS, spacing=10)

    async def enviar_peticion(e):
        texto = input_field.value
        if not texto: return
        
        # Mensaje de Usuario
        chat_display.controls.append(
            ft.Container(content=ft.Text(texto), alignment=ft.alignment.center_right, bgcolor="#1E293B", padding=10, border_radius=10)
        )
        input_field.value = ""
        page.update()

        # Respuesta de la IA
        respuesta = investigar(texto)
        chat_display.controls.append(
            ft.Container(content=ft.Text(respuesta), alignment=ft.alignment.center_left, bgcolor="#38BDF8", padding=10, border_radius=10)
        )
        page.update()

    input_field = ft.TextField(hint_text="Escribe un comando...", expand=True, on_submit=enviar_peticion)

    # Cabecera con iconos vinculados a CORE
    header = ft.Row([
        ft.Text("AGENTE 2026", size=22, weight="bold", color="#38BDF8"),
        ft.Row([
            ft.IconButton(ft.icons.MIC, on_click=lambda _: activar_escucha(page)),
            ft.IconButton(ft.icons.CAMERA_ALT, on_click=lambda _: activar_camara(page)),
            ft.IconButton(ft.icons.CALENDAR_MONTH, on_click=lambda _: mostrar_calendario(page, input_field)),
        ])
    ], alignment="spaceBetween")

    page.add(
        header,
        ft.Divider(height=2, color="#1E293B"),
        ft.Container(content=chat_display, expand=True),
        ft.Row([input_field, ft.FloatingActionButton(icon=ft.icons.SEND, on_click=enviar_peticion, bgcolor="#38BDF8")])
    )

if __name__ == "__main__":
    ft.app(target=main)
