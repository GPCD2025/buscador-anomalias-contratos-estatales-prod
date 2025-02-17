import psycopg2
from psycopg2 import sql
from datetime import datetime
import json
import unicodedata

# Configuración de la base de datos PostgreSQL
DB_CONFIG = {
    "dbname": "anomalias",
    "user": "anomalias",
    "password": "H7iubdf9889bc",
    "host": "ec2-3-86-24-125.compute-1.amazonaws.com",
    "port": "5432"
}

def conectar_db():
    """Establece conexión con PostgreSQL"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Error de conexión: {e}")
        return None

# 🔹 Función para limpiar y normalizar claves del JSON
def limpiar_clave(texto):
    """ Convierte las claves a minúsculas, sin espacios ni caracteres especiales """
    if not isinstance(texto, str):
        return texto
    texto = texto.lower().strip()
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("utf-8")  # Elimina acentos
    texto = texto.replace(" ", "_")  # Reemplaza espacios por guiones bajos
    return texto

def normalizar_json(data):
    """ Aplica la limpieza a las claves del JSON """
    if isinstance(data, dict):
        return {limpiar_clave(k): normalizar_json(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [normalizar_json(i) for i in data]
    return data

def insertar_empresa(conn, empresa):
    """Inserta una empresa en la base de datos, evitando duplicados"""
    try:
        query = """
        INSERT INTO empresas (
            nit, razon_social, sigla, municipio_dpto, categoria,
            numero_matricula, ultimo_ano_renovado, fecha_renovacion, fecha_matricula, fecha_vigencia,
            estado_matricula, motivo_cancelacion, tipo_sociedad, tipo_organizacion, categoria_matricula,
            fecha_ultima_actualizacion, emprendimiento_social, fecha_creacion
        ) VALUES (
            %(nit)s, %(razon_social)s, %(sigla)s, %(municipio_dpto)s, %(categoria)s,
            %(numero_matricula)s, %(ultimo_ano_renovado)s, %(fecha_renovacion)s, %(fecha_matricula)s, %(fecha_vigencia)s,
            %(estado_matricula)s, %(motivo_cancelacion)s, %(tipo_sociedad)s, %(tipo_organizacion)s, %(categoria_matricula)s,
            %(fecha_ultima_actualizacion)s, %(emprendimiento_social)s, %(fecha_creacion)s
        ) ON CONFLICT (nit) DO NOTHING;
        """
        with conn.cursor() as cur:
            empresa["fecha_creacion"] = datetime.utcnow()
            cur.execute(query, empresa)
        conn.commit()
        print(f"✅ Empresa {empresa['nit']} insertada correctamente.")
    except Exception as e:
        print(f"❌ Error en la inserción de empresa {empresa['nit']}: {e}")

def insertar_procedimiento(conn, procedimiento):
    """Inserta un procedimiento de contratación"""
    query = """
    INSERT INTO procedimientos (
        nit_empresa, nombre, descripcion, modalidad_contratacion, justificacion_modalidad, fecha_creacion
    ) VALUES (
        %(nit_empresa)s, %(nombre)s, %(descripcion)s, %(modalidad_contratacion)s, %(justificacion_modalidad)s, %(fecha_creacion)s
    );
    """
    with conn.cursor() as cur:
        procedimiento["fecha_creacion"] = datetime.utcnow()
        cur.execute(query, procedimiento)
    conn.commit()

def insertar_actividad_economica(conn, empresa_id, actividad):
    """Inserta actividades económicas asociadas a una empresa"""
    query = """
    INSERT INTO actividades_economicas (empresa_id, codigo, descripcion, fecha_creacion)
    VALUES (%s, %s, %s, %s);
    """
    with conn.cursor() as cur:
        cur.execute(query, (empresa_id, actividad["codigo"], actividad["descripcion"], datetime.utcnow()))
    conn.commit()

def insertar_representante_legal(conn, empresa_id, representante):
    """Inserta los representantes legales de una empresa"""
    query = """
    INSERT INTO representantes_legales (empresa_id, nombre, identificacion, cargo, facultades, fecha_creacion)
    VALUES (%s, %s, %s, %s, %s, %s);
    """
    with conn.cursor() as cur:
        cur.execute(query, (empresa_id, representante["nombre"], representante["identificacion"], 
                            representante["cargo"], representante["facultades"], datetime.utcnow()))
    conn.commit()

def obtener_empresa_id(conn, nit):
    """Obtiene el ID de la empresa a partir de su NIT"""
    query = "SELECT id FROM empresas WHERE nit = %s;"
    with conn.cursor() as cur:
        cur.execute(query, (nit,))
        result = cur.fetchone()
    return result[0] if result else None

def insertar_contrato(conn, contrato):
    """Inserta un contrato en la base de datos."""
    try:
        query = """
        INSERT INTO contratos (
            empresa_id, id_del_proceso, nombre_del_procedimiento,
            descripcion_del_procedimiento, modalidad_de_contratacion,
            justificacion_modalidad_de_contratacion, fecha_creacion, nombre_estudiante
        ) VALUES (
            %(empresa_id)s, %(id_del_proceso)s, %(nombre_del_procedimiento)s,
            %(descripcion_del_procedimiento)s, %(modalidad_de_contratacion)s,
            %(justificacion_modalidad_de_contratacion)s, %(fecha_creacion)s, 
            %(nombre_estudiante)s
        ) ON CONFLICT (id_del_proceso) DO NOTHING;
        """
        
        with conn.cursor() as cur:
            contrato["fecha_creacion"] = datetime.utcnow()
            cur.execute(query, contrato)
        conn.commit()
        print(f"✅ Contrato {contrato['id_del_proceso']} insertado correctamente.")
    
    except Exception as e:
        print(f"❌ Error en la inserción del contrato {contrato['id_del_proceso']}: {e}")

def procesar_datos(data_array):
    """Procesa el array de datos e inserta en la base de datos"""
    conn = conectar_db()
    if not conn:
        return

    try:
        # 🔹 Normalizar JSON antes de procesarlo
        data_array = normalizar_json(data_array)

        for item in data_array:
            print(f"🔹 Procesando empresa: {item.get('nit', 'N/A')}") 

            # 🔹 Normalización de empresa_data con manejo de errores
            empresa_data = {
                "nit": item.get("nit", "N/A").split(" - ")[0],  # Usa "N/A" si no existe
                "razon_social": item["formacion_rues"].get("razon_social", "N/A")[:255],
                "sigla": item["formacion_rues"].get("sigla", "N/A")[:50],  # Suponiendo que la BD tiene límite
                "municipio_dpto": item["formacion_rues"].get("municipio/dpto", "N/A")[:255],
                "categoria": item["formacion_rues"].get("categoria", "N/A")[:255],
                "numero_matricula": item["formacion_rues"].get("numero_de_matricula", "N/A")[:50],
                "ultimo_ano_renovado": int(item["formacion_rues"].get("ultimo_ano_renovado", 0)),  # Si falta, pone 0
                "fecha_renovacion": datetime.strptime(item["formacion_rues"].get("fecha_de_renovacion", "19000101"), "%Y%m%d").date(),
                "fecha_matricula": datetime.strptime(item["formacion_rues"].get("fecha_de_matricula", "19000101"), "%Y%m%d").date(),
                "fecha_vigencia": item["formacion_rues"].get("fecha_de_vigencia", "N/A")[:255],
                "estado_matricula": item["formacion_rues"].get("estado_de_la_matricula", "N/A")[:100],
                "motivo_cancelacion": item["formacion_rues"].get("motivo_cancelacion", "N/A")[:255],
                "tipo_sociedad": item["formacion_rues"].get("tipo_de_sociedad", "N/A")[:255],
                "tipo_organizacion": item["formacion_rues"].get("tipo_de_organizacion", "N/A")[:255],
                "categoria_matricula": item["formacion_rues"].get("categoria_de_la_matricula", "N/A")[:255],
                "fecha_ultima_actualizacion": datetime.strptime(item["formacion_rues"].get("fecha_ultima_actualizacion", "19000101"), "%Y%m%d").date(),
                "emprendimiento_social": item["formacion_rues"].get("emprendimiento_social", "N")[:1]  # 🔹 Fix para character(1)
            }

            insertar_empresa(conn, empresa_data)

            # Obtener el ID de la empresa recién insertada
            empresa_id = obtener_empresa_id(conn, empresa_data["nit"])

            if empresa_id:
                # 🔹 Insertar Contrato
                contrato_data = {
                    "empresa_id": empresa_id,
                    "id_del_proceso": item.get("id_del_proceso", "N/A")[:50],  # Truncado para evitar errores
                    "nombre_del_procedimiento": item.get("nombre_del_procedimiento", "N/A"),
                    "descripcion_del_procedimiento": item.get("descripcion_del_procedimiento", "N/A"),
                    "modalidad_de_contratacion": item.get("modalidad_de_contratacion", "N/A"),
                    "justificacion_modalidad_de_contratacion": item.get("justificacion_modalidad_de_contratacion", "N/A"),
                    "nombre_estudiante": item.get("nombre_estudiante", "N/A")
                }
                insertar_contrato(conn, contrato_data)
                
                # Insertar Actividades Económicas
                for actividad in item["formacion_rues"]["actividades_economicas"]:
                    insertar_actividad_economica(conn, empresa_id, actividad)

                # Insertar Representantes Legales
                representantes_texto = item["formacion_rues"]["representantes_legales"]
                for linea in representantes_texto.split("****"):
                    partes = linea.strip().split(" - ")
                    if len(partes) >= 2:
                        representante_data = {
                            "nombre": partes[1],
                            "identificacion": partes[0],
                            "cargo": "Representante Legal",
                            "facultades": item["formacion_rues"]["representantes_legales"]
                        }
                        insertar_representante_legal(conn, empresa_id, representante_data)
        
        print("Datos insertados correctamente.")
    except Exception as e:
        print(f"Error en la inserción: {e}")
    finally:
        conn.close()
        
def obtener_contratos_procesados( ):
    """Obtiene la lista de ID de procesos ya registrados en la base de datos."""
    query = "SELECT id_del_proceso FROM contratos;"
    try:
        conn = conectar_db()
        with conn.cursor() as cur:
            cur.execute(query)
            resultados = cur.fetchall()
        
        # Extraer solo los valores de ID del proceso en una lista
        id_procesos_procesados = [row[0] for row in resultados]

        print(f"✅ Se han obtenido {len(id_procesos_procesados)} ID de procesos procesados.")
        return id_procesos_procesados
    except Exception as e:
        print(f"❌ Error al obtener los contratos procesados: {e}")
        return []
    finally:
        conn.close()


def guardar_asignacion_grupos(grupos):
    """Guarda la asignación de grupos en la base de datos."""
    conn = conectar_db()
    try:
        query = """
        INSERT INTO grupos_asignados (nombre_grupo, min_consecutivo, max_consecutivo, fecha_creacion)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (nombre_grupo) DO UPDATE 
        SET min_consecutivo = EXCLUDED.min_consecutivo, 
            max_consecutivo = EXCLUDED.max_consecutivo, 
            fecha_creacion = EXCLUDED.fecha_creacion;
        """
        with conn.cursor() as cur:
            for grupo in grupos:
                cur.execute(query, (grupo["nombre_grupo"], grupo["min_consecutivo"], grupo["max_consecutivo"], datetime.utcnow()))
        conn.commit()
        print("✅ Asignación de grupos guardada en la base de datos.")
    except Exception as e:
        print(f"❌ Error al guardar la asignación de grupos: {e}")
    finally:
        conn.close()


def obtener_asignacion_grupos():
    """Recupera la asignación de grupos desde la base de datos."""
    query = "SELECT nombre_grupo, min_consecutivo, max_consecutivo FROM grupos_asignados;"
    conn = conectar_db()
    grupos = []
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            grupos = cur.fetchall()
    except Exception as e:
        print(f"❌ Error al obtener la asignación de grupos: {e}")
    finally:
        conn.close()

    return [{"nombre_grupo": row[0], "min_consecutivo": row[1], "max_consecutivo": row[2]} for row in grupos]

