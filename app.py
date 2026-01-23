import flet as ft
import requests
from groq import Groq
from tavily import TavilyClient

# CONFIGURACIÓN
LLAVE_GROQ = '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'
LLAVE_TAVILY = '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'
URL_API = "https://neutral-opossum-pruebaapk-bc9cecf4.koyeb.app/tareas/"

# Inicialización segura
try:
    client_groq = Groq(api_key=LLAVE_GROQ)
    tavily = TavilyClient(api_key=LLAVE_TAVILY)
except:
    pass

def main(page: ft.Page):
    page.title = "Agente 2026"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = "adaptive"
    
    campo = ft.TextField(label="¿En qué te ayudo?", expand=True, multiline=True)
    texto_log = ft.Text("")
    progreso = ft.ProgressBar(visible=False)

    def accion_ia(e):
        if not campo.value: return
        progreso.visible = True
        texto_log.value = "🔍 Investigando..."
        page.update()
        try:
            busqueda = tavily.search(query=campo.value)
            contexto = "\n".join([r['content'] for r in busqueda['results']])
            res = client_groq.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": f"{contexto}\n\nPregunta: {campo.value}"}]
            )
            campo.value = res.choices[0].message.content
            texto_log.value = "✅ Análisis completado"
        except Exception as err:
            texto_log.value = f"Error: {err}"
        progreso.visible = False
        page.update()

    page.add(
        ft.Text("🤖 SISTEMA IA 2026", size=25, weight="bold", color="blue"),
        campo,
        progreso,
        ft.ElevatedButton("INVESTIGAR", icon=ft.Icons.SEARCH, on_click=accion_ia),
        texto_log
    )

if __name__ == "__main__":
    ft.app(target=main)
