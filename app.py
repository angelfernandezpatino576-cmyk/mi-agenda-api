import flet as ft
import requests
from groq import Groq
from tavily import TavilyClient

# CONFIGURACIÓN
LLAVE_GROQ = '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'
LLAVE_TAVILY = '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'
URL_API = "https://neutral-opossum-pruebaapk-bc9cecf4.koyeb.app/tareas/"

def main(page: ft.Page):
    page.title = "Agente IA 2026"
    page.theme_mode = ft.ThemeMode.DARK
    
    campo = ft.TextField(label="Consulta a la IA...", expand=True, multiline=True)
    texto_log = ft.Text("")
    progreso = ft.ProgressBar(visible=False)

    def investigar(e):
        if not campo.value: return
        progreso.visible = True
        texto_log.value = "🔍 Buscando..."
        page.update()
        try:
            client = Groq(api_key=LLAVE_GROQ)
            tavily = TavilyClient(api_key=LLAVE_TAVILY)
            
            search = tavily.search(query=campo.value)
            context = "\n".join([r['content'] for r in search['results']])
            
            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": f"Contexto: {context}\n\nPregunta: {campo.value}"}]
            )
            campo.value = res.choices[0].message.content
            texto_log.value = "✅ Éxito"
        except Exception as err:
            texto_log.value = f"❌ Error: {str(err)}"
        progreso.visible = False
        page.update()

    page.add(
        ft.Text("🤖 AGENTE 2026", size=25, weight="bold"),
        campo,
        progreso,
        ft.ElevatedButton("INVESTIGAR", on_click=investigar),
        texto_log
    )

if __name__ == "__main__":
    ft.app(target=main)
