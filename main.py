import flet as ft
import os
import asyncio

# --- CONFIGURACIÓN DE ENTORNO ---
IS_TERMUX = "com.termux" in os.environ.get("PREFIX", "")

async def hablar_async(texto):
    """Voz nativa para Termux/Android sin dependencias pesadas."""
    if IS_TERMUX:
        os.system(f'termux-tts-speak "{texto}"')
    else:
        print(f"DEBUG (Voz): {texto}")

async def main(page: ft.Page):
    page.title = "Agente 2026 - Control Local"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 450
    page.window_height = 800
    
    # Colores premium basados en tu diseño original
    page.theme = ft.Theme(color_scheme=ft.ColorScheme(primary="#10B981"))

    # UI Components
    chat_display = ft.ListView(expand=True, spacing=10, initial_scroll_index=0)
    user_input = ft.TextField(
        hint_text="Comando o consulta...",
        expand=True,
        on_submit=lambda e: asyncio.create_task(procesar_comando(e))
    )
    loading_bar = ft.ProgressBar(visible=False, color="amber")

    async def procesar_comando(e):
        if not user_input.value: return
        
        comando = user_input.value
        user_input.value = ""
        loading_bar.visible = True
        
        # Añadir mensaje del usuario al chat
        chat_display.controls.append(
            ft.Text(f"👤 Tú: {comando}", color="blue", weight="bold")
        )
        page.update()

        # --- INTEGRACIÓN CON CORE ---
        # Aquí es donde el sistema interactúa con tus scripts en CORE/
        await asyncio.sleep(1) # Simulación de proceso
        
        if "/investigar" in comando.lower():
            respuesta = f"🔎 Iniciando protocolo de investigación en CORE/ia.py para: {comando}"
        else:
            respuesta = f"🤖 Agente 2026: Entendido. Ejecutando acción para '{comando}'."

        # Mostrar respuesta y hablar
        chat_display.controls.append(ft.Text(f"🤖 {respuesta}", color="green"))
        loading_bar.visible = False
        page.update()
        
        await hablar_async(respuesta)

    # Layout Principal
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Text("👽 SISTEMA IA 2026", size=28, weight="bold", color="#FBBF24"),
                ft.Divider(color="#374151"),
                ft.Container(content=chat_display, expand=True, padding=10),
                loading_bar,
                ft.Row([user_input, ft.IconButton(ft.icons.SEND_ROUNDED, on_click=lambda e: asyncio.create_task(procesar_comando(e)))]),
                ft.Row([
                    ft.TextButton("Cámara", icon=ft.icons.CAMERA_ALT),
                    ft.TextButton("Calendario", icon=ft.icons.CALENDAR_MONTH),
                ], alignment="center")
            ]),
            expand=True,
            padding=20
        )
    )

# Cambiado a ft.run para compatibilidad moderna y evitar DeprecationWarnings
if __name__ == "__main__":
    ft.run(target=main, view=ft.AppView.WEB_BROWSER, port=8550)
