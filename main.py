import flet as ft
import socket
import asyncio

def obtener_ip_local():
    """Detecta la IP actual del teléfono para que el APK sepa a dónde conectar"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # No requiere internet real, solo identifica la interfaz de red activa
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

async def main(page: ft.Page):
    ip_actual = obtener_ip_local()
    
    # Configuración de la interfaz visual
    page.title = "Agente 2026 - Servidor Local"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0F172A"
    page.window_width = 400
    page.window_height = 800
    
    chat = ft.ListView(expand=True, spacing=10, padding=20)
    
    async def enviar_mensaje(e):
        if not input_txt.value: return
        user_msg = input_txt.value
        chat.controls.append(ft.Text(f"👤 Tú: {user_msg}", color="#38BDF8", weight="bold"))
        input_txt.value = ""
        page.update()
        
        # Simulación de respuesta de la IA
        await asyncio.sleep(0.5)
        chat.controls.append(ft.Text(f"🤖 Agente: Procesando comando en {ip_actual}", color="#10B981"))
        page.update()

    input_txt = ft.TextField(
        hint_text="Escribe un comando...",
        expand=True,
        border_color="#10B981",
        on_submit=enviar_mensaje
    )

    page.add(
        ft.Column([
            ft.Container(
                content=ft.Column([
                    ft.Text("👽 AGENTE 2026", size=28, weight="bold", color="#FBBF24"),
                    ft.Text(f"📡 RED: {ip_actual}:8550", size=12, color="#94A3B8"),
                ]),
                padding=10
            ),
            ft.Divider(color="#1E293B"),
            chat,
            ft.Row([
                input_txt,
                ft.IconButton(
                    icon=ft.icons.SEND_ROUNDED,
                    icon_color="#10B981",
                    on_click=enviar_mensaje
                )
            ])
        ], expand=True)
    )

if __name__ == "__main__":
    # CORRECCIÓN CRÍTICA: Se añade 'target=main' para evitar el TypeError
    # host="0.0.0.0" permite que el APK vea el servidor en tu red local
    ft.run(
        target=main, 
        view=ft.AppView.WEB_BROWSER, 
        host="0.0.0.0", 
        port=8550
    )
