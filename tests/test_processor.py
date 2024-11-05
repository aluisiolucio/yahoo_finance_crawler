from unittest.mock import MagicMock, patch

from yahoo_finance_crawler.data_processor import DataProcessor
from yahoo_finance_crawler.selenium_scraper import SeleniumScraper

HTML_EXAMPLE = """
<table class="W(100%)"><tbody>
<tr><td>AMX.BA</td><td>América Móvil, S.A.B. de C.V.</td><td>2089.00</td></tr>
<tr><td>NOKA.BA</td><td>Nokia Corporation</td><td>557.50</td></tr>
</tbody></table>
"""


def test_fetch_url():
    mock_driver = MagicMock()
    mock_driver.page_source = HTML_EXAMPLE

    with patch(
        "yahoo_finance_crawler.selenium_scraper.SeleniumScraper._initialize_driver",
        return_value=mock_driver
    ):
        scraper = SeleniumScraper("Argentina")
        processor = DataProcessor(scraper=scraper.driver)

        response_html = processor._fetch_url("https://fakeurl.com")

        assert response_html == HTML_EXAMPLE
        mock_driver.get.assert_called_once_with("https://fakeurl.com")


def test_scrape_page():
    mock_driver = MagicMock()
    mock_driver.page_source = HTML_EXAMPLE

    with patch(
        "yahoo_finance_crawler.selenium_scraper.SeleniumScraper._initialize_driver",
        return_value=mock_driver
    ):
        scraper = SeleniumScraper("Argentina")
        processor = DataProcessor(scraper=scraper.driver)

        data = processor._scrape_page("https://fakeurl.com")

        assert data == [
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
        mock_driver.get.assert_called_once_with("https://fakeurl.com")
