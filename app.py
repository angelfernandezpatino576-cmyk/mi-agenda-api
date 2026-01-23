import flet as ft
import requests
from groq import Groq
from tavily import TavilyClient

# ⚙️ CONFIGURACIÓN (Tus llaves del bot)
LLAVE_GROQ = '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'
LLAVE_TAVILY = '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'
URL_API = "https://neutral-opossum-pruebaapk-bc9cecf4.koyeb.app/tareas/"

client_groq = Groq(api_key=LLAVE_GROQ)
tavily = TavilyClient(api_key=LLAVE_TAVILY)

def main(page: ft.Page):
    page.title = "Súper Agenda IA 2026"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = "adaptive"

    # --- FUNCIÓN: BUSCAR EN INTERNET + IA ---
    def investigar_con_ia(e):
        if not campo_texto.value: return
        progreso.visible = True
        page.update()

        try:
            # 1. Busca en tiempo real
            busqueda = tavily.search(query=campo_texto.value, search_depth="advanced")
            contexto = "\n".join([r['content'] for r in busqueda['results']])
            
            # 2. Llama a Llama 3.3 para resumir
            prompt = f"INFO WEB 2026: {contexto}\n\nPregunta: {campo_texto.value}"
            res = client_groq.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": "Eres un asistente de 2026. Resume info web de forma clara."},
                          {"role": "user", "content": prompt}]
            )
            campo_texto.value = res.choices[0].message.content
        except Exception as ex:
            print(f"Error IA: {ex}")
        
        progreso.visible = False
        page.update()

    # --- FUNCIÓN: GUARDAR EN LA NUBE (KOYEB) ---
    def guardar_tarea(e):
        if not campo_texto.value: return
        nueva_tarea = {
            "titulo": campo_texto.value[:50], # Toma los primeros 50 caracteres como título
            "fecha_limite": "2026-01-23",
            "estado": "pendiente"
        }
        try:
            requests.post(URL_API, json=nueva_tarea)
            campo_texto.value = "✅ ¡Guardado en la nube!"
            page.update()
        except:
            campo_texto.value = "❌ Error al guardar"
        page.update()

    # --- INTERFAZ ---
    progreso = ft.ProgressBar(visible=False, color="blue")
    campo_texto = ft.TextField(label="Escribe una tarea o pregunta...", multiline=True, expand=True)

    page.add(
        ft.Text("🚀 Agente Inteligente 2026", size=26, weight="bold"),
        ft.Row([campo_texto]),
        progreso,
        ft.Row([
            ft.ElevatedButton("🔍 Investigar con IA", icon=ft.Icons.LANGUAGE, on_click=investigar_con_ia, bgcolor="blue", color="white"),
            ft.ElevatedButton("💾 Guardar Tarea", icon=ft.Icons.SAVE, on_click=guardar_tarea, bgcolor="green", color="white"),
        ], alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(),
        ft.Text("Powered by Llama 3.3 & Tavily", size=10, color="gray")
    )

ft.app(target=main)import flet as ft
import requests

def main(page: ft.Page):
    # Configuración de la ventana
    page.title = "Mi Agenda 2026"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 400
    page.window_height = 600
    
    # URL de tu servidor en Koyeb
    URL_API = "https://neutral-opossum-pruebaapk-bc9cecf4.koyeb.app/tareas/"

    # --- FUNCIONES ---
    def agregar_tarea(e):
        if campo_texto.value == "": return
        
        # Enviamos la tarea a la nube
        try:
            nueva_tarea = {
                "titulo": campo_texto.value,
                "fecha_limite": "2026-01-23",
                "estado": "pendiente"
            }
            requests.post(URL_API, json=nueva_tarea)
            campo_texto.value = ""
            actualizar_lista()
        except Exception as ex:
            print(f"Error al guardar: {ex}")

    def actualizar_lista(e=None):
        try:
            res = requests.get(URL_API)
            lista_vista.controls.clear()
            # Mostramos las tareas que vienen de la base de datos
            for tarea in res.json():
                lista_vista.controls.append(
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.CIRCLE_OUTLINED),
                        title=ft.Text(tarea['titulo']),
                        subtitle=ft.Text("📅 Pendiente")
                    )
                )
            page.update()
        except Exception as ex:
            print(f"Error al cargar: {ex}")

    # --- ELEMENTOS VISUALES ---
    campo_texto = ft.TextField(
        label="Escribe una tarea...",
        expand=True,
        on_submit=agregar_tarea
    )
    
    boton_add = ft.FloatingActionButton(
        icon=ft.Icons.ADD, 
        on_click=agregar_tarea,
        bgcolor=ft.Colors.BLUE_400
    )
    
    lista_vista = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True)

    # --- DISEÑO DE LA PANTALLA ---
    page.add(
        ft.Text("📅 Mis Tareas 2026", size=28, weight="bold", color=ft.Colors.BLUE_200),
        ft.Row([campo_texto]),
        ft.Divider(height=20, color="transparent"),
        lista_vista
    )
    
    page.floating_action_button = boton_add

    # Cargar tareas al iniciar
    actualizar_lista()

# Comando para ejecutar la aplicación
if __name__ == "__main__":

    ft.app(target=main)
