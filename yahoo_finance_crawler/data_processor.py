import platform
import time

import requests
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError, Timeout


class DataProcessor:
    def parse_html(self):
        pass

    @staticmethod
    def _fetch_url(url, headers=None, retries=3):
        for i in range(retries):
            try:
                response = requests.get(url, headers=headers, timeout=15)
                response.raise_for_status()

                return response
            except (ConnectionError, Timeout) as e:
                print(f"Tentativa {i + 1} falhou: {e}")
                time.sleep(3)

        return None

    def _scrape_page(self, url):
        user_gent = ""
        if platform.system() == "Windows":
            user_gent = (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                '(KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
            )
        elif platform.system() == "Linux":
            user_gent = (
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                '(KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
            )

        headers = {'User-Agent': user_gent}
        response = self._fetch_url(url, headers=headers)

        if not response:
            print(f"Não foi possível acessar a URL {url} em 3 tentativas")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')

        table = soup.find('table', class_='W(100%)')

        if not table:
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
            url = f"{base_url}?count=100&offset={page}"
            print(f"Scraping {url}")

            data = self._scrape_page(url)
            if (end_page and page > end_page):
                break

            all_data.extend(data)
            time.sleep(3)

            page += 100

        return all_data
