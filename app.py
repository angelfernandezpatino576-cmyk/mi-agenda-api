import flet as ft
import requests
from groq import Groq
from tavily import TavilyClient

# CONFIGURACIÓN IA
LLAVE_GROQ = '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'
LLAVE_TAVILY = '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'

def main(page: ft.Page):
    page.title = "Agente IA 2026"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = "adaptive"
    
    campo = ft.TextField(label="Escribe tu consulta...", expand=True, multiline=True)
    texto_resumen = ft.Text("")
    progreso = ft.ProgressBar(visible=False)

    def investigar(e):
        if not campo.value: return
        progreso.visible = True
        texto_resumen.value = "🔍 Analizando fuentes en tiempo real..."
        page.update()
        try:
            client = Groq(api_key=LLAVE_GROQ)
            tavily = TavilyClient(api_key=LLAVE_TAVILY)
            
            # Búsqueda Web
            search = tavily.search(query=campo.value)
            context = "\n".join([r['content'] for r in search['results']])
            
            # Procesamiento Llama 3.3
            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": f"Contexto: {context}\n\nPregunta: {campo.value}"}]
            )
            campo.value = res.choices[0].message.content
            texto_resumen.value = "✅ Investigación finalizada con éxito."
        except Exception as err:
            texto_resumen.value = f"❌ Error: {str(err)}"
        
        progreso.visible = False
        page.update()

    page.add(
        ft.Text("🤖 AGENTE EJECUTIVO 2026", size=24, weight="bold", color="blue"),
        campo,
        progreso,
        ft.ElevatedButton("INICIAR BÚSQUEDA IA", icon=ft.Icons.AUTO_AWESOME, on_click=investigar),
        texto_resumen
    )

if __name__ == "__main__":
    ft.app(target=main)
