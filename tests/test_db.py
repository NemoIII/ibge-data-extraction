import unittest
import os
import sqlite3

from services.db import SQLiteDB


class TestSQLiteDB(unittest.TestCase):
    def setUp(self):
        """
        Configuração antes de cada teste.
        Cria um banco de dados temporário em memória.
        """
        self.db_path = "test_data.db"
        self.db = SQLiteDB(self.db_path)

    def tearDown(self):
        """
        Limpeza após cada teste.
        Fecha a conexão e remove o banco de dados.
        """
        self.db.close()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_create_table(self):
        """
        Testa se a tabela `gini_data` é criada corretamente.
        """
        query = (
            "SELECT name FROM sqlite_master WHERE type='table' AND name='gini_data';"
        )
        cursor = self.db.conn.execute(query)
        result = cursor.fetchone()
        self.assertIsNotNone(result, "Tabela 'gini_data' não foi criada corretamente.")

    def test_insert_invalid_data(self):
        """
        Testa a tentativa de inserir dados inválidos na tabela.
        """
        # Região inválida
        with self.assertRaises(ValueError) as context:
            self.db.insert_data(None, 1991, 0.55)
        self.assertIn("Região inválida", str(context.exception))

        # Ano inválido
        with self.assertRaises(ValueError) as context:
            self.db.insert_data("Test Region", "1991", 0.55)
        self.assertIn("Ano inválido", str(context.exception))

        # Índice de Gini inválido
        with self.assertRaises(ValueError) as context:
            self.db.insert_data("Test Region", 1991, "invalid")
        self.assertIn("Índice de Gini inválido", str(context.exception))

    def test_fetch_all(self):
        """
        Testa a recuperação de todos os registros da tabela.
        """
        # Inserir múltiplos registros
        self.db.insert_data("Region 1", 1990, 0.45)
        self.db.insert_data("Region 2", 1991, 0.55)
        self.db.insert_data("Region 3", 1992, 0.65)

        records = self.db.fetch_all()
        self.assertEqual(len(records), 3, "Número incorreto de registros recuperados.")
        self.assertEqual(records[1][1], "Region 2", "Região recuperada incorretamente.")
        self.assertEqual(records[2][2], 1992, "Ano recuperado incorretamente.")
        self.assertEqual(
            records[0][3], 0.45, "Índice de Gini recuperado incorretamente."
        )

    def test_insert_invalid_data(self):
        """
        Testa a tentativa de inserir dados inválidos na tabela.
        """
        with self.assertRaises(Exception):
            self.db.insert_data(None, 1991, 0.55)  # Região inválida
        with self.assertRaises(Exception):
            self.db.insert_data("Test Region", "1991", 0.55)  # Ano inválido
        with self.assertRaises(Exception):
            self.db.insert_data(
                "Test Region", 1991, "invalid"
            )  # Índice de Gini inválido

    def test_close_connection(self):
        """
        Testa se a conexão com o banco de dados é fechada corretamente.
        """
        self.db.close()
        with self.assertRaises(sqlite3.ProgrammingError):
            self.db.conn.execute("SELECT * FROM gini_data;")
