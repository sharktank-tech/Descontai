import requests
from bs4 import BeautifulSoup
import time


class AmazonScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }

    def scrape_product(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extrair informações do produto
            title = soup.select_one('#productTitle').get_text().strip()
            current_price = float(soup.select_one('.priceToPay span').get_text()[1:])
            original_price = float(soup.select_one('.priceBlockStrikePriceString').get_text()[1:])

            discount = round(((original_price - current_price) / original_price) * 100, 2)

            return {
                'title': title,
                'current_price': current_price,
                'original_price': original_price,
                'discount': discount,
                'url': url
            }
        except Exception as e:
            print(f"Error scraping {url}: {str(e)}")
            return None