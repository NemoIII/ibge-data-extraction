from services.downloader import IBGEDownloader
from services.processor import DataProcessor
from services.export_csv import CSVExporter
import os


def main():
    # Diretório de downloads e banco de dados
    output_dir = "downloads"
    db_path = "data.db"  # Caminho do banco de dados
    export_dir = "exports"

    # Etapa 1: Realizar download dos arquivos .zip
    downloader = IBGEDownloader(output_dir=output_dir)
    downloader.get_links_with_selenium()

    # Etapa 2: Processar os arquivos baixados
    for file_name in os.listdir(output_dir):
        if file_name.endswith(".zip"):
            zip_path = os.path.join(output_dir, file_name)
            DataProcessor.process_zip_and_save_to_db(zip_path, db_path=db_path)

    # Etapa 3: Exportar os dados do banco para CSV
    CSVExporter.export_to_csv(output_dir=export_dir, db_path=db_path)


if __name__ == "__main__":
    main()
