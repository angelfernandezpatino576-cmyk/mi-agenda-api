import flet as ft
import os

# Importaciones protegidas del CORE
try:
    from CORE.ia import investigar
    from CORE.camara import activar_camara
    from CORE.calendario import mostrar_calendario
    from CORE.microfono import activar_escucha
except ImportError as e:
    print(f"Error importando módulos: {e}")

async def main(page: ft.Page):
    # Configuración Visual
    page.title = "Agente 2026"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0F172A"
    page.padding = 20
    
    # Manejador de Permisos
    ph = ft.PermissionHandler()
    page.overlay.append(ph)

    # Área de Chat
    chat_display = ft.Column(expand=True, scroll=ft.ScrollMode.ALWAYS, spacing=10)

    # Función Principal
    async def procesar(e):
        texto = input_field.value
        if not texto: return
        
        # Mostrar mensaje usuario
        chat_display.controls.append(
            ft.Container(content=ft.Text(f"Tú: {texto}"), alignment=ft.alignment.center_right, padding=10, bgcolor="#1E293B", border_radius=10)
        )
        input_field.value = ""
        
        loader = ft.Text("Analizando...", italic=True, color="grey")
        chat_display.controls.append(loader)
        page.update()

        # Llamada a IA
        try:
            respuesta = investigar(texto)
            chat_display.controls.remove(loader)
            chat_display.controls.append(
                ft.Container(content=ft.Text(f"Agente: {respuesta}"), alignment=ft.alignment.center_left, padding=10, bgcolor="#38BDF8", border_radius=10)
            )
        except Exception as ex:
            chat_display.controls.remove(loader)
            chat_display.controls.append(ft.Text(f"Error: {ex}", color="red"))
        
        page.update()

    # Campo de Texto
    input_field = ft.TextField(hint_text="Escribe aquí...", expand=True, on_submit=procesar, border_radius=20, bgcolor="#1E293B")

    # Botones de Funciones (CORE)
    botones = ft.Row([
        ft.IconButton(ft.icons.MIC, on_click=lambda _: activar_escucha(page)),
        ft.IconButton(ft.icons.CAMERA_ALT, on_click=lambda _: activar_camara(page)),
        ft.IconButton(ft.icons.CALENDAR_MONTH, on_click=lambda _: mostrar_calendario(page, input_field)),
    ], alignment=ft.MainAxisAlignment.CENTER)

    # Armado de la Página
    page.add(
        ft.Container(content=ft.Text("AGENTE 2026", size=20, weight="bold", color="#38BDF8"), alignment=ft.alignment.center),
        botones,
        ft.Divider(color="grey"),
        ft.Container(content=chat_display, expand=True),
        ft.Row([input_field, ft.FloatingActionButton(icon=ft.icons.SEND, on_click=procesar)])
    )

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    ft.app(target=main, host="0.0.0.0", port=port)
