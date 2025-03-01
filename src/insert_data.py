import re
import psycopg2
from psycopg2.extras import DictCursor
from datetime import datetime
import pandas as pd
import unicodedata

# Configuración de la base de datos PostgreSQL
DB_CONFIG = {
    "dbname": "anomalias",
    "user": "anomalias",
    "password": "H7iubdf9889bc",
    "host": "ec2-44-201-247-41.compute-1.amazonaws.com",
    "port": "80"
}

estados = {}
estados['procesando'] = 'pro'
estados['finalizado'] = 'fin'
estados['error'] = 'err'

def conectar_db():
    """Establece conexión con PostgreSQL"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Error de conexión: {e}")
        raise e
  
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


# ejecuta el select en la base de datos y recorre los resultados
def get_contratos():
    conn = conectar_db()
    try:
        query = """
        SELECT id, empresa_id, nombre_del_procedimiento, descripcion_del_procedimiento,
            modalidad_de_contratacion, justificacion_modalidad_de_contratacion
        FROM contratos
        order by 1
        limit 100"""
        
        with conn.cursor(cursor_factory=DictCursor) as cur:  # 💡 Usamos DictCursor
            cur.execute(query)
            resultados = cur.fetchall()
        
        contratos = [dict(row) for row in resultados]  # 🔹 Convertimos cada fila en un diccionario
        
        return contratos
    
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        raise error
    finally:
        conn.close()

def get_actividades_from_contrato(contrato_id):
    conn = conectar_db()
    try:
        query = """
            SELECT descripcion from actividades_economicas
            WHERE empresa_id = %s"""
        with conn.cursor() as curs:
            curs.execute(query, (contrato_id,))
            actividades = curs.fetchall()

        print(f"Actividades encontradas: {len(actividades)} - del contrato: {contrato_id}")

        return [actividad[0] for actividad in actividades]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        raise error
    finally:
        conn.close()
 
from unicodedata import normalize

def limpiar_clave(texto):
    if not isinstance(texto, str):
        return texto
 
    texto = texto.lower().strip() 
    texto = normalize("NFKD", texto).encode("ascii", "ignore").decode("utf-8") 
    texto = re.sub(r"[^a-z\s]", "", texto)

    return texto

def clean_coherencias():
    conn = conectar_db()
    with conn.cursor() as curs:
        try:
            curs.execute("""DELETE FROM resultado""")
            conn.commit() 
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            raise error
        finally:
            conn.close()
            
        print('resultados eliminados correctamente')

def save_coherencia(contrato):
        try:
            split = contrato['resultado'].split('-')
            if len(split) > 1:
                save_resultado(split[0], split[1], contrato['id'], contrato['empresa_id'])
            else:
                valor_limpio = limpiar_clave(contrato['resultado'])
                if valor_limpio.strip().lower() == 'verdadero':
                    save_resultado(valor_limpio, "", contrato['id'], contrato['empresa_id'])
                else:
                    print(f'valor limpio {valor_limpio}')
                    print('resultado no guardado')
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            raise error 
            
        print('resultados guardados correctamente')

def save_resultado(resultado,categoria,contrato_id,empresa_id):
    try:
        conn = conectar_db()
        curs = conn.cursor()
        valor_limpio = limpiar_clave(resultado)
        resultado = True if valor_limpio.strip().lower() == 'verdadero' else False 
        print(f"valor_limpio: {valor_limpio} - categoria: {categoria}")
        curs.execute("""
                INSERT INTO resultado (contrato_id, empresa_id, resultado, categoria)
                VALUES (%s, %s, %s, %s)""",
                (contrato_id, empresa_id, resultado, categoria))
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            raise error
    finally:
            conn.close()

def save_prompts(contratos):
    conn = conectar_db()
    with conn.cursor() as curs:
        try:
            for contrato in contratos:
                curs.execute("""
                UPDATE contratos SET prompt = %s
                WHERE id = %s """,
                (contrato['prompt'], contrato['id']))
                conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            raise error
        finally:
            conn.close()
            
def get_all_actividades():
        conn = conectar_db()
        query = "SELECT id, empresa_id, codigo, descripcion, fecha_creacion FROM actividades_economicas"
        df = pd.read_sql(query, conn)
        conn.close()
        return df

def delete_all_actividades():
        conn = conectar_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM actividades_economicas")
        conn.commit()
        cur.close()
        conn.close()

def get_next_contrato_from_db():
    conn = conectar_db()
    with conn.cursor(cursor_factory=DictCursor) as curs:
        try:
            curs.execute("""
            UPDATE contratos SET estado = 'proc'
            WHERE id IN (SELECT MIN(c1.id) FROM contratos c1 WHERE c1.estado IS NULL)
            RETURNING *""")
            conn.commit()
            row = curs.fetchone()
            if not row:
                return None
            contrato = dict(row)  # Ahora row ya es un diccionario
            return contrato
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            raise error
        finally:
            conn.close()


def update_estado_contrato(contrato_id, prompt):
    conn = conectar_db()
    with conn.cursor() as curs:
        try:
            curs.execute("""
            UPDATE contratos SET estado = %s, prompt = %s
            WHERE id = %s """,
            (estados['finalizado'], prompt, contrato_id))
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            raise error
        finally:
            conn.close()

def insert_cleaned_actividades(df):
        conn = conectar_db()
        cur = conn.cursor()

        for _, row in df.iterrows():
            cur.execute(
                "INSERT INTO actividades_economicas (empresa_id, codigo, descripcion, fecha_creacion) VALUES (%s, %s, %s, %s)",
                (row["empresa_id"], row["codigo"], row["descripcion"], row["fecha_creacion"])
            )

        conn.commit()
        cur.close()
        conn.close()
