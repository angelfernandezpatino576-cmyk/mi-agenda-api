import flet as ft

def activar_escucha(page: ft.Page):
    # En un servidor en la nube, usamos el SpeechToText del cliente
    stt = ft.SpeechToText()
    page.overlay.append(stt)
    
    def on_result(e):
        print(f"Escuchado: {e.result}")
    
    stt.on_result = on_result
    stt.start()
    return "Escuchando..."
