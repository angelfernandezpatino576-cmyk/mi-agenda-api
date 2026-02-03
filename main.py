import flet as ft
import os
import asyncio

# --- CONFIGURACIÓN PARA TERMUX/ANDROID ---
# Detectamos si estamos en Termux para usar la voz del sistema
IS_TERMUX = "com.termux" in os.environ.get("PREFIX", "")

async def hablar_async(texto):
    """Lógica de voz optimizada para no bloquear el servidor"""
    if IS_TERMUX:
        # Usa la API de Termux para hablar por la bocina del celular
        os.system(f'termux-tts-speak "{texto}"')
    else:
        print(f"DEBUG (Voz): {texto}")

async def main(page: ft.Page):
    page.title = "Agente 2026 - Online"
    page.theme_mode = ft.ThemeMode.DARK
    
    # Estilo visual premium inspirado en tu diseño original
    page.theme = ft.Theme(color_scheme=ft.ColorScheme(primary="#10B981"))
    
    chat_display = ft.ListView(expand=True, spacing=10)
    input_field = ft.TextField(
        label="Escribe tu comando...", 
        expand=True,
        on_submit=lambda e: asyncio.create_task(procesar_mensaje(e))
    )

    async def procesar_mensaje(e):
        if not input_field.value: return
        
        mensaje = input_field.value
        chat_display.controls.append(ft.Text(f"👤 Tú: {mensaje}", color="blue", weight="bold"))
        input_field.value = ""
        page.update()

        # Simulación de respuesta conectada a tu CORE
        respuesta = f"🤖 Agente 2026: Procesando '{mensaje}' desde el servidor local..."
        chat_display.controls.append(ft.Text(respuesta, color="green"))
        page.update()
        
        await hablar_async(respuesta)

    page.add(
        ft.Text("👽 SISTEMA IA 2026", size=28, weight="bold", color="#FBBF24"),
        ft.Divider(color="#374151"),
        ft.Container(content=chat_display, expand=True, padding=10),
        ft.Row([
            input_field, 
            ft.IconButton(ft.icons.SEND_ROUNDED, on_click=lambda e: asyncio.create_task(procesar_mensaje(e)))
        ])
    )

# --- CORRECCIÓN DEL ERROR EN MAIN.PY ---
if __name__ == "__main__":
    # Usamos ft.run para evitar el DeprecationWarning de la v0.80.4
    # host="0.0.0.0" permite que entres desde tu PC u otro celular usando la IP
    ft.run(
        target=main, 
        view=ft.AppView.WEB_BROWSER, 
        host="0.0.0.0", 
        port=8550
    )
