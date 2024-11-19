import os
import sqlite3
import pytest
from services.db import SQLiteDB


@pytest.fixture
def temp_db():
    """
    Fixture para criar um banco de dados temporário.
    """
    db_path = "test_data.db"
    db = SQLiteDB(db_path)
    yield db
    db.close()
    if os.path.exists(db_path):
        os.remove(db_path)


def test_create_table(temp_db):
    """
    Testa se a tabela `gini_data` é criada corretamente.
    """
    query = "SELECT name FROM sqlite_master WHERE type='table' AND name='gini_data';"
    cursor = temp_db.conn.execute(query)
    result = cursor.fetchone()
    assert result is not None, "Tabela 'gini_data' não foi criada corretamente."


def test_insert_invalid_data(temp_db):
    """
    Testa a tentativa de inserir dados inválidos na tabela.
    """
    with pytest.raises(Exception):
        temp_db.insert_data(None, 1991, 0.55)  # Região inválida
    with pytest.raises(Exception):
        temp_db.insert_data("Test Region", "1991", 0.55)  # Ano inválido
    with pytest.raises(Exception):
        temp_db.insert_data("Test Region", 1991, "invalid")  # Índice de Gini inválido


def test_fetch_all(temp_db):
    """
    Testa a recuperação de todos os registros da tabela.
    """
    # Inserir múltiplos registros
    temp_db.insert_data("Region 1", 1990, 0.45)
    temp_db.insert_data("Region 2", 1991, 0.55)
    temp_db.insert_data("Region 3", 1992, 0.65)

    records = temp_db.fetch_all()
    assert len(records) == 3, "Número incorreto de registros recuperados."
    assert records[1][1] == "Region 2", "Região recuperada incorretamente."
    assert records[2][2] == 1992, "Ano recuperado incorretamente."
    assert records[0][3] == 0.45, "Índice de Gini recuperado incorretamente."


def test_close_connection(temp_db):
    """
    Testa se a conexão com o banco de dados é fechada corretamente.
    """
    temp_db.close()
    with pytest.raises(sqlite3.ProgrammingError):
        temp_db.conn.execute("SELECT * FROM gini_data;")
