# Base image com Python
FROM python:3.11-slim

# Definir diretório de trabalho
WORKDIR /app

# Copiar arquivos de dependência
COPY requirements.txt .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo o código da aplicação
COPY . .

# Expor a porta padrão (caso a aplicação use porta específica, ajuste aqui)
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["python", "main.py"]