import sqlite3
import os


class SQLiteDB:
    def __init__(self, db_path="data.db"):
        """
        Inicializa a conexão com o banco SQLite.
        """
        # Cria o diretório do banco de dados, se necessário
        db_dir = os.path.dirname(db_path)
        if db_dir:  # Apenas cria se houver um diretório no caminho
            os.makedirs(db_dir, exist_ok=True)

        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.create_table()

    def create_table(self):
        """
        Cria a tabela para armazenar os dados do índice de Gini.
        """
        query = """
        CREATE TABLE IF NOT EXISTS gini_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            region TEXT NOT NULL,
            year INTEGER NOT NULL,
            gini_index REAL NOT NULL
        );
        """
        self.conn.execute(query)
        self.conn.commit()

    def insert_data(self, region, year, gini_index):
        """
        Insere um registro no banco de dados.
        """
        query = "INSERT INTO gini_data (region, year, gini_index) VALUES (?, ?, ?);"
        self.conn.execute(query, (region, year, gini_index))
        self.conn.commit()

    def fetch_all(self):
        """
        Recupera todos os dados da tabela.
        """
        query = "SELECT * FROM gini_data;"
        cursor = self.conn.execute(query)
        return cursor.fetchall()

    def close(self):
        """
        Fecha a conexão com o banco de dados.
        """
        self.conn.close()
