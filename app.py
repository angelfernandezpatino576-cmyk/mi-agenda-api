import flet as ft
import pyttsx3

# Simulación: variable que indica si el asistente se inició fuera del APK
# En producción, esto se puede detectar con flags o configuración del sistema
INICIADO_FUERA_APK = True  

def hablar(texto):
    if INICIADO_FUERA_APK:  # Solo activa voz si está fuera del APK
        engine = pyttsx3.init()
        engine.setProperty("rate", 150)
        engine.setProperty("volume", 0.9)
        engine.say(texto)
        engine.runAndWait()

def main(page: ft.Page):
    page.title = "Asistente Inteligente"
    page.theme_mode = ft.ThemeMode.DARK

    # Paleta premium
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary="#10B981",       # Verde esmeralda
            secondary="#374151",     # Gris oscuro
            background="#1A1A1A",    # Negro suave
            surface="#1A1A1A",
            on_primary="#FFFFFF",
            on_secondary="#FFFFFF",
            on_background="#FFFFFF",
            on_surface="#FFFFFF",
        )
    )

    titulo = ft.Text("🤖 SISTEMA IA 2026", size=22, weight="bold", color="#FBBF24")
    campo = ft.TextField(label="Haz tu pregunta...", expand=True)
    resultado = ft.Text("", selectable=True)

    def ejecutar(e):
        if campo.value.startswith("/investigar "):
            pregunta = campo.value.replace("/investigar ", "")
            respuesta = f"📚 Resultado de investigación sobre: {pregunta}"
            resultado.value = respuesta
            hablar(respuesta)
        else:
            resultado.value = "❗ Usa el comando /investigar seguido de tu pregunta."
        page.update()

    boton_buscar = ft.ElevatedButton("INICIAR INVESTIGACIÓN", icon=ft.icons.SEARCH, on_click=ejecutar)
    boton_microfono = ft.IconButton(icon=ft.icons.MIC, tooltip="Usar voz", icon_color="#FBBF24")
    boton_camara = ft.IconButton(icon=ft.icons.CAMERA_ALT, tooltip="Capturar imagen", icon_color="#FBBF24")
    boton_calendario = ft.IconButton(icon=ft.icons.CALENDAR_MONTH, tooltip="Calendario", icon_color="#FBBF24")
    boton_tema = ft.IconButton(icon=ft.icons.BRIGHTNESS_6, tooltip="Cambiar tema", icon_color="#FBBF24")

    page.add(
        ft.Row([titulo, boton_tema], alignment="spaceBetween"),
        ft.Row([campo, boton_microfono]),
        boton_buscar,
        resultado,
        ft.Divider(color="#374151"),
        ft.Row([boton_camara, boton_calendario])
    )

ft.app(target=main)
