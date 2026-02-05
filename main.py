import flet as ft
import socket
import asyncio

def obtener_ip_local():
    """Detecta la IP de tu red para que el APK sepa dónde conectarse"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # No requiere internet, solo identifica la interfaz activa (ej. 192.168.101.2)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

async def main(page: ft.Page):
    ip_actual = obtener_ip_local()
    
    # Configuración de la interfaz
    page.title = "Agente 2026"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0F172A"
    
    chat_display = ft.ListView(expand=True, spacing=10, padding=20)
    
    async def enviar_mensaje(e):
        if not input_field.value: return
        user_text = input_field.value
        chat_display.controls.append(
            ft.Text(f"👤 Tú: {user_text}", color="#38BDF8", weight="bold")
        )
        input_field.value = ""
        page.update()

        # Lógica del Agente
        await asyncio.sleep(0.5)
        chat_display.controls.append(
            ft.Text(f"🤖 Agente: Procesando en servidor {ip_actual}", color="#10B981")
        )
        page.update()

    input_field = ft.TextField(
        hint_text="Escribe un comando...",
        expand=True,
        border_color="#10B981",
        on_submit=enviar_mensaje
    )

    # Construcción de la pantalla
    page.add(
        ft.Column([
            ft.Container(
                content=ft.Column([
                    ft.Text("👽 AGENTE 2026", size=28, weight="bold", color="#FBBF24"),
                    ft.Text(f"📡 IP LOCAL: {ip_actual}:8550", size=12, color="#94A3B8"),
                ]),
                padding=10
            ),
            ft.Divider(color="#1E293B"),
            chat_display,
            ft.Row([
                input_field,
                ft.IconButton(
                    icon=ft.icons.SEND_ROUNDED,
                    icon_color="#10B981",
                    on_click=enviar_mensaje
                )
            ])
        ], expand=True)
    )

# --- EJECUCIÓN DEL SERVIDOR (LÍNEA 74 CORREGIDA) ---
if __name__ == "__main__":
    # Se añade 'target=main' para solucionar el TypeError
    # host="0.0.0.0" permite que el APK se conecte a tu IP
    ft.run(
        target=main, 
        host="0.0.0.0", 
        port=8550, 
        view=ft.AppView.WEB_BROWSER
    )
