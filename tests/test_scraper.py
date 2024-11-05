from unittest.mock import MagicMock, patch

from yahoo_finance_crawler.selenium_scraper import (
    FIND_STOCKS_BUTTON,
    SeleniumScraper,
)


@patch("selenium.webdriver.Chrome")
def test_initialize_driver(mock_driver):
    scraper = SeleniumScraper("Argentina")
    assert scraper._driver == mock_driver.return_value


@patch("yahoo_finance_crawler.selenium_scraper.SeleniumScraper._load_page")
@patch("yahoo_finance_crawler.selenium_scraper.SeleniumScraper._set_region_filter")
@patch("yahoo_finance_crawler.selenium_scraper.SeleniumScraper._click_element")
@patch(
    "yahoo_finance_crawler.selenium_scraper.extract_numbers",
    return_value=[0, 0, 2]
)
def test_fetch_html(mock_extract, mock_click, mock_set_filter, mock_load_page):
    scraper = SeleniumScraper("Argentina")
    scraper._driver = MagicMock()

    scraper.fetch_html()

    mock_load_page.assert_called_once()
    mock_set_filter.assert_called_once()
    mock_click.assert_called_with(FIND_STOCKS_BUTTON)
    mock_extract.assert_called_once()
