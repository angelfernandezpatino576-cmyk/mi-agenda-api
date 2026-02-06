import os
from groq import Groq
from tavily import TavilyClient

# Llaves integradas
GROQ_KEY = "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"
TAVILY_KEY = "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"

client_ai = Groq(api_key=GROQ_KEY)
tavily = TavilyClient(api_key=TAVILY_KEY)

def investigar(pregunta):
    try:
        # Búsqueda avanzada
        search = tavily.search(query=pregunta, search_depth="advanced", max_results=2)
        contexto = search['results']

        # Procesamiento con Llama 3
        response = client_ai.chat.completions.create(
            messages=[
                {"role": "system", "content": "Eres el Agente 2026. Responde de forma clara usando el contexto web."},
                {"role": "user", "content": f"Contexto: {contexto}\n\nPregunta: {pregunta}"}
            ],
            model="llama3-8b-8192",
        )
        # RETORNAMOS el texto para que main.py lo reciba
        return response.choices[0].message.content
    except Exception as e:
        return f"Error en IA: {str(e)}"
