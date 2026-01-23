import flet as ft
import requests
from groq import Groq
from tavily import TavilyClient

# ⚙️ CONFIGURACIÓN - LLAVES Y URL
LLAVE_GROQ = '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'
LLAVE_TAVILY = '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'
URL_API = "https://neutral-opossum-pruebaapk-bc9cecf4.koyeb.app/tareas/"

# Inicialización segura de las herramientas de IA
try:
    client_groq = Groq(api_key=LLAVE_GROQ)
    tavily = TavilyClient(api_key=LLAVE_TAVILY)
except Exception as e:
    print(f"Error de inicialización: {e}")

def main(page: ft.Page):
    page.title = "Agente Ejecutivo 2026"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = "adaptive"
    page.padding = 20

    # Componentes de Interfaz
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

    # --- FUNCIÓN: INVESTIGAR CON IA + INTERNET ---
    def investigar(e):
        if not campo_texto.value: return
        progreso.visible = True
        texto_estado.value = "🔍 Buscando en 2026 y procesando con Llama 3.3..."
        page.update()

        try:
            # 1. Búsqueda Web
            busqueda = tavily.search(query=campo_texto.value, search_depth="advanced")
            contexto = "\n".join([r['content'] for r in busqueda['results']])
            
            # 2. Análisis con IA
            prompt = f"INFO WEB ACTUALIZADA: {contexto}\n\nPregunta: {campo_texto.value}"
            res = client_groq.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "Eres un asistente ejecutivo en 2026. Responde de forma precisa usando la info web."},
                    {"role": "user", "content": prompt}
                ]
            )
            campo_texto.value = res.choices[0].message.content
            texto_estado.value = "✅ Análisis completado con éxito."
        except Exception as ex:
            texto_estado.value = f"❌ Error: {str(ex)}"
        
        progreso.visible = False
        page.update()

    # --- FUNCIÓN: GUARDAR TAREA EN KOYEB ---
    def guardar(e):
        if not campo_texto.value: return
        progreso.visible = True
        page.update()
        
        # Preparamos el dato para la base de datos
        resumen_tarea = campo_texto.value[:100].replace("\n", " ")
        nueva_tarea = {
            "titulo": resumen_tarea,
            "fecha_limite": "2026-01-23",
            "estado": "pendiente"
        }
        
        try:
            r = requests.post(URL_API, json=nueva_tarea, timeout=10)
            if r.status_code == 200:
                campo_texto.value = ""
                texto_estado.value = "💾 Tarea guardada en la nube (Koyeb)."
            else:
                texto_estado.value = f"⚠️ Error Servidor: {r.status_code}"
        except:
            texto_estado.value = "❌ No hay conexión con el servidor de tareas."
        
        progreso.visible = False
        page.update()

    # --- CONSTRUCCIÓN DE LA PANTALLA ---
    page.add(
        ft.Text("🤖 AGENTE 2026 PRO", size=24, weight="bold", color="blue"),
        ft.Divider(height=10, color="transparent"),
        ft.Row([campo_texto]),
        progreso,
        texto_estado,
        ft.Divider(height=20, color="transparent"),
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

# Lanzamiento oficial de la App
if __name__ == "__main__":
    ft.app(target=main)
