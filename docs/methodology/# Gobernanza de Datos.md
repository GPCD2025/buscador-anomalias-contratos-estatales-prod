# Gobernanza de Datos

## Descripción
Este documento detalla las políticas de gobernanza de datos implementadas en el proyecto. La gobernanza de datos es un componente esencial para garantizar la calidad, integridad y seguridad de la información manejada en este análisis (Otto, 2020).

## Normas y Estándares Aplicados
El proyecto sigue principios fundamentales de gobernanza de datos basados en estándares reconocidos como el Data Management Body of Knowledge (DMBOK) y las directrices del General Data Protection Regulation (GDPR) para el manejo y protección de datos (DAMA, 2021). Se han aplicado principios de integridad y trazabilidad para garantizar la coherencia de la información.

## Privacidad y Seguridad de Datos
Dado que el conjunto de datos proviene de fuentes públicas, se han implementado prácticas de anonimización y control de acceso a los datos sensibles. Se ha priorizado el uso de protocolos de seguridad como el cifrado en tránsito y en reposo para proteger la información procesada (ISO/IEC 27001, 2022).

## Control y Auditoría de Datos
Si bien la auditoría de datos no fue un foco principal en este proyecto, se han establecido procesos mínimos de validación de datos para mitigar errores y garantizar la consistencia. Se han realizado revisiones periódicas de calidad de datos para identificar y corregir inconsistencias (Redman, 2018).

# Diseño del Pipeline de Datos

## Descripción
Este documento define la arquitectura y flujos de procesamiento de datos utilizados en el proyecto.

## Ingesta y Transformación de Datos
El proceso de ingesta de datos se realizó a partir de fuentes públicas como el SECOP II y el Registro Único Empresarial y Social (RUES), empleando técnicas de web scraping con Scrapy y Selenium, así como conexiones directas a APIs y bases de datos SQL. La transformación de los datos incluyó la limpieza de valores nulos, normalización de formatos y consolidación de información clave mediante Pandas y SQL.

## Almacenamiento y Disponibilidad
Los datos procesados fueron almacenados en bases de datos relacionales y archivos optimizados en formatos Parquet y CSV para mejorar la eficiencia en consultas y procesamiento posterior. Se habilitó un repositorio en Google Drive y AWS S3 para garantizar disponibilidad y respaldo.

## Plan de Monitoreo del Pipeline
El monitoreo del pipeline de datos se estableció mediante registros en MLflow y herramientas de logging en Python, permitiendo detectar posibles errores en la ejecución de los scripts de extracción y transformación. Además, se implementaron visualizaciones en Power BI para el seguimiento de métricas clave sobre la calidad y consistencia de los datos.
