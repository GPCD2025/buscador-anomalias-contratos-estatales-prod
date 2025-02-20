from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_ollama import OllamaLLM
import uvicorn
import re
import time

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
        print(f"Prompt recibido: {request.prompt}")

        start_time = time.time()  # ⏱️ Inicia el cronómetro
        result = model.invoke(request.prompt)
        end_time = time.time()  # ⏱️ Finaliza el cronómetro
        
        result = limpiar_respuesta(result)
        tiempo_respuesta = end_time - start_time  # ⏱️ Calcula el tiempo de respuesta
        
        print(f"✅ Respuesta generada en {tiempo_respuesta:.2f} segundos")  # ⏱️ Imprime el tiempo

        return {
            "response": result,
            "execution_time": f"{tiempo_respuesta:.2f} segundos"  # 🔹 Devolvemos el tiempo también en la respuesta
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

if __name__ == "__main__":
    print("Iniciando servidor...")
    uvicorn.run(app, host="0.0.0.0", port=8123)
