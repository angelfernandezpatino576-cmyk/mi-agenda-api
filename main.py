import flet as ft
import os
import asyncio
from groq import Groq
from tavily import TavilyClient

# ==========================================================
# CONFIGURACIÓN DE NÚCLEO (CORE INTEGRATION)
# ==========================================================
# Estos tokens alimentan la lógica de los archivos en /CORE
GROQ_KEY = "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"
TAVILY_KEY = "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"

# Inicialización de servicios globales
client_ai = Groq(api_key=GROQ_KEY)
tavily = TavilyClient(api_key=TAVILY_KEY)

async def main(page: ft.Page):
    # Configuración de la Interfaz del Asistente
    page.title = "Agente 2026 - Central Pro"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0F172A"
    page.window_width = 450
    page.window_height = 800
    page.scroll = ft.ScrollMode.HIDDEN
    
    # Manejador de Permisos para hardware (Cámara y Micro en /CORE)
    ph = ft.PermissionHandler()
    page.overlay.append(ph)

    # Contenedor de mensajes
    chat_display = ft.Column(expand=True, scroll=ft.ScrollMode.ALWAYS, spacing=15)

    # --- FUNCIONES DE HARDWARE (Relacionadas con CORE/camara.py y CORE/microfono.py) ---
    async def gestionar_hardware(tipo):
        if tipo == "microfono":
            status = await ph.request_permission(ft.PermissionType.MICROPHONE)
        else:
            status = await ph.request_permission(ft.PermissionType.CAMERA)
        
        color = "green" if status == ft.PermissionStatus.GRANTED else "red"
        page.snack_bar = ft.SnackBar(ft.Text(f"Estado de {tipo}: {status}"), bgcolor=color)
        page.snack_bar.open = True
        page.update()

    # --- MOTOR DE RESPUESTA (Relacionado con CORE/ia.py y CORE/calendario.py) ---
    async def ejecutar_asistente(e):
        user_input = input_field.value
        if not user_input: return
        
        # UI: Registro de usuario
        chat_display.controls.append(
            ft.Container(
                content=ft.Text(user_input, color="white"),
                alignment=ft.alignment.center_right,
                padding=12, bgcolor="#1E293B", border_radius=15
            )
        )
        input_field.value = ""
        
        # Animación de carga
        loader = ft.Row([ft.ProgressRing(width=16, height=16, stroke_width=2), ft.Text(" Procesando...", size=12)], alignment="center")
        chat_display.controls.append(loader)
        page.update()

        try:
            # 1. Búsqueda en la web (Tavily)
            busqueda = tavily.search(query=user_input, search_depth="advanced", max_results=2)
            contexto_web = busqueda['results']

            # 2. Inteligencia Artificial (Groq)
            # Aquí se procesa si la orden es para el CALENDARIO o información general
            prompt_sistema = (
                "Eres el Agente 2026. Tienes acceso a los módulos en la carpeta CORE: "
                "calendario, cámara, micrófono e IA. Si el usuario pide agendar algo, "
                "confirma que usarás el módulo de calendario."
            )
            
            completion = client_ai.chat.completions.create(
                messages=[
                    {"role": "system", "content": prompt_sistema},
                    {"role": "user", "content": f"Web Context: {contexto_web}\n\nOrden: {user_input}"}
                ],
                model="llama3-8b-8192",
            )
            
            respuesta_agente = completion.choices[0].message.content
            
            # UI: Respuesta del Agente
            chat_display.controls.remove(loader)
            chat_display.controls.append(
                ft.Container(
                    content=ft.Text(respuesta_agente, color="white"),
                    alignment=ft.alignment.center_left,
                    padding=12, bgcolor="#38BDF8", border_radius=15
                )
            )
        except Exception as ex:
            chat_display.controls.remove(loader)
            chat_display.controls.append(ft.Text(f"Error en CORE: {str(ex)}", color="red", size=10))
        
        page.update()

    # --- COMPONENTES VISUALES ---
    input_field = ft.TextField(
        hint_text="Comando de voz o texto...",
        expand=True,
        border_radius=25,
        bgcolor="#1E293B",
        on_submit=ejecutar_asistente,
        content_padding=15
    )

    header = ft.Container(
        content=ft.Row([
            ft.Text("AGENTE 2026", weight="bold", size=22, color="#38BDF8"),
            ft.Row([
                ft.IconButton(ft.icons.MIC_NONE_ROUNDED, on_click=lambda _: gestionar_hardware("microfono")),
                ft.IconButton(ft.icons.CAMERA_ALT_OUTLINED, on_click=lambda _: gestionar_hardware("camara")),
            ])
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=10
    )

    # --- ESTRUCTURA DE PÁGINA ---
    page.add(
        header,
        ft.Divider(color="#1E293B", height=1),
        ft.Container(
            content=chat_display,
            expand=True,
            padding=10
        ),
        ft.Container(
            content=ft.Row([
                input_field,
                ft.FloatingActionButton(icon=ft.icons.SEND_ROUNDED, on_click=ejecutar_asistente, bgcolor="#38BDF8")
            ]),
            padding=10
        )
    )
    page.update()

# --- INICIO DE SERVIDOR (KOYEB) ---
if __name__ == "__main__":
    puerto = int(os.getenv("PORT", 8080))
    ft.app(target=main, host="0.0.0.0", port=puerto)
