import sqlite3
import os


class SQLiteDB:
    def __init__(self, db_path="data.db"):
        """
        Inicializa a conexão com o banco SQLite.
        Cria o diretório do banco de dados, caso necessário.
        """
        # Cria o diretório do banco de dados (se especificado)
        db_dir = os.path.dirname(db_path)
        if db_dir:  # Apenas cria se houver um diretório no caminho
            os.makedirs(db_dir, exist_ok=True)

        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.create_table()  # Cria a tabela se ela ainda não existir

    def create_table(self):
        """
        Cria a tabela 'gini_data' no banco de dados.
        Essa tabela armazena informações processadas sobre o índice de Gini.
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
        # Validação explícita dos tipos de dados
        if not isinstance(region, str):
            raise ValueError(f"Região inválida: {region}")
        if not isinstance(year, int):
            raise ValueError(f"Ano inválido: {year}")
        if not isinstance(gini_index, (int, float)):
            raise ValueError(f"Índice de Gini inválido: {gini_index}")

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
