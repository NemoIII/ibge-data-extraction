# IBGE Data Extraction

Este projeto extrai dados do IBGE em arquivos `.xls` compactados, processa os dados, salva-os em um banco de dados SQLite e os exporta para um arquivo CSV.

## Tecnologias
- Python
- SQLite
- Docker (opcional)
- pytest (para testes)

## Como Rodar

### Sem Docker
1. Crie um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate

2. Instale as dependências:
  ```bash
   pip install -r requirements.txt

3. Rode a aplicação:
  ```bash
  python main.py

### Com Docker
1. Construa os containers:
  ```bash
  docker-compose build

2. Inicie os serviços:
  ```bash
  docker-compose up