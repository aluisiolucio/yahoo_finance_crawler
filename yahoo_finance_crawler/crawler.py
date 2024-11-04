from csv_exporter import CSVExporter
from data_processor import DataProcessor
from selenium_scraper import SeleniumScraper


class YahooFinanceCrawler:
    def __init__(self, region: str):
        self._region = region
        self._data = None
        self._scraper = SeleniumScraper(region)
        self._data_processor = DataProcessor()

    def run(self):
        self._scraper.fetch_html()
        self._data = self._data_processor.scrape_all_pages(
            self._scraper.current_url, end_page=self._scraper.count
        )

        CSVExporter.export_to_csv(self._data, 'yahoo_finance_data.csv')
