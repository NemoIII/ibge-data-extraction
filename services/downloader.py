import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


class IBGEDownloader:
    BASE_URL = "https://www.ibge.gov.br/estatisticas/downloads-estatisticas.html"

    def __init__(self, output_dir="downloads"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def get_links_with_selenium(self):
        """
        Configura o WebDriver, navega no site do IBGE e realiza os downloads diretamente.
        """
        # Configurar opções do ChromeDriver para downloads
        chrome_options = Options()
        prefs = {
            "download.default_directory": os.path.abspath(self.output_dir),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
        }
        chrome_options.add_experimental_option("prefs", prefs)

        # Iniciar o WebDriver
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(self.BASE_URL)

        # Esperar que a página carregue completamente
        wait = WebDriverWait(driver, 20)

        try:
            # Fechar o banner de cookies, se existir
            try:
                cookie_button = wait.until(
                    EC.element_to_be_clickable((By.ID, "cookie-btn"))
                )
                print("Aceitando os cookies...")
                cookie_button.click()
            except Exception:
                print("Banner de cookies não encontrado ou já fechado.")

            # Navegar pelas pastas
            self.click_folder(wait, driver, "Censos_anchor", "Censos")
            self.click_folder(
                wait,
                driver,
                "Censos/Censo_Demografico_1991_anchor",
                "Censo_Demografico_1991",
            )
            self.click_folder(
                wait,
                driver,
                "Censos/Censo_Demografico_1991/Indice_de_Gini_anchor",
                "Indice_de_Gini",
            )

            # Localizar links e simular cliques
            zip_links = wait.until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "jstree-anchor"))
            )
            print(f"Links encontrados: {len(zip_links)}")

            for elem in zip_links:
                text = elem.text.strip()
                if text.endswith(".zip"):  # Garantir que é um arquivo .zip
                    print(f"Baixando: {text}")
                    try:
                        elem.click()
                    except Exception:
                        print("Tentando forçar o clique com JavaScript.")
                        driver.execute_script("arguments[0].click();", elem)
                    time.sleep(2)  # Aguardar para evitar sobreposição de cliques

        except Exception as e:
            print(f"Erro durante a navegação ou download: {e}")
        finally:
            driver.quit()

    def click_folder(self, wait, driver, folder_id, folder_name):
        """
        Clica em uma pasta específica no site do IBGE.
        """
        try:
            folder = wait.until(EC.presence_of_element_located((By.ID, folder_id)))
            print(f"Clicando na pasta '{folder_name}'")
            folder.click()
        except Exception:
            print(f"Tentando forçar o clique na pasta '{folder_name}' com JavaScript.")
            driver.execute_script("arguments[0].click();", folder)
