import time

from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError, Timeout
from selenium.common.exceptions import TimeoutException

from yahoo_finance_crawler.utils import display_progress_bar


class DataProcessor:
    def __init__(self, scraper):
        self._scraper = scraper

    def parse_html(self):
        pass

    def _fetch_url(self, url, retries=3):
        for i in range(retries):
            try:
                self._scraper.get(url)
                return self._scraper.page_source
            except (ConnectionError, Timeout) as e:
                print(f'Tentativa {i + 1} falhou: {e}')
                time.sleep(3)
            except TimeoutException:
                return self._scraper.page_source
            except Exception as e:
                print(f'Erro ao acessar a URL: {e}')
                break

        return None

    def _scrape_page(self, url):
        html = self._fetch_url(url)

        if not html:
            print(f'Não foi possível acessar a URL {url} em 3 tentativas')
            return []

        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table', class_='W(100%)')

        if not table:
            print('Não foi possível encontrar a tabela')
            return []

        tbody = table.find('tbody')

        data = []

        rows = tbody.find_all('tr')
        for row in rows:
            col_symbol = row.find_all('td')[0]
            col_name = row.find_all('td')[1]
            col_price = row.find_all('td')[2]

            if col_symbol and col_name and col_price:
                symbol = col_symbol.get_text()
                name = col_name.get_text()
                price = col_price.get_text()

                data.append({'symbol': symbol, 'name': name, 'price': price})

        return data

    def scrape_all_pages(self, base_url, start_page=0, end_page=None):
        all_data = []
        page = start_page

        while True:
            url = f'{base_url}?count=100&offset={page}'
            display_progress_bar(page, end_page)

            data = self._scrape_page(url)
            if end_page and page > end_page:
                break

            all_data.extend(data)
            time.sleep(3)

            page += 100

        self._scraper.quit()

        return all_data
