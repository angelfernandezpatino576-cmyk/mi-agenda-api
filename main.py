import flet as ft
import socket
import asyncio

def obtener_ip_local():
    """Detecta la IP de tu red actual (ej. 192.168.101.2)"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

async def main(page: ft.Page):
    ip_actual = obtener_ip_local()
    page.title = "Agente 2026"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0F172A"
    
    chat = ft.ListView(expand=True, spacing=10)
    
    async def enviar(e):
        if not txt.value: return
        chat.controls.append(ft.Text(f"👤 Tú: {txt.value}", color="#38BDF8"))
        txt.value = ""
        page.update()
        
        await asyncio.sleep(0.5)
        chat.controls.append(ft.Text(f"🤖 Agente: Conectado en {ip_actual}", color="#10B981"))
        page.update()

    txt = ft.TextField(hint_text="Escribe aquí...", expand=True, on_submit=enviar)

    page.add(
        ft.Column([
            ft.Text("👽 AGENTE 2026", size=28, weight="bold", color="#FBBF24"),
            ft.Text(f"📡 Servidor en: {ip_actual}:8550", size=12, color="grey"),
            ft.Divider(),
            chat,
            ft.Row([txt, ft.IconButton(ft.icons.SEND, on_click=enviar)])
        ], expand=True)
    )

if __name__ == "__main__":
    # SOLUCIÓN AL TYPEERROR: Usamos ft.app con target explícito
    # host="0.0.0.0" permite que el APK vea el servidor en tu IP local
    ft.app(
        target=main, 
        view=ft.AppView.WEB_BROWSER, 
        host="0.0.0.0", 
        port=8550
    )
