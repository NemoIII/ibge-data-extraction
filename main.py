from services.downloader import IBGEDownloader


def main():
    downloader = IBGEDownloader(output_dir="downloads")

    print("Iniciando processo de navegação e download...")
    downloader.get_links_with_selenium()
    print("Processo concluído.")


if __name__ == "__main__":
    main()
