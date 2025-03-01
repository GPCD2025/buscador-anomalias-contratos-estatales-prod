# Evaluación de Riesgos

## Descripción
Este documento identifica los posibles riesgos que podrían afectar el éxito del proyecto de análisis de contratos públicos. Los riesgos han sido clasificados en técnicos, organizacionales, y financieros. A continuación se detallan los riesgos más relevantes, su impacto potencial en el proyecto y las estrategias de mitigación propuestas para minimizarlos.

## Identificación de Riesgos

### 1. **Riesgo Técnico: Errores en la Extracción de Datos**
- **Descripción**: El proceso de extracción de datos mediante técnicas de scraping y conexión con APIs puede enfrentar problemas técnicos como cambios en la estructura del sitio web o interrupciones en el servicio de las APIs.
- **Impacto**: La extracción de datos puede ser incompleta o incorrecta, lo que afectaría la calidad del análisis y retrasaría el proyecto.
- **Plan de Mitigación**:
  - Implementar un monitoreo constante de los scripts de scraping para detectar cambios en las estructuras de los sitios web.
  - Establecer procedimientos de validación de datos para verificar la calidad y consistencia antes de procesarlos.

### 2. **Riesgo Organizacional: Falta de Coordinación entre el Equipo**
- **Descripción**: Dado que el equipo de trabajo está compuesto por varios roles con diferentes responsabilidades, podría haber falta de coordinación en la ejecución de las tareas.
- **Impacto**: Retrasos en las entregas de las fases del proyecto, malentendidos en las expectativas de los entregables y dificultades en la integración de los resultados de diferentes áreas.
- **Plan de Mitigación**:
  - Realizar reuniones periódicas de seguimiento entre los miembros del equipo para asegurar que todos estén alineados con los objetivos y avances del proyecto.
  - Utilizar herramientas de gestión de proyectos (como Trello y GitHub) para hacer seguimiento de las tareas y avances.

### 3. **Riesgo Financiero: Limitación de Recursos Tecnológicos**
- **Descripción**: El proyecto puede requerir recursos tecnológicos adicionales, como servidores o herramientas específicas para procesamiento y modelado de datos, que podrían no estar disponibles debido a limitaciones presupuestarias.
- **Impacto**: Un retraso en la adquisición de recursos puede afectar el ritmo del trabajo y la calidad de los modelos de detección de anomalías.
- **Plan de Mitigación**:
  - Priorizar el uso de herramientas gratuitas y de código abierto siempre que sea posible.
  - Buscar acuerdos con proveedores de recursos en la nube (como AWS o Google Cloud) que ofrezcan descuentos para proyectos gubernamentales o de investigación.

### 4. **Riesgo Técnico: Calidad de los Modelos de Anomalías**
- **Descripción**: Los modelos de aprendizaje automático para la detección de anomalías, como Isolation Forest y DBSCAN, pueden no ofrecer los resultados esperados debido a una incorrecta selección de variables o un ajuste inadecuado de los parámetros.
- **Impacto**: Los modelos podrían generar muchos falsos positivos o negativos, lo que disminuiría la efectividad del proyecto y la confianza en los resultados.
- **Plan de Mitigación**:
  - Realizar pruebas exhaustivas de los modelos, utilizando técnicas como la validación cruzada para asegurar que los resultados sean consistentes.
  - Ajustar continuamente los modelos y realizar iteraciones basadas en los resultados de las evaluaciones.

### 5. **Riesgo Legal y Ético: Uso de Datos Sensibles**
- **Descripción**: El manejo de datos contractuales puede estar sujeto a normativas legales relacionadas con la protección de datos personales, especialmente si los contratos incluyen información sensible.
- **Impacto**: El incumplimiento de las regulaciones podría derivar en sanciones legales y en la desconfianza por parte de los stakeholders.
- **Plan de Mitigación**:
  - Asegurarse de que todos los datos utilizados provengan de fuentes públicas y sean anonimizados según las regulaciones locales (como el GDPR).
  - Implementar medidas de seguridad para proteger los datos procesados, como el cifrado de datos y control de acceso.

### 6. **Riesgo Organizacional: Retrasos en la Aprobación de Resultados**
- **Descripción**: Los stakeholders clave, como Colombia Compra Eficiente y otros organismos gubernamentales, podrían experimentar retrasos en la revisión o aprobación de los resultados entregados.
- **Impacto**: Los retrasos en la aprobación de los resultados podrían afectar la implementación de las recomendaciones y la capacidad de generar cambios en los procesos de contratación pública.
- **Plan de Mitigación**:
  - Establecer un cronograma claro con tiempos de revisión acordados con los stakeholders.
  - Tener reuniones regulares con las partes interesadas para revisar los avances y asegurarse de que los entregables sean aceptables.

## Resumen de Estrategias de Mitigación

- **Monitoreo y Validación**: Implementación de procesos de control de calidad de datos y verificación de resultados durante todo el ciclo del proyecto.
- **Comunicación y Coordinación**: Establecimiento de reuniones periódicas y uso de herramientas de gestión para mantener la alineación del equipo y con los stakeholders.
- **Adaptabilidad**: Ajuste flexible de los modelos y recursos en función de las necesidades del proyecto y los resultados obtenidos durante el proceso.
