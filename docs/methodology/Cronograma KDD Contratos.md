# **Cronograma KDD - Detección de Anomalías en Contratos**

## **Distribución de Tareas**

- **Jaime** (Ing. Datos): Desarrollo del notebook.
- **Henry** (Arquitecto) & **Juan Camilo** (Ing. ML): Creación del project plan.
- **J. Alexandra** (Analista de BI): Ingeniería de prompts y desarrollo de tableros.

## **Semana 1: Extracción, Preprocesamiento y Limpieza de Datos**

| Día       | Actividad                                                                                                               | Responsable  | Herramientas                              |
| --------- | ----------------------------------------------------------------------------------------------------------------------- | ------------ | ----------------------------------------- |
| **Día 1** | Definir estructura y formato de los datos a extraer de **SECOP** y **Cámara de Comercio**. Ajustar scripts de scraping. | Jaime        | Python (Scrapy, Selenium), API SECOP, SQL |
| **Día 2** | Implementar y probar scripts de scraping y conexión con fuentes de datos. Identificar posibles errores.                 | Jaime        | Python, Pandas, SQL                       |
| **Día 3** | Normalización y limpieza de datos extraídos. Eliminar duplicados, corregir valores nulos.                               | Jaime        | Pandas, SQL                               |
| **Día 4** | Unificación de bases de datos de distintas fuentes en un solo esquema. Revisión de formatos.                            | Jaime        | SQL, Pandas                               |
| **Día 5** | Exploración inicial de datos (estadísticas descriptivas, detección de outliers básicos). Visualización inicial.         | J. Alexandra | Power BI, Matplotlib, Seaborn             |

## **Semana 2: Transformación, Modelado y Evaluación**

| Día        | Actividad                                                                                          | Responsable        | Herramientas         |
| ---------- | -------------------------------------------------------------------------------------------------- | ------------------ | -------------------- |
| **Día 6**  | Definir variables clave para detección de anomalías (monto, proveedor, tiempo de ejecución, etc.). | Henry, Juan Camilo | Pandas, SQL          |
| **Día 7**  | Implementación de técnicas de detección de anomalías (IQR, DBSCAN, Isolation Forest).              | Juan Camilo        | Scikit-learn, MLflow |
| **Día 8**  | Ajuste de modelos y comparación de resultados. Revisión de falsos positivos/negativos.             | Juan Camilo        | Python, Jupyter      |
| **Día 9**  | Creación de visualizaciones interactivas de anomalías encontradas.                                 | J. Alexandra       | Power BI             |
| **Día 10** | Documentación de hallazgos y entrega de resultados preliminares.                                   | Todo el equipo     | Confluence, Notion   |

