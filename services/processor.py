import zipfile
import pandas as pd
from services.db import SQLiteDB


class DataProcessor:
    @staticmethod
    def process_zip_and_save_to_db(zip_path, db_path="data.db"):
        """
        Processa arquivos .zip contendo dados em formato .xls.
        Extraímos os dados, processamos e salvamos no banco de dados SQLite.

        Parâmetros:
            - zip_path (str): Caminho para o arquivo .zip.
            - db_path (str): Caminho do banco de dados SQLite.
        """
        # Inicializa a conexão com o banco de dados
        db = SQLiteDB(db_path)

        # Extrai todos os arquivos do arquivo zip
        with zipfile.ZipFile(zip_path, "r") as z:
            file_names = z.namelist()
            for file_name in file_names:
                if file_name.endswith(".XLS"):  # Verifica se o arquivo é um Excel
                    print(f"Processando: {file_name}")
                    with z.open(file_name) as file:
                        try:
                            # Lê o arquivo Excel sem cabeçalhos
                            df = pd.read_excel(file, header=None)
                            DataProcessor.process_dataframe(df, db)
                        except Exception as e:
                            print(f"Erro ao processar {file_name}: {e}")

        # Fecha a conexão com o banco de dados
        db.close()

    @staticmethod
    def process_dataframe(df, db):
        """
        Processa um DataFrame extraído de um arquivo .xls e salva no banco de dados.
        """
        # Verificar se o DataFrame não está vazio
        if df.empty:
            print("DataFrame vazio. Nenhum dado para processar.")
            return

        # Definir o ano fixo (ou dinamicamente extraído)
        year = 1991

        for index, row in df.iterrows():
            try:
                # Extração e limpeza dos dados
                region = row[0]
                gini_index = row[1]

                # Validar 'region'
                if pd.isna(region) or not isinstance(region, str):
                    print(f"[Linha {index}] Região inválida: {region}. Ignorando.")
                    continue
                region = region.strip()

                # Validar e converter 'gini_index'
                if pd.isna(gini_index) or not isinstance(gini_index, (int, float)):
                    raise ValueError(
                        f"[Linha {index}] Índice de Gini inválido: {gini_index}"
                    )
                gini_index = float(gini_index)

                # Garantir que o ano seja válido
                if not isinstance(year, int):
                    raise ValueError(f"[Linha {index}] Ano inválido: {year}")

                # Salvar no banco de dados
                db.insert_data(region=region, year=year, gini_index=gini_index)

            except Exception as e:
                print(f"[Linha {index}] Erro ao processar dados: {e}")
