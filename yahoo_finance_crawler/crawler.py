from yahoo_finance_crawler.csv_exporter import CSVExporter
from yahoo_finance_crawler.data_processor import DataProcessor
from yahoo_finance_crawler.selenium_scraper import SeleniumScraper


class YahooFinanceCrawler:
    def __init__(self, region: str):
        self._region = region
        self._data = None
        self._scraper = SeleniumScraper(region)
        self._data_processor = DataProcessor(self._scraper.driver)

    def run(self):
        try:
            self._scraper.fetch_html()
            self._data = self._data_processor.scrape_all_pages(
                self._scraper.current_url, end_page=self._scraper.count
            )
            if self._data:
                CSVExporter.export_to_csv(self._data, 'yahoo_finance_data.csv')
            else:
                print('Nenhum dado encontrado para exportar.')
        except Exception as e:
            print(f'Erro ao executar o crawler: {e}')
