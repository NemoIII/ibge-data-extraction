import os
import csv
import pytest
from services.db import SQLiteDB
from services.export_csv import CSVExporter


@pytest.fixture
def db_path(tmp_path):
    """
    Cria um banco de dados temporário para os testes.
    """
    return os.path.join(tmp_path, "test_data.db")


@pytest.fixture
def test_db(db_path):
    """
    Fixture para instanciar e retornar um banco de dados SQLiteDB temporário.
    """
    db = SQLiteDB(db_path)
    # Inserir dados de exemplo no banco
    db.insert_data("Region 1", 1991, 0.45)
    db.insert_data("Region 2", 1991, 0.60)
    db.insert_data("Region 3", 1991, 0.75)
    yield db
    db.close()


@pytest.fixture
def output_dir(tmp_path):
    """
    Diretório temporário para exportação de arquivos CSV.
    """
    export_dir = os.path.join(tmp_path, "exports")
    os.makedirs(export_dir, exist_ok=True)
    return export_dir


def test_export_to_csv(test_db, output_dir, db_path):
    """
    Testa a exportação de dados do banco para um arquivo CSV.
    """
    # Exportar os dados do banco para CSV
    CSVExporter.export_to_csv(output_dir=output_dir, db_path=db_path)

    # Verificar se o arquivo CSV foi criado
    output_file = os.path.join(output_dir, "gini_data.csv")
    assert os.path.exists(output_file), f"O arquivo {output_file} não foi criado."

    # Ler o arquivo CSV exportado
    with open(output_file, "r") as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)

    # Verificar os cabeçalhos
    assert rows[0] == [
        "ID",
        "Region",
        "Year",
        "Gini Index",
    ], "Cabeçalhos do CSV estão incorretos."

    # Verificar os dados exportados
    assert rows[1:] == [
        ["1", "Region 1", "1991", "0.45"],
        ["2", "Region 2", "1991", "0.6"],
        ["3", "Region 3", "1991", "0.75"],
    ], "Os dados exportados estão incorretos."
