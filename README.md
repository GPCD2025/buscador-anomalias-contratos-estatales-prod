# 📖 Proyecto de Gerencia en Ciencia de Datos

## Descripción General
Este proyecto tiene como objetivo enseñar la gestión efectiva de proyectos de ciencia de datos, abarcando planificación, ejecución, mitigación de riesgos y presentación de resultados. La idea es proporcionar una estructura clara para la gestión de proyectos relacionados con la ciencia de datos, asegurando que las actividades y entregables sean bien definidos y gestionados.

## ¿Cómo empezar?
1. **Revisa la documentación en** `docs/`: Consulta toda la documentación que detalla el proceso de planificación, las metodologías y los entregables.
2. **Define los roles en** `docs/roles/roles.md`: Establece los roles dentro del equipo y sus responsabilidades específicas en el proyecto.
3. **Usa el plan del proyecto en** `project_management/project_plan.md`: Organiza el trabajo según los plazos, entregables y actividades del proyecto.
4. **Sigue la metodología seleccionada en** `docs/methodology/methodology.md`: Implementa la metodología seleccionada, en este caso, **KDD**, para estructurar el flujo de trabajo y la extracción de conocimientos de los datos.

## Flujo del Proyecto

El flujo del proyecto se basa en una metodología estructurada para garantizar la extracción y análisis de datos efectivos. A continuación se detalla el flujo principal de las fases del proyecto:

1. **Inicia el Proyecto**
   - Revisión de los objetivos.
   - Definición del equipo y roles (ver `docs/roles/roles.md`).

2. **Recopilación de Datos**
   - Extracción de datos desde fuentes como el **SECOP II** y el **RUES**.
   - Limpieza y preprocesamiento de los datos obtenidos.

3. **Análisis Exploratorio de Datos**
   - Exploración y validación inicial de la consistencia de los datos.
   - Identificación de patrones relevantes y posibles anomalías.

4. **Modelado (si aplica)**
   - En este proyecto no se implementaron modelos predictivos, pero se podrían aplicar técnicas como **KDD** en futuras etapas.

5. **Visualización**
   - Uso de **Power BI** para visualizar los hallazgos y patrones identificados.
   
6. **Evaluación y Presentación de Resultados**
   - Documentación de los resultados obtenidos.
   - Generación de informes con hallazgos y recomendaciones.

7. **Entrega Final**
   - Entrega de los resultados y presentación a los stakeholders.

### Flujo Gráfico del Proyecto
```mermaid
graph TD
    A[Inicia el Proyecto] --> B[Recopilación de Datos]
    B --> C[Análisis Exploratorio de Datos]
    C --> D[Modelado (si aplica)]
    D --> E[Visualización]
    E --> F[Evaluación y Presentación de Resultados]
    F --> G[Entrega Final]
