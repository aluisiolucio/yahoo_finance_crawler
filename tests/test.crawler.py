from unittest.mock import patch

from yahoo_finance_crawler.crawler import YahooFinanceCrawler


@patch("yahoo_finance_crawler.selenium_scraper.SeleniumScraper.fetch_html")
@patch("yahoo_finance_crawler.data_processor.DataProcessor.scrape_all_pages")
@patch("yahoo_finance_crawler.csv_exporter.CSVExporter.export_to_csv")
def test_crawler_run(mock_export, mock_scrape, mock_fetch):
    mock_scrape.return_value = [
        {
            "symbol": "AMX.BA",
            "name": "América Móvil, S.A.B. de C.V.",
            "price": "2089.00"
        },
        {
            "symbol": "NOKA.BA",
            "name": "Nokia Corporation",
            "price": "557.50"
        },
    ]
    crawler = YahooFinanceCrawler("Argentina")

    crawler.run()

    mock_fetch.assert_called_once()
    mock_scrape.assert_called_once_with(
        mock_fetch.return_value,
        end_page=mock_fetch.return_value.count
    )
    mock_export.assert_called_once_with(
        mock_scrape.return_value,
        'yahoo_finance_data.csv'
    )
