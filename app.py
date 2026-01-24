import flet as ft
from groq import Groq
from tavily import TavilyClient

def main(page: ft.Page):
    page.title = "Agente IA 2026"
    page.theme_mode = ft.ThemeMode.DARK
    
    campo = ft.TextField(label="Consulta a la IA...", expand=True)
    texto = ft.Text("")

    def investigar(e):
        try:
            client = Groq(api_key='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')
            tavily = TavilyClient(api_key='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')
            search = tavily.search(query=campo.value)
            context = "\n".join([r['content'] for r in search['results']])
            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": f"Contexto: {context}\n\nPregunta: {campo.value}"}]
            )
            texto.value = res.choices[0].message.content
        except Exception as err:
            texto.value = f"Error: {err}"
        page.update()

    page.add(ft.Text("🤖 AGENTE 2026"), campo, ft.ElevatedButton("BUSCAR", on_click=investigar), texto)

if __name__ == "__main__":
    ft.app(target=main)
