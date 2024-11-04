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
    def __init__(self, region: str):
        self._region = region
        self._base_url = 'https://finance.yahoo.com/screener/new'
        self._current_url = ''
        self._count = 0
        self._driver = self._initialize_driver()

    @property
    def current_url(self) -> str:
        return self._current_url

    @property
    def count(self) -> int:
        return self._count

    @staticmethod
    def _initialize_driver() -> webdriver.Chrome:
        service = Service(ChromeDriverManager().install())

        chrome_options = Options()
        chrome_options.add_argument('profile.managed_default_content_settings.images=2')
        # chrome_options.add_argument("--headless=new")

        return webdriver.Chrome(service=service, options=chrome_options)

    def _load_page(self):
        self._driver.set_page_load_timeout(15)
        try:
            self._driver.get(self._base_url)
        except TimeoutException:
            pass

    def _click_element(self, xpath: str):
        element = WebDriverWait(self._driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        element.click()

    def _input_text(self, xpath: str, text: str):
        input_element = WebDriverWait(self._driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, xpath))
        )
        input_element.send_keys(text)

    def _reload_required(self) -> bool:
        return any(
            self._driver.find_elements(By.XPATH, span)
            for span in [RELOAD_MESSAGE_FILTER_SPAN, RELOAD_MESSAGE_DATA_SPAN]
        )

    def _set_region_filter(self):
        self._click_element(SELECTED_REGION_BUTTON)
        self._click_element(REGION_SELECT_BUTTON)
        self._input_text(FILTER_REGION_INPUT, self._region)

        region_label = WebDriverWait(self._driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, REGION_LABEL))
        )
        region_checkbox = region_label.find_element(
            By.XPATH, f"//span[text()='{self._region.title()}']"
        )
        region_checkbox.click()

    def fetch_html(self):
        try:
            self._load_page()
            self._set_region_filter()
            self._click_element(FIND_STOCKS_BUTTON)

            if self._reload_required():
                self.fetch_html()
                return

            WebDriverWait(self._driver, 20).until(
                EC.presence_of_element_located((By.XPATH, TABLE_OF_STOCKS))
            )

            results_text = self._driver.find_element(
                By.XPATH, RESULTS_SPAN
            ).text
            self._count = extract_numbers(results_text)[2]
            self._current_url = self._driver.current_url
        finally:
            self._driver.quit()
