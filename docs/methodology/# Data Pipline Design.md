# Riesgos Identificados

## 1. Creación de un Web Scraping

### Riesgos Identificados:
- **Cambios en la estructura de la página de origen**: Las modificaciones en el código HTML pueden afectar la extracción de datos y requerir mantenimiento frecuente.
- **Bloqueo de acceso por parte del servidor**: Algunas páginas implementan medidas anti-scraping, como CAPTCHAs o restricciones de IP, lo que puede interrumpir la operación.
- **Cumplimiento legal y ético**: Dependiendo de la regulación vigente y los términos de uso del sitio web, el scraping podría violar políticas de privacidad o protección de datos.

## 2. Manejo de Eventos y Errores

### Riesgos Identificados:
- **Falta de control de excepciones**: Si los eventos y errores no están correctamente gestionados, la aplicación podría fallar inesperadamente sin ofrecer una solución oportuna.
- **Fallas en la captura de eventos críticos**: Un manejo deficiente de eventos puede afectar la estabilidad y fiabilidad de la aplicación, generando respuestas inconsistentes o erróneas.

## 3. Información No Existente en la Página de Origen

### Riesgos Identificados:
- **Errores en la extracción de datos**: Si la información no está disponible, el sistema podría devolver resultados vacíos o datos incorrectos.
- **Falta de validación de datos**: La aplicación podría procesar datos nulos o incompletos, generando sesgos en los resultados.

## 4. Utilización de un LLM de Mediano Tamaño (7B)

### Riesgos Identificados:
- **Costos computacionales elevados**: Dependiendo de la infraestructura utilizada, el procesamiento de un LLM puede generar costos significativos en almacenamiento y cálculo.
- **Dependencia de la calidad de los datos**: El rendimiento del modelo está sujeto a la calidad de los datos utilizados para su entrenamiento y validación.

## 5. Inexactitudes del Prompt o Resiliencia del LLM a Seguir Instrucciones

### Riesgos Identificados:
- **Respuestas inconsistentes o incorrectas**: Dependiendo de la formulación del prompt, el LLM podría generar respuestas ambiguas o imprecisas.
- **Falta de control sobre los sesgos del modelo**: Los LLM pueden reproducir sesgos inherentes a los datos de entrenamiento, afectando la calidad y objetividad de las respuestas.
- **Dificultad en la interpretabilidad**: La toma de decisiones basada en los resultados del LLM puede ser compleja si no hay transparencia en el proceso de generación de respuestas.

---

La evaluación de estos riesgos es clave para garantizar la robustez y fiabilidad de las aplicaciones desarrolladas en Python. Se recomienda implementar estrategias de mitigación como validación de datos, monitoreo continuo, revisión de prompts y optimización del manejo de excepciones para minimizar el impacto de los riesgos identificados.
