# Plan del Proyecto

## Descripción
Este documento define el alcance del proyecto, sus objetivos y el cronograma general de trabajo. En él se detallan las fases del proyecto, los entregables esperados y los responsables de cada actividad. Se recomienda actualizar este documento regularmente conforme avanza el proyecto para reflejar cambios en los plazos, recursos y tareas.

## Alcance del Proyecto
El proyecto tiene como objetivo analizar los contratos públicos en Colombia, específicamente los adjudicados a personas jurídicas durante 2024 en Bogotá, a través del Sistema Electrónico de Contratación Pública (SECOP II). Se busca identificar patrones y detectar irregularidades, evaluando la coherencia entre las actividades económicas de los contratistas y los objetos contractuales asignados.

## Objetivos
- **Objetivo General**: Aplicar técnicas de ciencia de datos para analizar los contratos públicos en Colombia, identificar anomalías y mejorar la transparencia en la contratación pública.
- **Objetivos Específicos**:
  - Analizar la base de datos del SECOP II y conectarla con el Registro Único Empresarial y Social (RUES).
  - Desarrollar modelos de detección de anomalías en los contratos, como IQR, DBSCAN e Isolation Forest.
  - Crear visualizaciones de los resultados y generar un informe final con hallazgos y recomendaciones para la optimización de la supervisión en la contratación pública.

## Cronograma General de Trabajo
A continuación se presenta el cronograma de actividades basado en la metodología KDD (Knowledge Discovery in Databases). Cada fase tiene entregables específicos y responsables asignados para asegurar el avance del proyecto.

### Fase 1: **Extracción, Preprocesamiento y Limpieza de Datos**
- **Semana 1**
    - **Día 1**: Definir la estructura y formato de los datos a extraer de SECOP y Cámara de Comercio. Ajustar scripts de scraping.  
      **Responsable**: Jaime (Ingeniero de Datos)  
      **Herramientas**: Python (Scrapy, Selenium), API SECOP, SQL
    - **Día 2**: Implementar y probar scripts de scraping y conexión con fuentes de datos. Identificar posibles errores.  
      **Responsable**: Jaime  
      **Herramientas**: Python, Pandas, SQL
    - **Día 3**: Normalización y limpieza de datos extraídos. Eliminar duplicados, corregir valores nulos.  
      **Responsable**: Jaime  
      **Herramientas**: Pandas, SQL
    - **Día 4**: Unificación de bases de datos de distintas fuentes en un solo esquema. Revisión de formatos.  
      **Responsable**: Jaime  
      **Herramientas**: SQL, Pandas
    - **Día 5**: Exploración inicial de datos (estadísticas descriptivas, detección de outliers básicos). Visualización inicial.  
      **Responsable**: J. Alexandra (Analista de BI)  
      **Herramientas**: Power BI, Matplotlib, Seaborn  

#### Entregable:  
- Datos limpios y estructurados listos para el análisis.

### Fase 2: **Transformación, Modelado y Evaluación**
- **Semana 2**
    - **Día 6**: Definir variables clave para la detección de anomalías (monto, proveedor, tiempo de ejecución, etc.).  
      **Responsables**: Henry (Arquitecto), Juan Camilo (Ingeniero ML)  
      **Herramientas**: Pandas, SQL
    - **Día 7**: Implementación de técnicas de detección de anomalías (IQR, DBSCAN, Isolation Forest).  
      **Responsable**: Juan Camilo (Ingeniero ML)  
      **Herramientas**: Scikit-learn, MLflow
    - **Día 8**: Ajuste de modelos y comparación de resultados. Revisión de falsos positivos/negativos.  
      **Responsable**: Juan Camilo  
      **Herramientas**: Python, Jupyter
    - **Día 9**: Creación de visualizaciones interactivas de anomalías encontradas.  
      **Responsable**: J. Alexandra  
      **Herramientas**: Power BI
    - **Día 10**: Documentación de hallazgos y entrega de resultados preliminares.  
      **Responsable**: Todo el equipo  
      **Herramientas**: Confluence, Notion  

#### Entregable:
- Modelos de detección de anomalías ajustados y evaluados.
- Visualización de anomalías detectadas.

### Fase 3: **Informe Final**
- **Semana 3 y 4**
    - **Día 11-15**: Elaboración del informe final con hallazgos, análisis y recomendaciones.  
      **Responsable**: Todo el equipo  
      **Herramientas**: Google Docs, Power BI (para visualizaciones), Jupyter

#### Entregable:
- Informe final con hallazgos, análisis y recomendaciones.
  
## Responsables de Actividades
El equipo está compuesto por profesionales con roles definidos para asegurar la correcta ejecución de cada fase del proyecto:

- **Jaime (Ingeniero de Datos)**: Responsable de la extracción, limpieza y transformación de datos.
- **Juan Camilo (Ingeniero de ML)**: Responsable del desarrollo y ajuste de modelos de detección de anomalías.
- **J. Alexandra (Analista de BI)**: Responsable de la visualización de los datos y creación de dashboards.
- **Henry (Arquitecto)**: Responsable de la planificación, coordinación general y supervisión de la ejecución del proyecto.

## Actualización del Documento
Este plan de trabajo será revisado y actualizado periódicamente conforme avance el proyecto. Se realizarán ajustes según los resultados obtenidos y las necesidades emergentes del proyecto.
