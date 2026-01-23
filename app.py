import flet as ft
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