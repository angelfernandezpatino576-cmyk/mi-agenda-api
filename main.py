import flet as ft
import os
from groq import Groq
from tavily import TavilyClient

# Configuración de las llaves (Tokens)
GROQ_KEY = "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"
TAVILY_KEY = "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"

# Inicialización de clientes
client_ai = Groq(api_key=GROQ_KEY)
tavily = TavilyClient(api_key=TAVILY_KEY)

async def main(page: ft.Page):
    page.title = "Agente 2026 - Asistente Personal"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0F172A"
    
    chat_display = ft.Column(expand=True, scroll=ft.ScrollMode.ALWAYS)
    
    async def procesar_comando(e):
        user_text = input_field.value
        if not user_text: return
        
        # 1. Mostrar mensaje del usuario
        chat_display.controls.append(ft.Text(f"Usted: {user_text}", color="#38BDF8"))
        input_field.value = ""
        page.update()

        # 2. El Agente "Investiga" en internet usando Tavily
        try:
            search_result = tavily.search(query=user_text, max_results=2)
            contexto = search_result['results']
            
            # 3. El Agente "Piensa" usando Groq
            response = client_ai.chat.completions.create(
                messages=[
                    {"role": "system", "content": "Eres el Agente 2026, un asistente personal eficiente. Usa el contexto de búsqueda para responder de forma breve y clara."},
                    {"role": "user", "content": f"Contexto: {contexto}\n\nPregunta: {user_text}"}
                ],
                model="llama3-8b-8192",
            )
            
            respuesta_final = response.choices[0].message.content
            chat_display.controls.append(ft.Text(f"Agente 2026: {respuesta_final}", color="#10B981"))
        except Exception as err:
            chat_display.controls.append(ft.Text(f"Error: {str(err)}", color="red"))
        
        page.update()

    input_field = ft.TextField(hint_text="¿En qué puedo ayudarte?", expand=True)
    send_button = ft.IconButton(icon=ft.icons.SEND_ROUNDED, on_click=procesar_comando)

    page.add(
        ft.Container(
            content=ft.Text("👽 AGENTE 2026 - ONLINE", size=20, weight="bold", color="#38BDF8"),
            padding=10
        ),
        ft.Container(content=chat_display, expand=True, bgcolor="#1E293B", padding=20, border_radius=15),
        ft.Row([input_field, send_button])
    )
    page.update()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    ft.app(target=main, host="0.0.0.0", port=port)
