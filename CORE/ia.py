from groq import Groq
from tavily import TavilyClient

LLAVE_GROQ = "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"
LLAVE_TAVILY = "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"

def investigar(pregunta):
    client_groq = Groq(api_key=LLAVE_GROQ)
    tavily = TavilyClient(api_key=LLAVE_TAVILY)

    busqueda = tavily.search(query=pregunta)
    contexto = "\n".join([r["content"] for r in busqueda["results"]])

    respuesta = client_groq.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Eres un asistente de investigación avanzado."},
            {"role": "user", "content": f"Contexto: {contexto}\n\nPregunta: {pregunta}"}
        ]
    )

    return respuesta.choices[0].message.content
