# IBGE Data Extraction

Este projeto extrai dados do IBGE em arquivos `.xls` compactados, processa-os, salva-os em um banco de dados SQLite e os exporta para um arquivo CSV. Ele utiliza Selenium para automação de download e processamento de dados com Python.

---

## Tecnologias

- **Python**
- **SQLite**
- **Docker** (opcional)
- **pytest** (para testes)

---

## Principais Bibliotecas

- **Selenium**: Para automação de download de arquivos.
- **Pandas**: Para manipulação e processamento de dados.
- **SQLite 3**: Para armazenamento local dos dados processados.

---

### Selenium e o WebDriver

Como o Selenium é usado para realizar downloads automáticos, você precisa configurar o WebDriver para o navegador que você utilizará. Aqui estão os passos:

#### Links para Download do WebDriver
- [ChromeDriver (Google Chrome)](https://sites.google.com/chromium.org/driver/)
- [GeckoDriver (Mozilla Firefox)](https://github.com/mozilla/geckodriver/releases)
- [EdgeDriver (Microsoft Edge)](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)
- [SafariDriver (Apple Safari)](https://developer.apple.com/documentation/webkit/testing_with_webdriver_in_safari)

#### Instruções para Configuração

1. **Verifique a versão do navegador:**
   - Para Chrome: Vá até `chrome://settings/help` e veja a versão.
   - Para Firefox: Vá até `Menu > Ajuda > Sobre o Firefox`.
   - Para Edge: Vá até `Configurações > Sobre o Microsoft Edge`.

2. **Baixe o WebDriver correspondente** usando os links fornecidos acima.

3. **Adicione o WebDriver ao PATH do sistema:**
   - No Linux/Mac: Mova o executável para `/usr/local/bin`.
   - No Windows: Mova o executável para `C:\Windows` ou adicione o diretório ao PATH.

4. **Teste a instalação:**
   - Abra o terminal e execute:
     ```bash
     chromedriver --version
     ```
     ou
     ```bash
     geckodriver --version
     ```
     Isso deve retornar a versão do WebDriver instalado.

---

## Como Rodar o Projeto

### Sem Docker

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/NemoIII/ibge-data-extraction.git
   cd ibge-data-extraction

2. **Crie um ambiente virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate  # Windows

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt

4. **Configure o WebDriver conforme as instruções acima.**

5. **Execute a aplicação:**
   ```bash
   python main.py

6. **Exporte os dados para CSV (opcional):**
- Certifique-se de que os dados foram salvos no banco de dados.
- Rode o script de exportação:
   ```bash
   python export_csv.py


### Com Docker

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/NemoIII/ibge-data-extraction.git
   cd ibge-data-extraction

2. **Construa os containers:**
   ```bash
   docker-compose build

3. **Inicie os serviços:**
   ```bash
   docker-compose up

4. **Acompanhe os logs:**
-	Os logs do container mostram o progresso da aplicação.
-	Use Ctrl+C para finalizar o processo.

5. **Exporte os dados para CSV (opcional):**
-	Certifique-se de que o serviço foi finalizado corretamente.
-	Rode o container para exportar os dados:


### Testes

1. Para executar os testes automatizados do projeto, utilize o comando abaixo:
- Certifique-se de que todas as dependências estão instaladas e o ambiente virtual está ativado.
   ```bash
   pytest -v


### CI/CD

Este projeto utiliza GitHub Actions para CI/CD. Os testes e validações são executados automaticamente ao fazer commits ou abrir Pull Requests. Para garantir que seu código está conforme os padrões, utilize:
- pytest: Para garantir que os testes passem.
- flake8: Para validar o estilo do código:
   ```bash
   flake8 .


### Contribuição

Contribuições são bem-vindas! Siga as etapas abaixo:
1.	Faça um fork do repositório.
2.	Crie uma nova branch:
   ```bash
   git checkout -b feature/nova-feature

3.	Faça suas alterações e adicione os commits.
4.	Abra um Pull Request descrevendo suas mudanças.