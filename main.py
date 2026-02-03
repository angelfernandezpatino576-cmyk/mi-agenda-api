import flet as ft
import os
import asyncio
import sys

# --- OPTIMIZACIÓN 1: DETECCIÓN DE ENTORNO ---
# Detectamos si estamos ejecutando dentro de Termux
IS_TERMUX = "com.termux" in os.environ.get("PREFIX", "")

# Función de voz optimizada para Android/Termux
async def hablar_async(texto):
    if IS_TERMUX:
        # Usa la API nativa de Android a través de Termux
        # Requiere instalar la app "Termux:API" y el paquete "pkg install termux-api"
        os.system(f'termux-tts-speak "{texto}"')
    else:
        # Fallback para pruebas en PC (Windows/Linux)
        # Importamos aquí para no causar errores en Android si falta la librería
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.say(texto)
            engine.runAndWait()
        except ImportError:
            print(f"Audio simulado: {texto}")

async def main(page: ft.Page):
    page.title = "Agente 2026 - Servidor Termux"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = ft.ScrollMode.AUTO

    # Configuración adaptable para móviles
    page.window_width = 400 
    page.window_height = 800

    # --- UI COMPONENTS ---
    titulo = ft.Text("👽 SISTEMA IA 2026", size=22, weight="bold", color="#FBBF24")
    
    # Campo de texto que acepta "Enter" para enviar
    campo = ft.TextField(
        label="Haz tu pregunta...", 
        expand=True, 
        multiline=True,
        on_submit=lambda e: asyncio.create_task(ejecutar(e)) # Envío con Enter
    )
    
    resultado = ft.Text("", selectable=True, size=16)
    loading = ft.ProgressBar(width=400, color="amber", visible=False)

    # --- LOGICA DEL ASISTENTE ---
    async def ejecutar(e):
        pregunta_usuario = campo.value
        if not pregunta_usuario:
            return

        # 1. Feedback visual inmediato
        loading.visible = True
        campo.disabled = True
        resultado.value = "⏳ Procesando..."
        page.update()

        # 2. Lógica (Aquí conectarías con tu carpeta CORE/ia.py)
        respuesta = ""
        
        # Simulación de procesamiento asíncrono (no congela la app)
        await asyncio.sleep(0.5) 

        if pregunta_usuario.startswith("/investigar "):
            tema = pregunta_usuario.replace("/investigar ", "")
            respuesta = f"🔎 Iniciando protocolo de investigación sobre: {tema}..."
            # Aquí llamarías a: await ia.investigar(tema)
        else:
            # Aquí conectarías tu LLM local u online
            respuesta = f"🤖 Recibido: {pregunta_usuario}. (Aquí iría la respuesta de la IA)"

        # 3. Salida de audio y texto
        resultado.value = respuesta
        loading.visible = False
        campo.disabled = False
        campo.value = "" # Limpiar campo
        campo.focus()
        page.update()

        # Hablar sin congelar la UI
        await hablar_async(respuesta)

    # --- BOTONES ---
    btn_investigar = ft.ElevatedButton(
        "INVESTIGAR", 
        icon=ft.icons.SEARCH, 
        on_click=lambda e: asyncio.create_task(ejecutar(e)),
        bgcolor="#1A1A1A",
        color="white"
    )

    # Layout optimizado
    page.add(
        ft.Row([titulo], alignment="center"),
        ft.Divider(color="#374151"),
        ft.Container(
            content=resultado,
            padding=10,
            bgcolor="#111111",
            border_radius=10,
            min_height=100
        ),
        loading,
        ft.Row([campo], alignment="center"),
        ft.Row([btn_investigar], alignment="spaceEvenly"),
        ft.Text("Servidor Local Activo", size=10, color="grey", text_align="center")
    )

# Para modo web (servidor) en Termux:
ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8550)
