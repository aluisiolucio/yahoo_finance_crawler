import argparse

from csv_exporter import CSVExporter
from data_processor import DataProcessor
from selenium_scraper import SeleniumScraper

parser = argparse.ArgumentParser(description='Descrição do seu script.')
parser.add_argument(
    'region',
    type=str,
    help='O nome da região para ser usado como filtro de busca.'
)
args = parser.parse_args()

if __name__ == '__main__':
    try:
        region = args.region.lower()

        sc = SeleniumScraper(region)
        sc.fetch_html()

        bs = DataProcessor()
        data = bs.scrape_all_pages(sc.current_url, end_page=sc.cout)

        CSVExporter.export_to_csv(data, 'yahoo_finance_data.csv')
    except KeyboardInterrupt:
        print('\nPrograma interrompido pelo usuário')
    except FileNotFoundError:
        print('Arquivo não encontrado')
    except Exception as e:
        print(e)
