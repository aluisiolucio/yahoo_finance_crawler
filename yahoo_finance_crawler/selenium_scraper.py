import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from utils import extract_numbers
from webdriver_manager.chrome import ChromeDriverManager

SELECTED_REGION_BUTTON = (
    '//*[@id="screener-criteria"]/div[2]/div[1]/div[1]/div[1]/div/div[2]/ul/li[1]/button'
)
REGION_SELECT_BUTTON = (
    '//*[@id="screener-criteria"]/div[2]/div[1]/div[1]/div[1]/div/div[2]/ul/li/button'
)
FILTER_REGION_INPUT = '//*[@id="dropdown-menu"]/div/div[1]/div/input'
REGION_LABEL = 'label[class="Ta(c) Pos(r) Va(tb) Pend(10px)"]'
FIND_STOCKS_BUTTON = (
    '//*[@id="screener-criteria"]/div[2]/div[1]/div[3]/button[1]'
)
TABLE_OF_STOCKS = '//*[@id="scr-res-table"]/div[1]/table'
RESULTS_SPAN = '//*[@id="fin-scr-res-table"]/div[1]/div[1]/span[2]/span'
RELOAD_MESSAGE_FILTER_SPAN = (
    '//*[@id="screener-criteria"]/div[2]/div/div[2]/span'
)
RELOAD_MESSAGE_DATA_SPAN = '//*[@id="fin-scr-res-table"]/div[2]/div[2]/span'


class SeleniumScraper:
    def __init__(self, region):
        self._region = region
        self._base_url = 'https://finance.yahoo.com/screener/new'
        self._current_url = ''
        self._cout = 0

    @property
    def current_url(self) -> str:
        return self._current_url

    @property
    def cout(self) -> str:
        return self._cout

    @staticmethod
    def _get_chrome_driver():
        service = Service(ChromeDriverManager().install())

        chrome_options = Options()
        chrome_options.add_argument(
            'profile.managed_default_content_settings.images=2'
        )
        # chrome_options.add_argument("--headless=new")

        return webdriver.Chrome(service=service, options=chrome_options)

    @staticmethod
    def _wait_for_page_load_script(driver):
        while (
            driver.execute_script('return document.readyState') != 'complete'
        ):
            time.sleep(0.5)

    @staticmethod
    def _wait_for_page_load_webdriver(driver):
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, SELECTED_REGION_BUTTON))
        )

    @staticmethod
    def _wait_for_page_load_implicitly(driver):
        driver.implicitly_wait(10)

    @staticmethod
    def _wait_for_page_load():
        time.sleep(10)

    @staticmethod
    def _reload_page_if_necessary(driver):
        reload_msg_filter_span = driver.find_elements(
            By.XPATH, RELOAD_MESSAGE_FILTER_SPAN
        )
        reload_msg_data_span = driver.find_elements(
            By.XPATH, RELOAD_MESSAGE_DATA_SPAN
        )

        return len(reload_msg_filter_span) > 0 or len(reload_msg_data_span) > 0

    def fetch_html(self):
        driver = self._get_chrome_driver()
        try:
            driver.set_page_load_timeout(20)

            try:
                driver.get(self._base_url)
            except TimeoutException:
                pass

            selected_region_btn = driver.find_element(
                By.XPATH, SELECTED_REGION_BUTTON
            )
            selected_region_btn.click()

            region_select_btn = driver.find_element(
                By.XPATH, REGION_SELECT_BUTTON
            )
            region_select_btn.click()

            filter_region_input = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, FILTER_REGION_INPUT)
                )
            )
            filter_region_input.send_keys(self._region)

            region_label = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, REGION_LABEL))
            )
            region_checkbox = region_label.find_element(
                By.XPATH, f"//span[text()='{self._region.title()}']"
            )
            region_checkbox.click()

            find_stocks_btn = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, FIND_STOCKS_BUTTON))
            )
            find_stocks_btn.click()

            if self._reload_page_if_necessary(driver):
                self.fetch_html()
                return

            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, TABLE_OF_STOCKS))
            )

            results_span = driver.find_element(By.XPATH, RESULTS_SPAN)
            self._cout = extract_numbers(results_span.text)[2]

            self._current_url = driver.current_url

            time.sleep(10)
        finally:
            driver.quit()
