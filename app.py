import flet as ft
from groq import Groq
from tavily import TavilyClient

# --- CONFIGURACIÓN DE LLAVES ---
LLAVE_GROQ = "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"
LLAVE_TAVILY = "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"

def main(page: ft.Page):
    page.title = "Agente IA 2026"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.padding = 20

    titulo = ft.Text("🤖 SISTEMA IA 2026", size=28, weight="bold", color="blue")
    subtitulo = ft.Text("Investigación en tiempo real", size=16, color="grey")

    campo_busqueda = ft.TextField(
        label="¿Qué deseas investigar?",
        hint_text="Ej: ¿Cómo estará el clima en 2026?",
        expand=True,
        multiline=True,
        min_lines=1,
        max_lines=3
    )

    texto_resultado = ft.Text("", selectable=True)
    progreso = ft.ProgressBar(visible=False, color="blue")

    def ejecutar_ia(e):
        if not campo_busqueda.value:
            texto_resultado.value = "⚠️ Por favor ingresa una pregunta."
            page.update()
            return

        progreso.visible = True
        texto_resultado.value = "🔍 Consultando fuentes web y procesando..."
        page.update()

        try:
            client_groq = Groq(api_key=LLAVE_GROQ)
            tavily = TavilyClient(api_key=LLAVE_TAVILY)

            busqueda = tavily.search(query=campo_busqueda.value)
            resultados = busqueda.get("results", [])

            if not resultados:
                texto_resultado.value = "⚠️ No se encontraron resultados relevantes."
            else:
                contexto = "\n".join([r.get("content", "") for r in resultados])

                respuesta_ia = client_groq.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "Eres un asistente de investigación avanzado. Usa el contexto proporcionado para responder de forma precisa."},
                        {"role": "user", "content": f"Contexto: {contexto}\n\nPregunta: {campo_busqueda.value}"}
                    ]
                )

                texto_resultado.value = respuesta_ia.choices[0].message.content

        except Exception as error:
            texto_resultado.value = f"❌ Error del sistema: {str(error)}"

        progreso.visible = False
        page.update()

    btn_buscar = ft.ElevatedButton(
        "INICIAR INVESTIGACIÓN",
        icon=ft.Icons.SEARCH,
        on_click=ejecutar_ia,
        style=ft.ButtonStyle(padding=20)
    )

    page.add(
        titulo,
        subtitulo,
        ft.Divider(height=20, color="transparent"),
        campo_busqueda,
        progreso,
        btn_buscar,
        ft.Divider(height=20),
        texto_resultado
    )

if __name__ == "__main__":
    ft.app(target=main)
