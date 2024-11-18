import os
import pytest
from unittest.mock import MagicMock, patch
from services.downloader import IBGEDownloader


@pytest.fixture
def downloader():
    """
    Fixture para criar uma instância do IBGEDownloader.
    """
    return IBGEDownloader(output_dir="test_downloads")


def test_initialization(downloader):
    """
    Testa se o diretório de saída é criado corretamente.
    """
    assert downloader.output_dir == "test_downloads"
    assert os.path.exists(downloader.output_dir)
    os.rmdir(downloader.output_dir)  # Remove o diretório após o teste


@patch("services.downloader.webdriver.Chrome")
def test_click_folder(mock_driver, downloader):
    """
    Testa se a função click_folder interage corretamente com o Selenium.
    """
    # Mock do WebDriver e WebDriverWait
    mock_wait = MagicMock()
    mock_folder = MagicMock()

    # Configurar o mock para simular o elemento encontrado
    mock_wait.until.return_value = mock_folder

    # Simular comportamento do clique no elemento
    mock_folder.click = MagicMock()

    # Executar o método
    downloader.click_folder(mock_wait, mock_driver, "test_id", "Test Folder")

    # Verificar se o clique foi chamado
    mock_folder.click.assert_called_once()


@patch("services.downloader.webdriver.Chrome")
@patch("services.downloader.WebDriverWait")
def test_get_links_with_selenium(mock_wait, mock_driver, downloader):
    """
    Testa se get_links_with_selenium encontra e clica nos links corretamente.
    """
    # Configurar mocks
    mock_driver_instance = mock_driver.return_value
    mock_element = MagicMock()
    mock_element.text = "Acre.zip"
    mock_element.get_attribute.return_value = "https://example.com/Acre.zip"

    # Mock para WebDriverWait e elementos da página
    mock_wait.return_value.until.side_effect = [
        None,  # Cookie banner
        None,  # Primeiro clique
        None,  # Segundo clique
        None,  # Terceiro clique
        [mock_element],  # Links encontrados
    ]

    # Mock do clique no elemento
    mock_element.click = MagicMock()

    # Executar o método
    downloader.get_links_with_selenium()

    # Verificar se o elemento foi clicado
    mock_element.click.assert_called_once()

    # Verificar se o WebDriver foi encerrado
    mock_driver_instance.quit.assert_called_once()
