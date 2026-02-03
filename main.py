import flet as ft
import os
import asyncio

# --- OPTIMIZACIÓN: DETECCIÓN DE ENTORNO ---
# Detectamos si estamos ejecutando dentro de Termux para el audio
IS_TERMUX = "com.termux" in os.environ.get("PREFIX", "")

async def hablar_async(texto):
    """Función de voz optimizada para Android/Termux"""
    if IS_TERMUX:
        # Requiere: pkg install termux-api y la app Termux:API instalada
        os.system(f'termux-tts-speak "{texto}"')
    else:
        print(f"Consola (Simulado): {texto}")

async def main(page: ft.Page):
    # Configuración de la página
    page.title = "Agente 2026 - Servidor Local"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = ft.ScrollMode.AUTO
    
    # Paleta de colores premium (basada en tu diseño original)
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary="#10B981", # Verde esmeralda
            secondary="#374151",
            background="#1A1A1A",
        )
    )

    # --- UI COMPONENTS ---
    titulo = ft.Text("👽 SISTEMA IA 2026", size=24, weight="bold", color="#FBBF24")
    resultado = ft.Text("Listo para recibir órdenes...", selectable=True, size=16)
    loading = ft.ProgressBar(width=400, color="amber", visible=False)
    
    campo = ft.TextField(
        label="Escribe aquí...", 
        expand=True,
        border_color="#374151",
        on_submit=lambda e: asyncio.create_task(ejecutar(e))
    )

    # --- LÓGICA DE EJECUCIÓN ---
    async def ejecutar(e):
        if not campo.value:
            return

        loading.visible = True
        campo.disabled = True
        input_usuario = campo.value
        page.update()

        # Aquí es donde conectarías con tus archivos en CORE/ia.py
        # Por ahora, una respuesta lógica simple:
        if "/investigar" in input_usuario.lower():
            respuesta = f"🔎 Iniciando protocolo de investigación sobre: {input_usuario.replace('/investigar', '').strip()}"
        else:
            respuesta = f"🤖 Agente 2026 procesando: {input_usuario}"

        resultado.value = respuesta
        loading.visible = False
        campo.disabled = False
        campo.value = ""
        page.update()

        # Audio asíncrono (no bloquea la pantalla)
        await hablar_async(respuesta)

    # --- DISEÑO DE LA INTERFAZ ---
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Row([titulo], alignment="center"),
                ft.Divider(color="#374151"),
                ft.Container(
                    content=resultado,
                    padding=20,
                    bgcolor="#111111",
                    border_radius=15,
                    min_height=150
                ),
                loading,
                ft.Row([campo], alignment="center"),
                ft.Row([
                    ft.ElevatedButton(
                        "ENVIAR COMANDO", 
                        icon=ft.icons.SEND,
                        on_click=lambda e: asyncio.create_task(ejecutar(e)),
                        style=ft.ButtonStyle(color="white", bgcolor="#10B981")
                    )
                ], alignment="center"),
            ], spacing=20),
            padding=20
        )
    )

# --- PASO 3 CORREGIDO: Usamos ft.run en lugar de ft.app ---
if __name__ == "__main__":
    ft.run(target=main, view=ft.AppView.WEB_BROWSER, port=8550)
