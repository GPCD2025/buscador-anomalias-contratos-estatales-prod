import requests
import time
from insert_data import get_contratos, get_actividades_from_contrato, save_prompts, save_coherencias

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
      prompt = f"""
        Dado el siguiente registro, analiza la coherencia entre la descripción del objeto contractual y las actividades económicas declaradas de la empresa. ¿Existen discrepancias semánticas o conceptuales que sugieran que el contrato no se ajusta a la actividad económica reportada?
        Registro:

        fin del Contrato: {contrato['descripcion_del_procedimiento']} - {contrato['nombre_del_procedimiento']}
        - {contrato['modalidad_de_contratacion']} - {contrato['justificacion_modalidad_de_contratacion']}
        Actividades económicas: {contrato['actividades']}
        Salida esperada:
        Nivel de coherencia (por ejemplo, score de similitud).
        Comentarios sobre discrepancias detectadas.
        Recomendación de alerta (Sí/No) y justificación."
        Prompt 2: Evaluación del Valor del Contrato en Función del Sector"""
      contrato['prompt'] = prompt
    return contratos
 

  def get_coherencia(self, contratos):
    for contrato in contratos:
      contrato['resultado'] = self.execute_prompt(contrato['prompt'])
    return contratos


  def principal(self):
    self.contratos = get_contratos()
    self.contratos = self.add_actividades_to_contratos(self.contratos)
    self.contratos = self.create_prompts(self.contratos)
    # GUARDA LOS PROMPTS EN LOS CONTRATOS (comentarear cuando ya esté guardado)
    save_prompts(self.contratos)
    self.contratos = self.get_coherencia(self.contratos)
    save_coherencias(self.contratos)
  

  def execute_prompt(self, prompt):     
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

          return respuesta
      except requests.exceptions.RequestException as e:
          print(f"❌ Error en la solicitud: {e}")
          return None
 
if __name__ == "__main__":
  print("Iniciando proceso de evaluación de contratos...")
  contratoService = ContratoService()
  contratoService.principal()
  print("Proceso finalizado.")
  
  