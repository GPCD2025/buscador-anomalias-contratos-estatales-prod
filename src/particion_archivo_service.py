
import pandas as pd 
from insert_data import guardar_asignacion_grupos, obtener_asignacion_grupos

def crear_consecutivo(df):
    """
    Agrega un consecutivo único al DataFrame.
    """
    df = df.copy()
    df["ID_Consecutivo"] = range(1, len(df) + 1)  # Crear un consecutivo único
    return df

def asignar_grupos(df, num_grupos=4):
    """
    Divide el DataFrame en `num_grupos` partes y guarda la asignación de rangos en la base de datos.
    """
    df = crear_consecutivo(df)  # Asegurar que tiene un consecutivo único

    # Crear tabla de asignación de grupos
    grupos = []
    total_registros = len(df)
    registros_por_grupo = total_registros // num_grupos

    for i in range(num_grupos):
        min_consecutivo = (i * registros_por_grupo) + 1
        max_consecutivo = total_registros if i == num_grupos - 1 else (i + 1) * registros_por_grupo
        grupos.append({
            "nombre_grupo": f"Grupo {i + 1}",  # ✅ Ajustado a la clave correcta
            "min_consecutivo": min_consecutivo,  # ✅ Ajustado a la clave correcta
            "max_consecutivo": max_consecutivo  # ✅ Ajustado a la clave correcta
        })

    # Guardar en la base de datos
    guardar_asignacion_grupos(grupos)
    
    return df


def obtener_grupo_por_nombre(nombre):
    """
    Asigna un grupo a un usuario basado en su nombre.
    """
    
    grupo_asignado = None
    if nombre == "jaime":
        grupo_asignado = "Grupo 1"
    elif nombre == "juan":
        grupo_asignado = "Grupo 2"
    elif nombre == "henry":
        grupo_asignado = "Grupo 3"
    elif nombre == "alexandra":
        grupo_asignado = "Grupo 4"
    else:
        raise ValueError(f"⚠️ El nombre '{nombre}' no tiene un grupo asignado. Los nombres son: jaime, juan, henry, alexandra.")
    
    return grupo_asignado


def cargar_mi_grupo(nombre, df):
    """
    Carga solo el subconjunto de datos correspondiente al usuario según la asignación de grupos en la BD.
    """
    grupo_asignado = obtener_grupo_por_nombre(nombre)
  
    grupos = obtener_asignacion_grupos() 

    print(f"Claves disponibles en grupos: {grupos[0].keys() if grupos else 'Lista vacía'}")

    # Filtrar el grupo asignado
    rango = next((g for g in grupos if g["nombre_grupo"] == grupo_asignado), None)
    if not rango:
        print("⚠️ No se encontró un rango para este grupo.")
        return None

    min_id, max_id = rango["min_consecutivo"], rango["max_consecutivo"]

    # Filtrar el DataFrame por el rango asignado
    df_filtrado = df[(df["ID_Consecutivo"] >= min_id) & (df["ID_Consecutivo"] <= max_id)]
    print(f"✅ {nombre} procesará {df_filtrado.shape[0]} registros del Grupo {grupo_asignado}.")
    return df_filtrado
