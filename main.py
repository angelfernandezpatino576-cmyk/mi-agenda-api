import flet as ft
import asyncio

async def main(page: ft.Page):
    page.title = "Agente 2026 - Servidor Local"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0F172A"
    
    chat = ft.ListView(expand=True, spacing=10, padding=20)
    
    async def enviar(e):
        if not input_txt.value: return
        msg = input_txt.value
        chat.controls.append(ft.Text(f"👤 Tú: {msg}", color="#38BDF8", weight="bold"))
        input_txt.value = ""
        page.update()
        
        # Simulación de respuesta
        await asyncio.sleep(0.5)
        chat.controls.append(ft.Text(f"🤖 Agente: Procesando en IP 192.168.101.2...", color="#10B981"))
        page.update()

    input_txt = ft.TextField(hint_text="Comando...", expand=True, on_submit=enviar)

    page.add(
        ft.Column([
            ft.Text("👽 AGENTE 2026", size=28, weight="bold", color="#FBBF24"),
            ft.Text("IP LOCAL: 192.168.101.2", size=10, italic=True, color="grey"),
            ft.Divider(color="#1E293B"),
            chat,
            ft.Row([input_txt, ft.IconButton(ft.icons.SEND, on_click=enviar)])
        ], expand=True)
    )

if __name__ == "__main__":
    # Usamos ft.run para evitar errores de versión
    # host="0.0.0.0" permite que el APK vea el servidor en la IP 192.168.101.2
    ft.run(
        target=main,
        view=ft.AppView.WEB_BROWSER,
        host="0.0.0.0",
        port=8550
    )
