import flet as ft
import os
import asyncio

# --- CONFIGURACIÓN DE VOZ ---
# En Android/Pydroid 3, usaremos la consola para el log de voz para evitar bloqueos
async def hablar_async(texto):
    """Lógica de respuesta de voz del Agente 2026"""
    print(f"🤖 AGENTE 2026: {texto}")

async def main(page: ft.Page):
    # Configuración de página premium
    page.title = "Agente 2026 - Servidor Pydroid"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0F172A"  # Azul muy oscuro
    
    # Estilo de la interfaz
    chat_display = ft.ListView(expand=True, spacing=10, padding=20)
    
    input_field = ft.TextField(
        hint_text="Ingresa un comando...",
        expand=True,
        border_radius=10,
        border_color="#10B981", # Verde esmeralda
        on_submit=lambda e: asyncio.create_task(enviar_comando(e))
    )

    async def enviar_comando(e):
        if not input_field.value: return
        
        user_text = input_field.value
        chat_display.controls.append(
            ft.Text(f"👤 Tú: {user_text}", color="#38BDF8", weight="bold")
        )
        input_field.value = ""
        page.update()

        # Respuesta lógica vinculada a tu estructura CORE
        respuesta = f"Ejecutando '{user_text}' en el servidor local de Pydroid 3."
        chat_display.controls.append(
            ft.Text(f"🤖 Agente: {respuesta}", color="#10B981")
        )
        page.update()
        await hablar_async(respuesta)

    # Construcción de la UI
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.icons.SATELLITE_ALT, color="#FBBF24"),
                    ft.Text("AGENTE 2026", size=28, weight="bold", color="#FBBF24")
                ], alignment="center"),
                ft.Text("Estado: Local / Sin Hibernación", size=10, italic=True),
                ft.Divider(color="#1E293B"),
                chat_display,
                ft.Row([
                    input_field,
                    ft.FloatingActionButton(
                        icon=ft.icons.SEND,
                        bgcolor="#10B981",
                        on_click=lambda e: asyncio.create_task(enviar_comando(e))
                    )
                ])
            ]),
            expand=True,
            padding=15
        )
    )

# --- INICIO DEL SERVIDOR ACTUALIZADO ---
if __name__ == "__main__":
    # Cambiamos a ft.run para evitar el DeprecationWarning de v0.80.4
    # host="0.0.0.0" permite que tu APK cliente vea el servidor
    ft.run(
        target=main,
        view=ft.AppView.WEB_BROWSER,
        host="0.0.0.0",
        port=8550
    )
