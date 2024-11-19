import csv
import os
from services.db import SQLiteDB


class CSVExporter:
    def __init__(self, db_path="data/data.db", output_dir="exports"):
        """
        Inicializa o exportador CSV.
        """
        self.db_path = db_path
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    @staticmethod
    def export_to_csv(output_dir="exports", db_path="data.db"):
        """
        Exporta os dados do SQLite para um arquivo CSV.
        """
        os.makedirs(output_dir, exist_ok=True)  # Cria o diretório se não existir
        output_file = os.path.join(output_dir, "gini_data.csv")

        db = SQLiteDB(db_path)
        data = db.fetch_all()
        db.close()

        with open(output_file, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["ID", "Region", "Year", "Gini Index"])  # Cabeçalhos
            writer.writerows(data)

        print(f"Dados exportados para {output_file}")
