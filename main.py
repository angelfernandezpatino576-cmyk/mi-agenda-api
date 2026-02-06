import flet as ft
import os
import asyncio

# ==========================================================
# IMPORTACIÓN DE MÓDULOS DEL NÚCLEO (CORE)
# ==========================================================
try:
    from CORE.ia import investigar
    from CORE.camara import abrir_camara
    from CORE.calendario import seleccionar_fecha
    from CORE.microfono import activar_escucha
except ImportError as e:
    print(f"⚠️ Error al importar módulos de CORE: {e}")

async def main(page: ft.Page):
    # --- CONFIGURACIÓN DE PÁGINA ---
    page.title = "Agente 2026 - Central de Comando"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0F172A"
    page.window_width = 450
    page.window_height = 800
    page.padding = 0
    
    # Manejador de Permisos (Crítico para Android)
    ph = ft.PermissionHandler()
    page.overlay.append(ph)

    # Contenedor de Chat
    chat_display = ft.Column(expand=True, scroll=ft.ScrollMode.ALWAYS, spacing=15)

    # --- LÓGICA DE PROCESAMIENTO ---
    async def enviar_mensaje(e):
        texto = input_field.value
        if not texto: return
        
        # UI: Usuario
        chat_display.controls.append(
            ft.Container(
                content=ft.Text(texto, color="white"),
                alignment=ft.alignment.center_right,
                padding=12, bgcolor="#1E293B", border_radius=15
            )
        )
        input_field.value = ""
        
        # UI: Indicador de carga
        loader = ft.Row([ft.ProgressRing(width=14, height=14), ft.Text(" Agente pensando...", size=12)], alignment="center")
        chat_display.controls.append(loader)
        page.update()

        try:
            # LLAMADA AL CORE DE IA (Groq + Tavily)
            # Esta función está en CORE/ia.py
            respuesta = investigar(texto)
            
            chat_display.controls.remove(loader)
            chat_display.controls.append(
                ft.Container(
                    content=ft.Text(respuesta, color="white"),
                    alignment=ft.alignment.center_left,
                    padding=12, bgcolor="#38BDF8", border_radius=15
                )
            )
        except Exception as ex:
            chat_display.controls.remove(loader)
            chat_display.controls.append(ft.Text(f"Error de sistema: {str(ex)}", color="red", size=10))
        
        page.update()

    # --- ELEMENTOS DE INTERFAZ ---
    input_field = ft.TextField(
        hint_text="Escribe o usa los botones...",
        expand=True,
        border_radius=25,
        bgcolor="#1E293B",
        on_submit=enviar_mensaje,
        content_padding=15
    )

    # Cabecera con botones de hardware vinculados a CORE
    header = ft.Container(
        padding=15,
        bgcolor="#1E293B",
        content=ft.Row([
            ft.Text("AGENTE 2026", weight="bold", size=20, color="#38BDF8"),
            ft.Row([
                ft.IconButton(
                    icon=ft.icons.MIC_ROUNDED, 
                    icon_color="#38BDF8",
                    on_click=lambda _: activar_escucha(page) # Llama a CORE/microfono.py
                ),
                ft.IconButton(
                    icon=ft.icons.CAMERA_ALT_ROUNDED, 
                    icon_color="#38BDF8",
                    on_click=lambda _: abrir_camara(page) # Llama a CORE/camara.py
                ),
                ft.IconButton(
                    icon=ft.icons.CALENDAR_MONTH_ROUNDED, 
                    icon_color="#38BDF8",
                    on_click=lambda _: seleccionar_fecha(page, input_field) # Llama a CORE/calendario.py
                ),
            ])
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    )

    # --- COMPOSICIÓN FINAL ---
    page.add(
        header,
        ft.Container(
            content=chat_display,
            expand=True,
            padding=20
        ),
        ft.Container(
            padding=15,
            content=ft.Row([
                input_field,
                ft.FloatingActionButton(icon=ft.icons.SEND_ROUNDED, on_click=enviar_mensaje, bgcolor="#38BDF8")
            ])
        )
    )
    page.update()

# --- ARRANQUE COMPATIBLE CON KOYEB ---
if __name__ == "__main__":
    # El puerto lo asigna la nube automáticamente
    port = int(os.getenv("PORT", 8080))
    ft.app(
        target=main, 
        host="0.0.0.0", 
        port=port,
        view=None # Importante para que no intente abrir navegador en el servidor
    )
