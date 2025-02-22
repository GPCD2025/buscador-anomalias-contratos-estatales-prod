import requests
import time
from insert_data import get_contratos, get_actividades_from_contrato, save_prompts, save_coherencias, clean_coherencias

class ContratoService:
  def __init__(self):       
    estados = {}
    estados['procesando'] = 'pro'
    estados['finalizado'] = 'fin'
    estados['error'] = 'err' 
  
  def add_actividades_to_contratos(self, contratos):
    for contrato in self.contratos:
      actividades = get_actividades_from_contrato(contrato['empresa_id'])
      contrato['actividades'] = actividades
    return contratos

  def create_prompts(self, contratos):
    prompts = []
    for contrato in contratos:
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
        
      contrato['prompt'] = prompt
      prompts.append(prompt)
    return contratos
 

  def get_coherencia(self, contratos):
    for contrato in contratos:
      contrato['resultado'] = self.execute_prompt(contrato['prompt'], empresa_id=contrato['empresa_id'])
      save_coherencias([contrato])
    return contratos


  def principal(self):
    self.contratos = get_contratos()
    self.contratos = self.add_actividades_to_contratos(self.contratos)
    self.contratos = self.create_prompts(self.contratos)
    # GUARDA LOS PROMPTS EN LOS CONTRATOS (comentarear cuando ya esté guardado)
    save_prompts(self.contratos)
    print("Prompts guardados")
    clean_coherencias()
    start_time = time.time()  
    self.contratos = self.get_coherencia(self.contratos)
    end_time = time.time() 
    print(f"✅ Respuestas recibidas en {end_time - start_time:.2f} segundos")
  

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
 
if __name__ == "__main__":
  print("Iniciando proceso de evaluación de contratos...")
  contratoService = ContratoService()
  contratoService.principal()
  print("Proceso finalizado.")
  
  