import flet as ft
from core.ia import investigar
from core.microfono import escuchar
from core.camara import capturar
from core.calendario import mostrar_calendario

def main(page: ft.Page):
    page.title = "SISTEMA IA 2026"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 20

    campo = ft.TextField(label="¿Qué deseas investigar?", expand=True)
    resultado = ft.Text("", selectable=True)
    progreso = ft.ProgressBar(visible=False)

    def ejecutar(e):
        if not campo.value:
            resultado.value = "⚠️ Ingresa una pregunta."
        else:
            progreso.visible = True
            resultado.value = "🔍 Procesando..."
            page.update()
            try:
                resultado.value = investigar(campo.value)
            except Exception as err:
                resultado.value = f"❌ Error: {err}"
            progreso.visible = False
        page.update()

    def usar_microfono(e):
        try:
            campo.value = escuchar()
            page.update()
        except Exception as err:
            resultado.value = f"🎙️ Error de micrófono: {err}"
            page.update()

    def usar_camara(e):
        try:
            capturar()
            resultado.value = "📷 Imagen capturada como captura.jpg"
            page.update()
        except Exception as err:
            resultado.value = f"📷 Error de cámara: {err}"
            page.update()

    boton_buscar = ft.ElevatedButton("INICIAR INVESTIGACIÓN", icon=ft.icons.SEARCH, on_click=ejecutar)
    boton_microfono = ft.IconButton(icon=ft.icons.MIC, tooltip="Usar voz", on_click=usar_microfono)
    boton_camara = ft.IconButton(icon=ft.icons.CAMERA_ALT, tooltip="Capturar imagen", on_click=usar_camara)
    boton_calendario = mostrar_calendario(page)

    page.add(
        ft.Row([campo, boton_microfono]),
        boton_buscar,
        progreso,
        resultado,
        ft.Divider(),
        ft.Row([boton_camara, boton_calendario])
    )

ft.app(target=main)
