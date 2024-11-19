import zipfile
import pandas as pd
from services.db import SQLiteDB


class DataProcessor:
    @staticmethod
    def process_zip_and_save_to_db(zip_path, db_path="data.db"):
        """
        Processa arquivos .zip, extrai os dados de arquivos .xls e salva no banco de dados.
        """
        # Conectar ao banco de dados
        db = SQLiteDB(db_path)

        # Extrair arquivos do .zip
        with zipfile.ZipFile(zip_path, "r") as z:
            file_names = z.namelist()
            for file_name in file_names:
                if file_name.endswith(".XLS"):  # Verificar se o arquivo é .xls
                    print(f"Processando: {file_name}")
                    with z.open(file_name) as file:
                        # Ler o arquivo .xls com pandas
                        try:
                            df = pd.read_excel(file, header=None)  # Sem cabeçalhos
                            DataProcessor.process_dataframe(df, db)
                        except Exception as e:
                            print(f"Erro ao processar {file_name}: {e}")

        # Fechar a conexão com o banco de dados
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
