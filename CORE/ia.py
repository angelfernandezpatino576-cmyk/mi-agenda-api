import requests
from groq import Groq

# Llaves maestras
LLAVE_GROQ = "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"
LLAVE_TAVILY = "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"

def investigar(pregunta):
    try:
        # Búsqueda directa vía API (Evita el error de tiktoken)
        url_tavily = "https://api.tavily.com/search"
        data_busqueda = {
            "api_key": LLAVE_TAVILY,
            "query": pregunta,
            "search_depth": "advanced",
            "max_results": 3
        }
        
        response_web = requests.post(url_tavily, json=data_busqueda)
        resultados = response_web.json().get("results", [])
        contexto = "\n".join([r["content"] for r in resultados])

        # Procesamiento con Groq
        client_groq = Groq(api_key=LLAVE_GROQ)
        chat_completion = client_groq.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Eres el Agente 2026. Resume la información web de forma precisa."},
                {"role": "user", "content": f"Contexto: {contexto}\n\nPregunta: {pregunta}"}
            ]
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error en el núcleo de IA: {str(e)}"
