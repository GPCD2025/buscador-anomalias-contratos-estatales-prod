from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_ollama import OllamaLLM
import uvicorn
import re

# Inicializar FastAPI
app = FastAPI()
print("FastAPI iniciado")



# Función para limpiar la respuesta
def limpiar_respuesta(respuesta):
    # Eliminar todo lo que está dentro de las etiquetas <think> y </think>
    respuesta_limpia = re.sub(r'<think>.*?</think>', '', respuesta, flags=re.DOTALL)
    
    # Eliminar los backticks del bloque de código markdown (```json ... ```)
    respuesta_limpia = re.sub(r'```json|```', '', respuesta_limpia)
    
    # Eliminar espacios en blanco adicionales
    return respuesta_limpia.strip()

# Definir el modelo de solicitud
class RequestModel(BaseModel):
    prompt: str

# Configurar el modelo Ollama
model = OllamaLLM(model="deepseek-r1:8b")

@app.post("/generate")
async def generate_text(request: RequestModel):
    try:
        print(f"Prompt: {request.prompt}")
        result = model.invoke(request.prompt)
        result = limpiar_respuesta(result)
        return {"response": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

if __name__ == "__main__":
    print("Iniciando servidor...")
    uvicorn.run(app, host="0.0.0.0", port=8123)
