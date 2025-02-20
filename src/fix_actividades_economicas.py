import pandas as pd
from insert_data import get_all_actividades, delete_all_actividades, insert_cleaned_actividades

class DataProcessing:
     
    @staticmethod 
    def export_original_data():
        df = get_all_actividades()
        df.to_csv("actividades_economicas_original.csv", index=False)
        return df
    
    @staticmethod
    def clean_data(df):
        df = df.sort_values(by=["empresa_id", "codigo", "fecha_creacion"], ascending=[True, True, False])
        df_cleaned = df.drop_duplicates(subset=["empresa_id", "codigo"], keep="first")
        df_cleaned.to_csv("actividades_economicas_limpias.csv", index=False)
        return df_cleaned
 
    @staticmethod
    def update_database():
        df_original = DataProcessing.export_original_data()
        df_cleaned = DataProcessing.clean_data(df_original)
        delete_all_actividades()
        insert_cleaned_actividades(df_cleaned)
        print("✅ Datos limpios insertados en la base de datos.")

if __name__ == "__main__":
    DataProcessing.update_database()
