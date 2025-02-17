from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver  
from retrying import retry
import time

class RUESScraper:
    def __init__(self):
        """Inicializa el navegador y configura el WebDriver."""
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        
        self.driver = webdriver.Chrome(options=options)
        self.informacion_empresa = {}  # Diccionario para almacenar la info
        self.fila_resultado = None

 
    def manejar_validacion_robot(self):
        """Maneja la validación de CAPTCHA si aparece."""
        try:
            boton_enviar = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and @value='Enviar']"))
            ) 
            boton_enviar.click()
            print("✅ Se ha hecho clic en el botón 'Enviar'.")

            # Lanzar una excepción controlada para que retry vuelva a ejecutar obtener_informacion()
            raise Exception("Captcha detectado y solucionado. Reintentando consulta...")
        
        except Exception as e:
            print("⚠️ No se encontró el CAPTCHA, continuando...") 
        
    def cargar_pagina(self):
        """Carga la página de consulta del RUES y evita el modal inicial."""
        url = "https://www.rues.org.co/?old=true"
        self.driver.get(url) 
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "txtNIT")))
        print("✅ Página cargada correctamente.")
        time.sleep(3)
        # Recargar la página para evitar que aparezca el modal
        self.driver.refresh()

        # Esperar a que la página cargue completamente
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "txtNIT"))
        )

        print("✅ Página recargada. Modal evitado.")



    @retry(stop_max_attempt_number=5, wait_fixed=2000)
    def obtener_informacion(self, nit_empresa):
        """Consulta la información de la empresa por NIT."""
        try:
            self.informacion_empresa["NIT"] = nit_empresa

            # Ingresar NIT en el campo de búsqueda
            campo_nit = self.driver.find_element(By.ID, "txtNIT")
            campo_nit.clear()
            campo_nit.send_keys(nit_empresa)

            # Hacer clic en el botón de búsqueda
            boton_buscar = self.driver.find_element(By.ID, "btnConsultaNIT")
            boton_buscar.click()

            # Esperar la carga de los resultados
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "rmTable2")))
            print("✅ Consulta realizada correctamente.")
            
            # Espera 3 segundos antes de extraer datos
            time.sleep(3)
        except Exception as e:
            print(f"⚠️ Error en la consulta: {e}")
            self.manejar_validacion_robot()  # Llamar a la validación del CAPTCHA
            raise e  # Relanzar la excepción para que retry funcione

    @retry(stop_max_attempt_number=5, wait_fixed=2000)
    def cargar_empresa(self):
        """Extrae los datos de la empresa desde la tabla de resultados."""
        try:
            # Esperar que el mensaje de "No hay resultados" aparezca si existe
            try:
                no_resultado = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "card-info"))
                )
                # Verificamos si el mensaje contiene la alerta de "No ha retornado resultados"
                if "La consulta por NIT no ha retornado resultados" in no_resultado.text:
                    print("❌ No se encontraron resultados para la consulta.")
                    return False  # Retorna False si no hay resultados
            except:
                pass  # Si el mensaje no está presente, continuamos con el proceso

            # Esperar que la tabla de resultados aparezca
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, "rmTable2")))

            # Extraer información de la tabla
            self.fila_resultado = self.driver.find_element(By.XPATH, "//table[@id='rmTable2']/tbody/tr")
            columnas = self.fila_resultado.find_elements(By.TAG_NAME, "td")

            # Guardar información en el diccionario
            self.informacion_empresa.update({
                "NIT": columnas[0].text.strip(),
                "Razón Social": columnas[1].text.strip(),
                "Sigla": columnas[2].text.strip(),
                "Municipio/Dpto": columnas[3].text.strip(),
                "Categoría": columnas[4].text.strip()
            })

            print("✅ Datos extraídos de la tabla de resultados.")
            return True
        except Exception as e:
            print(f"⚠️ Error al cargar la empresa: {e}")
            self.manejar_validacion_robot()
            raise e
        
    @retry(stop_max_attempt_number=5, wait_fixed=2000)
    def redirigir_detalle_empresa(self):
        try:
            from selenium.webdriver.common.action_chains import ActionChains

            # Encontrar la celda del NIT que contiene el botón
            celda_nit = self.fila_resultado.find_element(By.XPATH, ".//td[1]")  # Primera columna (NIT)

            # Realizar un scroll hacia el elemento para asegurarnos de que es visible
            self.driver.execute_script("arguments[0].scrollIntoView();", celda_nit)
            
            # Intentar hacer clic en la celda (esto podría abrir el detalle)
            try:
                celda_nit.click()
            except Exception:
                print("🔹 Celda del NIT no interactuable directamente, probando con JavaScript.") 
                # Si el click normal no funciona, usar JavaScript para forzar la interacción
                self.driver.execute_script("arguments[0].click();", celda_nit)

            # Esperar a que la página de detalles cargue completamente
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "card-title")))
            
            time.sleep(3)
            enlace_detalle = self.driver.find_element(By.XPATH, "//a[contains(@href, 'ConsultarDetalleRM')]")

            # Realizar un scroll hacia el elemento para asegurarnos de que es visible
            self.driver.execute_script("arguments[0].scrollIntoView();", enlace_detalle)

            # Hacer clic en el enlace para abrir la página de detalles
            try:
                enlace_detalle.click()
            except Exception:
                print("🔹 Enlace no interactuable directamente, probando con JavaScript.")
                self.driver.execute_script("arguments[0].click();", enlace_detalle)

            # Esperar a que la nueva página cargue completamente
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "card-title")))

            print("✅ Redirigido correctamente a la página de detalles.")
        except Exception as e:
            print(f"⚠️ Error al redirigir a la página de detalles: {e}")
            self.manejar_validacion_robot()
            raise e

    @retry(stop_max_attempt_number=5, wait_fixed=2000)
    def llenar_campos_finales(self):
        """Extrae los datos de la tabla final y los guarda en `self.informacion_empresa`."""
        try:           
            # Esperar a que la tabla de información esté disponible
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "table"))
            )

            # Buscar la tabla dentro de la sección correspondiente
            tabla_info = self.driver.find_element(By.XPATH, "//div[contains(@class, 'card-text')]/table")

            # Extraer las filas de la tabla
            filas = tabla_info.find_elements(By.TAG_NAME, "tr")

            # Recorrer las filas de la tabla y guardar en el diccionario `self.informacion_empresa`
            for fila in filas:
                columnas = fila.find_elements(By.TAG_NAME, "td")
                if len(columnas) == 2:
                    clave = columnas[0].text.strip()
                    valor = columnas[1].text.strip()
                    self.informacion_empresa[clave] = valor  # Guardar en `self.informacion_empresa`

            print("✅ Datos finales extraídos y guardados correctamente en `self.informacion_empresa`.")

        except Exception as e:
            print(f"⚠️ Error al llenar los campos finales: {e}")
            self.manejar_validacion_robot()
            raise e  # Relanzar excepción para que `retry` funcione correctamente

 

    @retry(stop_max_attempt_number=5, wait_fixed=2000)
    def extraer_actividades_economicas(self):
        """Extrae las Actividades Económicas y las guarda en `self.informacion_empresa`."""
        try:
            # Esperar a que la sección de Actividades Económicas esté disponible
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'card border-info')]//ul[@class='cleanlist']"))
            )

            # Ubicar la lista de actividades económicas
            lista_actividades = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'card border-info')]//ul[@class='cleanlist']/li")

            # Lista para almacenar las actividades económicas
            actividades_economicas = []

            # Recorrer cada elemento de la lista y extraer el código y la descripción
            for actividad in lista_actividades:
                texto = actividad.text.strip()
                if texto:  # Evitar elementos vacíos
                    partes = texto.split(" ", 1)  # Separar por el primer espacio (Código y Descripción)
                    if len(partes) == 2:
                        codigo, descripcion = partes
                    else:
                        codigo, descripcion = partes[0], "No especificada"

                    actividades_economicas.append({"Código": codigo, "Descripción": descripcion})

            # Guardar en el diccionario de información
            self.informacion_empresa["Actividades Económicas"] = actividades_economicas

            print("✅ Actividades Económicas extraídas correctamente.")
        
        except Exception as e:
            print(f"⚠️ Error al extraer Actividades Económicas: {e}")
            self.manejar_validacion_robot()
            raise e

    @retry(stop_max_attempt_number=5, wait_fixed=2000)
    def extraer_representantes_legales(self):
        """Extrae la información de Representantes Legales y la guarda en `self.informacion_empresa`."""
        try:
            # Esperar a que el botón de representantes sea clickeable y hacer clic
            boton_representantes = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "Facultades"))
            )
            boton_representantes.click()
            print("✅ Se ha hecho clic en el botón 'Representantes Legales'.")

            time.sleep(5)
            # Esperar a que el contenedor de Facultades esté presente
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "txtFacultades"))
            )

            # Obtener el contenido del div donde está la información de Representantes Legales y Facultades
            contenedor_facultades = self.driver.find_element(By.ID, "txtFacultades")

            # Extraer el texto y limpiar
            informacion_representantes = contenedor_facultades.text.replace("\n", " ").replace("\xa0", " ").strip()

            # Guardar en el diccionario de información
            self.informacion_empresa["Representantes Legales"] = informacion_representantes

            print("✅ Información de Representantes Legales extraída correctamente.")
        
        except Exception as e:
            print(f"⚠️ Error al extraer Representantes Legales: {e}")
            self.manejar_validacion_robot()
            raise e




    def obtener_informacion_completa(self):
        """Retorna la información completa de la empresa."""
        return self.informacion_empresa

    def cerrar_pagina(self):
        """Cierra el navegador."""
        self.driver.quit()
        print("❌ Navegador cerrado.")

