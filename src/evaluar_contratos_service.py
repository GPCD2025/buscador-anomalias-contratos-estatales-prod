import requests
import time
from insert_data import (get_actividades_from_contrato,
                         save_coherencia, get_next_contrato_from_db, update_estado_contrato)

class ContratoService:
  def __init__(self):       
    estados = {}
    estados['procesando'] = 'pro'
    estados['finalizado'] = 'fin'
    estados['error'] = 'err' 
  
  def create_prompt(self, contrato):
    descripcion_contrato = f"""[{contrato['descripcion_del_procedimiento']}] - [{contrato['nombre_del_procedimiento']}] - [{contrato['modalidad_de_contratacion']}] - [{contrato['justificacion_modalidad_de_contratacion']}]"""
    prompt = f"""
            Instrucciones:
            Eres un sistema experto en validación de contratos. Debes evaluar si la descripción del contrato es coherente con las actividades económicas del contratante.

            Entrada:

            Descripción del contrato: {descripcion_contrato}
            Lista de actividades económicas del contratante: {contrato['actividades']}

            Salida esperada:
            "Verdadero" si la descripción del contrato está alineada con al menos una de las actividades económicas.
            "Falso" si no hay relación entre la descripción del contrato y las actividades económicas.

            Si la respuesta es "Falso", proporciona una de las siguientes categorias que explique la razón de la incompatibilidad.

            Categorías de Falta de Relación:

            1. Actividad no relacionada con el objeto del contrato → Ninguna de las actividades económicas coincide con el objeto del contrato.
            2. Actividades insuficientes para cumplir el contrato → Las actividades económicas están relacionadas, pero no son suficientes para ejecutar el contrato.
            3. Requiere habilitación especial no presente → El contrato necesita certificaciones, permisos o características que no se encuentran en las actividades económicas.
            4. Sector no alineado con el contrato → El contrato pertenece a un sector regulado o especializado distinto al de las actividades económicas.

            Ejemplo de salida posibles:

            Falso - Actividad no relacionada con el objeto del contrato
            Falso - Actividades insuficientes para cumplir el contrato
            Falso - Requiere habilitación especial no presente
            Falso - Sector no alineado con el contrato
            Verdadero - 

            Responde SOLAMENTE en el siguiente formato:
            [Verdadero/Falso] - [Categoría (solo si es Falso)]"""
    return prompt


  def execute_prompt(self, prompt, empresa_id):
      url = "http://127.0.0.1:8123/generate" 
      payload = {"prompt": prompt}
      
      try:
          start_time = time.time()  
          response = requests.post(url, json=payload)
          end_time = time.time() 
          
          response.raise_for_status()  
          respuesta = response.json().get("response", "No response received")
          
          tiempo_respuesta = end_time - start_time  
          print(f"✅ Respuesta recibida en {tiempo_respuesta:.2f} segundos") 
          print(f"-------------------------------------------------------------------")
          print(f"Respuesta generada para la empresa {empresa_id}---> {respuesta}")
          print(f"-------------------------------------------------------------------")
          
          return respuesta
      except requests.exceptions.RequestException as e:
          print(f"❌ Error en la solicitud: {e}")
          return None


  def execute_prompts(self):
      while True:
          contrato = get_next_contrato_from_db() 
          actividades = get_actividades_from_contrato(contrato['empresa_id'])
          contrato['actividades'] = actividades
          contrato['prompt'] = self.create_prompt(contrato)
          contrato['resultado'] = self.execute_prompt(
              prompt=contrato['prompt'], empresa_id=contrato['empresa_id'])
          save_coherencia(contrato)
          update_estado_contrato(
              contrato_id=contrato['id'],
              prompt=contrato['prompt'])
          print(f"contrato gestionado {contrato['id']}")


  def principal(self):
      # ejecuta los prompts uno por uno
      self.execute_prompts()

if __name__ == "__main__":
  print("Iniciando proceso de evaluación de contratos...")
  contratoService = ContratoService()
  contratoService.principal()
  print("Proceso finalizado.")
  
  