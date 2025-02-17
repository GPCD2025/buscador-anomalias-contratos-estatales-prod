import concurrent.futures
import time
import requests
import zipfile
from tqdm import tqdm  # Para mostrar la barra de progreso
import pandas as pd
import re
from rues_web_scrapping import RUESScraper
from insert_data import procesar_datos, obtener_contratos_procesados
from particion_archivo_service import crear_consecutivo, asignar_grupos, cargar_mi_grupo, obtener_asignacion_grupos
import json 

def descargar_zip(url):
    print(f"Descargando archivo {url}...")

    # Hacer una solicitud con streaming para no cargar todo el archivo en memoria
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Lanza un error si hay problemas con la descarga

    # Obtener el tamaño total del archivo
    total_size = int(response.headers.get('content-length', 0))
    nombre_archivo = url.split("/")[-1]

    # Descargar en chunks y mostrar progreso
    with open(nombre_archivo, 'wb') as file, tqdm(
        desc=nombre_archivo,
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
                bar.update(len(chunk))  # Actualiza la barra de progreso

    return f"./{nombre_archivo}"

  
def descomprimir_zip(archivo):
    print(f"Descomprimiendo archivo {archivo}...")
    # Descomprimir archivo 
    with zipfile.ZipFile(archivo, 'r') as zip_ref:
        zip_ref.extractall("./")
        
    print("Archivo descomprimido.")

def procesar_archivo_csv(archivo):
    print(f"Procesando archivo {archivo}...")
    
    # Procesar archivo CSV
    df = pd.read_csv(archivo)
    
    print(df.shape)
    print("dataframe filtrado por fecha")
    df  = df[(df['Fecha de Publicacion del Proceso'] >= '01-01-2024') & (df['Fecha de Publicacion del Proceso'] <= '08-02-2025')]
    
    print(df.shape)
    print("dataframe filtrado por ciudad")
    df = df[df['Ciudad Entidad'] == 'Bogotá'] 
    
    print(df.shape)
    print("dataframe filtrado por NIT")
    df = df.dropna(subset=['NIT del Proveedor Adjudicado'])
     
    print(df.shape)
    print("Filtrar por NIT válido")
    nit_regex_completo = re.compile(r"^(8|9)\d{8,9}(-\d)?$|^(8|9)\d{2}(\.\d{3}){2}(-\d)?$")
    df = df[df['NIT del Proveedor Adjudicado'].str.match(nit_regex_completo)]
    
    print(df.shape)
    print("Limpiar caracteres especiales")
    df = df.select_dtypes(include=['object'])
    df = df.apply(lambda x: x.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8'))
    print(df.head(3))
     
    print(df.shape)
    print("Archivo procesado.")   
    
    df.to_csv("procesado.csv", index=False)
    
    return df 

def obtener_formacion_rues(nit):
    print("Obteniendo formación RUES...")
    scraper = RUESScraper()
    
    print("Iniciando proceso de extracción de información RUES...")
    scraper.cargar_pagina()
    time.sleep(3)
    print("obtener_informacion")
    scraper.obtener_informacion(nit)
    time.sleep(1)
    print("cargar_empresa")
    empresaExiste = scraper.cargar_empresa()

    if empresaExiste:
        time.sleep(1)
        print("redirigir_detalle_empresa")
        scraper.redirigir_detalle_empresa()
        time.sleep(2)
        print("llenar_campos_finales")
        scraper.llenar_campos_finales() 
        print("extraer_informacion_general")
        scraper.extraer_actividades_economicas() 
        scraper.extraer_representantes_legales()
        print("obtener_informacion_completa")
        informacion_rues = scraper.obtener_informacion_completa()
        scraper.cerrar_pagina()
        print("Formación RUES obtenida.")
        return informacion_rues    
    else:
        scraper.cerrar_pagina()
        return None

def insertar_datos_recolectados(contratos):
    print("Insertando datos recolectados...")
    
    procesar_datos(contratos)

def filtrar_contratos_procesados():
    print("Filtrando contratos procesados...")
    return obtener_contratos_procesados()


def procesar_fila(row, nombre_estudiante):
    """
    Procesa una fila del DataFrame, obteniendo la formación RUES y estructurando el resultado.
    """
    try:
        start_time_ciclo = time.time()
        nit = row['NIT del Proveedor Adjudicado']
        print(f"🔍 Procesando NIT: {nit}")
        
        formacion_rues = obtener_formacion_rues(nit)
        if formacion_rues is not None:
            registro = {
                'nit': nit,
                'nombre_estudiante': nombre_estudiante,
                'ID del Proceso': row['ID del Proceso'],
                'Nombre del Procedimiento': row['Nombre del Procedimiento'],
                'Descripción del Procedimiento': row['Descripción del Procedimiento'],
                'Modalidad de Contratacion': row['Modalidad de Contratacion'],
                'Justificación Modalidad de Contratación': row['Justificación Modalidad de Contratación'],
                'formacion_rues': formacion_rues
            }
            insertar_datos_recolectados([registro])  # Guardar en BD
            print(f"✅ Procesado en {time.time() - start_time_ciclo:.2f} segundos")
            return registro  # Devolver el resultado procesado

        print(f"⚠️ NIT {nit} no encontrado")
        return None
    except Exception as e:
        print(f"❌ Error procesando {row['NIT del Proveedor Adjudicado']}: {e}")
        return None

def procesar_en_paralelo(df, nombre_estudiante, max_workers=4):
    """
    Procesa el DataFrame en paralelo usando hilos.
    """
    contratos = []
    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Ejecutar tareas en paralelo
        futures = {executor.submit(procesar_fila, row, nombre_estudiante): row for _, row in df.iterrows()}
        
        for future in concurrent.futures.as_completed(futures):
            resultado = future.result()
            if resultado:
                contratos.append(resultado)

    print(f"🔹 Procesamiento completo en {time.time() - start_time:.2f} segundos")
    return contratos  # Devuelve la lista de contratos procesados

  
if __name__ == "__main__":
    yaFueDescargado = True
    yaFueDescomprimido = True
    yaFueProcesado = True
    yaFueScrapeado = False
    nombre_estudiante = input("Ingrese su nombre: ").strip()
    
    print("Iniciando proceso...")
    url="https://nuelgaloproductos.s3.us-east-1.amazonaws.com/uploads/SECOP_II_-_Procesos_de_Contrataci_n_20250208.zip" 
    if yaFueDescargado:
        path = "SECOP_II_-_Procesos_de_Contrataci_n_20250208.zip"
    else:
        path = descargar_zip(url)
       
    print("\nDescarga completada.")
    
    if not yaFueDescomprimido:
        descomprimir_zip(path)  
    
    print("Archivo ya descomprimido")
    csv_file = path.split('.')[0]+".csv"     
     
    print(f"Archivo {csv_file} descargado")
    
    if not yaFueProcesado:
        df = procesar_archivo_csv(csv_file)
    else:
        df = pd.read_csv("procesado.csv")
    
    print(df.shape) 
    
    grupos_existentes = obtener_asignacion_grupos()
    
    if(len(grupos_existentes) == 0): 
        df = asignar_grupos(df)
    else:
        df = crear_consecutivo(df)
    
    df = cargar_mi_grupo(nombre_estudiante, df)
    
    contratos_procesados = filtrar_contratos_procesados()
    
    print(df.shape) 
    df = df[~df["ID del Proceso"].isin(contratos_procesados)]
     
    print(df.shape) 
    
    dftest = df.head(1000)
    
    contratos = []
    cont =0
    if not yaFueScrapeado:
        start_time = time.time()
      
        # Procesar en paralelo
        contratos = procesar_en_paralelo(dftest, nombre_estudiante, max_workers=2)
        
        # Guardar resultados en JSON
        with open('contratos.json', 'w', encoding="utf-8") as file:
            json.dump(contratos, file, indent=2, ensure_ascii=False)

        print(f"📝 Se guardaron {len(contratos)} contratos en contratos.json")
            
        #convertir la variable contratos en un json y despues imprimir el json
        
        print(contratos.count)
        json = json.dumps(contratos, indent=2)
        
        #salvar json en el disco
        with open('contratos.json', 'w', encoding="utf-8") as file:
            file.write(json)
        
        print(f"Tiempo de ejecución total: {time.time() - start_time} segundos")
    else: 
        # Leer archivo JSON asegurando codificación correcta
        with open("contratos.json", "r", encoding="utf-8") as f:
            raw_data = f.read()

        # Decodificar caracteres especiales correctamente
        contratos = json.loads(raw_data)
 
    
