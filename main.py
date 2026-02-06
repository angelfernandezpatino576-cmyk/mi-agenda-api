import flet as ft
import os
from groq import Groq
from tavily import TavilyClient

# ==========================================================
# CONFIGURACIÓN DE CRUCIAL: TOKENS Y LLAVES
# ==========================================================
GROQ_KEY = "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"
TAVILY_KEY = "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"

# Inicialización de clientes de IA y Búsqueda
client_ai = Groq(api_key=GROQ_KEY)
tavily = TavilyClient(api_key=TAVILY_KEY)

async def main(page: ft.Page):
    # Configuración estética de la aplicación
    page.title = "Agente 2026 - Asistente Personal"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0F172A"  # Azul oscuro profesional
    page.padding = 20
    
    # Contenedor de mensajes (el cuerpo del chat)
    chat_display = ft.Column(expand=True, scroll=ft.ScrollMode.ALWAYS, spacing=10)

    # Función principal de procesamiento de comandos
    async def procesar_comando(e):
        user_text = input_field.value
        if not user_text:
            return
        
        # 1. Mostrar mensaje del usuario en pantalla
        chat_display.controls.append(
            ft.Container(
                content=ft.Text(f"Tú: {user_text}", color="white"),
                alignment=ft.alignment.center_right,
                padding=10,
                bgcolor="#1E293B",
                border_radius=10
            )
        )
        input_field.value = ""
        page.update()

        # Indicador de "Pensando..."
        thinking_text = ft.Text("Agente 2026 está investigando...", italic=True, color="#94A3B8")
        chat_display.controls.append(thinking_text)
        page.update()

        try:
            # 2. BÚSQUEDA: El Agente usa Tavily para consultar internet
            search_result = tavily.search(query=user_text, max_results=3, search_depth="advanced")
            contexto = search_result['results']
            
            # 3. RAZONAMIENTO: El Agente usa Groq (Llama 3) para generar la respuesta
            response = client_ai.chat.completions.create(
                messages=[
                    {
                        "role": "system", 
                        "content": (
                            "Eres el Agente 2026, un asistente personal avanzado. "
                            "Tu objetivo es ser útil, preciso y breve. Usa el contexto de búsqueda "
                            "proporcionado para dar respuestas actualizadas. Si es un recordatorio, "
                            "confirma que lo has anotado."
                        )
                    },
                    {"role": "user", "content": f"Contexto de internet: {contexto}\n\nPregunta del usuario: {user_text}"}
                ],
                model="llama3-8b-8192",
            )
            
            respuesta_final = response.choices[0].message.content
            
            # 4. Mostrar respuesta del Agente
            chat_display.controls.remove(thinking_text)
            chat_display.controls.append(
                ft.Container(
                    content=ft.Text(f"Agente 2026: {respuesta_final}", color="white"),
                    alignment=ft.alignment.center_left,
                    padding=10,
                    bgcolor="#38BDF8",
                    border_radius=10
                )
            )
        except Exception as err:
            chat_display.controls.remove(thinking_text)
            chat_display.controls.append(ft.Text(f"Error de conexión: {str(err)}", color="red"))
        
        page.update()

    # Componentes de entrada
    input_field = ft.TextField(
        hint_text="Escribe un comando o pregunta...",
        expand=True,
        border_color="#38BDF8",
        on_submit=procesar_comando
    )
    
    send_button = ft.FloatingActionButton(
        icon=ft.icons.SEND_ROUNDED,
        on_click=procesar_comando,
        bgcolor="#38BDF8"
    )

    # Construcción de la interfaz
    page.add(
        ft.Row([
            ft.Icon(ft.icons.SUPPORT_AGENT, color="#38BDF8", size=30),
            ft.Text("AGENTE 2026 V1.0", size=22, weight="bold", color="#38BDF8"),
            ft.Icon(ft.icons.CIRCLE, color="green", size=10), # Indicador para HetrixTools
        ], alignment=ft.MainAxisAlignment.CENTER),
        
        ft.Divider(height=20, color="#1E293B"),
        
        ft.Container(
            content=chat_display,
            expand=True,
            bgcolor="#0F172A",
            padding=10,
        ),
        
        ft.Row([input_field, send_button], vertical_alignment=ft.CrossAxisAlignment.CENTER)
    )
    page.update()

# Ejecución del servidor compatible con Koyeb
if __name__ == "__main__":
    # Koyeb inyecta el puerto en la variable de entorno 'PORT'
    puerto_koyeb = int(os.getenv("PORT", 8080))
    
    ft.app(
        target=main,
        host="0.0.0.0",  # Necesario para acceso externo
        port=puerto_koyeb,
        view=None        # Modo servidor (sin ventana local)
    )
