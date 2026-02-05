import flet as ft
import socket
import asyncio

def obtener_ip_local():
    """Detecta la IP actual del teléfono automáticamente"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # No necesita conexión real, solo para identificar la interfaz activa
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

async def main(page: ft.Page):
    ip_actual = obtener_ip_local()
    
    # Configuración de la interfaz premium
    page.title = f"Agente 2026 - {ip_actual}"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0F172A"
    
    chat = ft.ListView(expand=True, spacing=10, padding=20)
    
    async def enviar(e):
        if not input_txt.value: return
        msg = input_txt.value
        chat.controls.append(ft.Text(f"👤 Tú: {msg}", color="#38BDF8", weight="bold"))
        input_txt.value = ""
        page.update()
        
        # Respuesta lógica
        await asyncio.sleep(0.3)
        chat.controls.append(ft.Text(f"🤖 Agente: Procesando en red {ip_actual}", color="#10B981"))
        page.update()

    input_txt = ft.TextField(
        hint_text="Escribe un comando...", 
        expand=True, 
        border_color="#10B981",
        on_submit=enviar
    )

    page.add(
        ft.Column([
            ft.Container(
                content=ft.Column([
                    ft.Text("👽 SISTEMA IA 2026", size=28, weight="bold", color="#FBBF24"),
                    ft.Text(f"📡 SERVIDOR ACTIVO EN: {ip_actual}:8550", size=12, color="#94A3B8", weight="bold"),
                ]),
                padding=10
            ),
            ft.Divider(color="#1E293B"),
            chat,
            ft.Row([
                input_txt, 
                ft.IconButton(icon=ft.icons.SEND_ROUNDED, icon_color="#10B981", on_click=enviar)
            ])
        ], expand=True)
    )

if __name__ == "__main__":
    # ft.run elimina el error de 'ft.app is deprecated'
    # host="0.0.0.0" hace que el servidor sea visible en toda tu red local
    ft.run(
        target=main,
        view=ft.AppView.WEB_BROWSER,
        host="0.0.0.0",
        port=8550
    )
