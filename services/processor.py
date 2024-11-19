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

        # Iterar sobre as linhas e salvar no banco de dados
        for index, row in df.iterrows():
            # Supondo que as colunas de interesse são A (região) e B (índice de Gini)
            if index == 0:  # Ignorar a primeira linha se for título global
                continue

            region = row[0]  # Primeira coluna
            gini_index = row[1]  # Segunda coluna
            year = 1991  # Ano fixo (ou extraído dinamicamente)

            # Verificar se a região é válida
            if pd.isna(region) or not isinstance(region, str):
                print(f"Valor inválido encontrado na região: {region}. Ignorando.")
                continue

            # Limpeza e validação do índice de Gini
            try:
                if pd.isna(gini_index) or not isinstance(gini_index, (int, float)):
                    raise ValueError(f"Índice de Gini inválido: {gini_index}")
                gini_index = float(gini_index)
            except (ValueError, TypeError):
                print(
                    f"Valor inválido encontrado: {region} ou {gini_index}. Ignorando."
                )
                continue

            # Garantir que o ano seja convertido para inteiro
            try:
                year = int(year)  # Converte explicitamente o ano para inteiro
                if not isinstance(year, int):
                    raise ValueError(f"Valor de year não é inteiro: {year}")
            except ValueError:
                print(f"Erro ao converter o ano: {year}. Ignorando {region}.")
                continue

            # Salvar no banco de dados
            try:
                db.insert_data(
                    region=region.strip(), year=int(year), gini_index=gini_index
                )
            except Exception as e:
                print(f"Erro ao salvar no banco para {region}: {e}")
