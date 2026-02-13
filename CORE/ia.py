import requests
from groq import Groq

# Configuración de Llaves
LLAVE_GROQ = "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"
LLAVE_TAVILY = "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"

def investigar(pregunta):
    try:
        # 1. Búsqueda Web Directa (Sin librería pesada)
        url = "https://api.tavily.com/search"
        payload = {
            "api_key": LLAVE_TAVILY,
            "query": pregunta,
            "search_depth": "advanced",
            "max_results": 2
        }
        resp = requests.post(url, json=payload)
        data = resp.json()
        
        contexto = ""
        if "results" in data:
            for r in data["results"]:
                contexto += f"- {r['content']}\n"
        
        # 2. Razonamiento con Groq
        client = Groq(api_key=LLAVE_GROQ)
        chat = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Eres el Agente 2026. Responde brevemente usando este contexto web."},
                {"role": "user", "content": f"Contexto: {contexto}\n\nPregunta: {pregunta}"}
            ]
        )
        return chat.choices[0].message.content

    except Exception as e:
        return f"Error en IA: {str(e)}"
