1️⃣ Data Quality (Calidad de los Datos)
La limpieza de datos se realizó aplicando transformaciones en Power Query, asegurando la coherencia y estandarización de la columna categoria.

🛠 Acciones Implementadas:
✅ Normalización de texto: Se eliminaron espacios en blanco y se convirtieron los valores a minúsculas (Text.Trim + Text.Lower).
✅ Estandarización de categorías: Se mapearon valores específicos a categorías definidas.
✅ Corrección de inconsistencias: Se corrigieron valores con errores tipográficos o formatos irregulares.
✅ Manejo de valores nulos: Se asignó "Sin Información" a registros sin datos.

🔄 Transformaciones Aplicadas:
Se renombraron valores genéricos como "verdadero" o "[verdadero/falso]" a una categoría más clara.
Se agruparon valores similares en categorías amplias (ejemplo: "mantenimiento y reparación especializado de maquinaria y equipo" → "Mantenimiento y Reparación").
Se utilizaron expresiones condicionales (Text.Contains) para asignar etiquetas a valores que contenían descripciones específicas.
Se preservaron los valores originales si no coincidían con ninguna regla de transformación.