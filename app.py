import flet as ft
import requests
from groq import Groq
from tavily import TavilyClient

# ⚙️ CONFIGURACIÓN - Verificada 2026
LLAVE_GROQ = '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'
LLAVE_TAVILY = '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'
URL_API = "https://neutral-opossum-pruebaapk-bc9cecf4.koyeb.app/tareas/"

# Inicialización de clientes
try:
    client_groq = Groq(api_key=LLAVE_GROQ)
    tavily = TavilyClient(api_key=LLAVE_TAVILY)
except Exception as e:
    print(f"Error inicializando APIs: {e}")

def main(page: ft.Page):
    page.title = "Agente Ejecutivo 2026"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.scroll = "adaptive"

    # Componentes de la interfaz
    campo_texto = ft.TextField(
        label="Escribe una tarea o pregunta...",
        multiline=True,
        min_lines=1,
        max_lines=8,
        expand=True,
        border_color="blue"
    )
    
    progreso = ft.ProgressBar(visible=False, color="blue")
    texto_estado = ft.Text("", size=12, color="gray")

    # --- FUNCIÓN 1: INVESTIGAR CON IA + WEB ---
    def investigar(e):
        if not campo_texto.value: return
        progreso.visible = True
        texto_estado.value = "🔍 Navegando en la web y consultando a Llama 3.3..."
        page.update()

        try:
            # Búsqueda en tiempo real
            busqueda = tavily.search(query=campo_texto.value, search_depth="advanced")
            contexto = "\n".join([r['content'] for r in busqueda['results']])
            
            # Procesamiento con Groq
            prompt = f"INFO WEB 2026: {contexto}\n\nPregunta: {campo_texto.value}"
            res = client_groq.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "Eres un asistente experto. Responde de forma concisa usando la info web proporcionada."},
                    {"role": "user", "content": prompt}
                ]
            )
            campo_texto.value = res.choices[0].message.content
            texto_estado.value = "✅ Análisis completado."
        except Exception as ex:
            texto_estado.value = f"❌ Error de IA: {str(ex)}"
        
        progreso.visible = False
        page.update()

    # --- FUNCIÓN 2: GUARDAR EN KOYEB ---
    def guardar(e):
        if not campo_texto.value: return
        progreso.visible = True
        page.update()
        
        nueva_tarea = {
            "titulo": campo_texto.value[:100].replace("\n", " "),
            "fecha_limite": "2026-01-23",
            "estado": "pendiente"
        }
        
        try:
            r = requests.post(URL_API, json=nueva_tarea, timeout=10)
            if r.status_code == 200:
                campo_texto.value = ""
                texto_estado.value = "💾 Guardado exitosamente en la base de datos."
            else:
                texto_estado.value = f"⚠️ Error del servidor: {r.status_code}"
        except:
            texto_estado.value = "❌ Error de conexión con Koyeb."
        
        progreso.visible = False
        page.update()

    # --- DISEÑO DE LA APP ---
    page.add(
        ft.Header(ft.Text("🤖 AGENTE 2026 PRO", size=22, weight="bold", color="blue")),
        ft.Divider(height=10, color="transparent"),
        ft.Row([campo_texto]),
        progreso,
        texto_estado,
        ft.Divider(height=10, color="transparent"),
        ft.Row([
            ft.ElevatedButton(
                "INVESTIGAR", 
                icon=ft.Icons.LANGUAGE, 
                on_click=investigar,
                style=ft.ButtonStyle(bgcolor="blue", color="white")
            ),
            ft.ElevatedButton(
                "GUARDAR", 
                icon=ft.Icons.SAVE, 
                on_click=guardar,
                style=ft.ButtonStyle(bgcolor="green", color="white")
            ),
        ], alignment=ft.MainAxisAlignment.CENTER),
    )

# Ejecución
if __name__ == "__main__":
    ft.app(target=main)
