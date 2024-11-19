import os
import zipfile
import pandas as pd
import pytest
from services.processor import DataProcessor
from services.db import SQLiteDB


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
    yield db
    db.close()


@pytest.fixture
def sample_zip(tmp_path):
    """
    Cria um arquivo .zip temporário com arquivos .xls de exemplo.
    """
    zip_path = tmp_path / "test_data.zip"
    xls_data = pd.DataFrame(
        {0: ["Region 1", "Region 2", "Region 3"], 1: [0.45, 0.60, 0.75]}
    )
    xls_path = tmp_path / "sample.XLS"
    xls_data.to_excel(xls_path, index=False, header=False)

    with zipfile.ZipFile(zip_path, "w") as z:
        z.write(xls_path, arcname="sample.XLS")
    return str(zip_path)


def test_process_zip_and_save_to_db(sample_zip, db_path):
    """
    Testa o método process_zip_and_save_to_db para verificar se os dados são extraídos e salvos corretamente no banco.
    """
    DataProcessor.process_zip_and_save_to_db(sample_zip, db_path)
    db = SQLiteDB(db_path)
    result = db.fetch_all()

    # Verifique se os dados foram salvos corretamente
    assert len(result) == 3
    assert result[0][1] == "Region 1"
    assert result[0][2] == 1991  # Ano fixo
    assert result[0][3] == 0.45


def test_process_dataframe(test_db):
    """
    Testa o método process_dataframe para verificar o processamento de um DataFrame.
    """
    df = pd.DataFrame({0: ["Region 1", "Region 2", "Region 3"], 1: [0.45, 0.60, 0.75]})
    DataProcessor.process_dataframe(df, test_db)
    result = test_db.fetch_all()

    # Verifique se os dados foram salvos corretamente
    assert len(result) == 3
    assert result[1][1] == "Region 2"
    assert result[1][2] == 1991
    assert result[1][3] == 0.60


def test_process_empty_dataframe(test_db):
    """
    Testa o processamento de um DataFrame vazio.
    """
    df = pd.DataFrame()
    DataProcessor.process_dataframe(df, test_db)

    # Nenhum dado deve ser salvo
    result = test_db.fetch_all()
    assert len(result) == 0


def test_process_invalid_data(test_db):
    """
    Testa o processamento de um DataFrame com dados inválidos.
    """
    df = pd.DataFrame({0: ["Region 1", None, "Region 3"], 1: [0.45, 0.60, None]})
    DataProcessor.process_dataframe(df, test_db)
    result = test_db.fetch_all()

    # Apenas os dados válidos devem ser salvos
    assert len(result) == 1
    assert result[0][1] == "Region 1"
    assert result[0][2] == 1991
    assert result[0][3] == 0.45
