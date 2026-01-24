import speech_recognition as sr

def escuchar():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        return r.recognize_google(audio, language="es-ES")