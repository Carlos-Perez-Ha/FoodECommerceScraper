import bs4
import requests
from bs4 import BeautifulSoup
import logging
from utils import *
from typing import Tuple, List
import hashlib
import glob
import shutil


class DiaScraper:
    """
    Objeto para descargar información de la pagina de DIA
    """

    URLSiteMap = 'https://www.dia.es/sitemap.xml'

    logging.basicConfig(level=logging.INFO)

    def __init__(self):

        # Lista de paginas de producto del site
        self.listaPaginasProducto = []
        self.data_path = create_data_folder()

    @staticmethod
    def get_page(url: str) -> bs4.BeautifulSoup:
        """
        :param url:
        :return: Devuelve un objeto BeautifulSoup para operar con la pagina cargada
        """

        headers = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/107.0.0.0 Safari/537.36 '
        }

        session = requests.Session()

        page = session.get(url, headers=headers)

        soup = BeautifulSoup(page.content, features='xml')

        return soup

    @staticmethod
    def print_page(page: bs4.BeautifulSoup, ruta: str):
        """
        imprime la pagina escrapeada en la ruta correspondiente.

        :param page:
        :param ruta:
        :return:
        """
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(page.prettify())

    @staticmethod
    def obtain_name(page: bs4.BeautifulSoup) -> Tuple[str, str]:
        fetched_product = page.find_all("div", "product-name container-center")
        product_name = [preprocess_str(product.text) for product in fetched_product][0]
        brand = [process_brand(product.text) for product in fetched_product][0]
        return product_name, brand

    @staticmethod
    def obtain_price(page: bs4.BeautifulSoup) -> float:
        fetched_price = page.find_all("span", "big-price")
        price = [process_price(price.text) for price in fetched_price][0]
        return float(price)

    @staticmethod
    def obtain_categories(page: bs4.BeautifulSoup) -> List[str]:
        fetched_categories = page.find_all("span", itemprop="name")
        categories = [preprocess_str(category.text) for category in fetched_categories]
        return categories

    @staticmethod
    def obtain_price_per_unit(page: bs4.BeautifulSoup) -> Tuple[float, str]:
        fetched_unit_prices = page.find_all("span", "average-price")
        price = [process_price(unit_price.text) for unit_price in fetched_unit_prices][0]
        units = [process_unit_price(unit_price.text) for unit_price in fetched_unit_prices][0]
        return float(price), units

    @staticmethod
    def obtain_discount(page: bs4.BeautifulSoup) -> str:
        try:
            fetched_discount = page.find_all("span", "product_details_promotion_description")
            discount_percentage = [process_discount(discount.text) for discount in fetched_discount][0]
        except Exception:
            discount_percentage = None
        return discount_percentage

    def cargar_paginas_producto(self):
        """
        Carga las paginas de producto que haya en el sitemap en la
        varible 'listaPaginasProducto'
        :return:
        """

        sitemap = self.get_page(self.URLSiteMap)

        paginas_producto = sitemap.find_all("loc", string=re.compile('.+\/p\/\d+'))

        for p in paginas_producto:
            self.listaPaginasProducto.append(p.string)

    def get_info_from_url(self, url: str) -> dict:
        req = requests.get(url)
        page = BeautifulSoup(req.content, features='html.parser')
        price = self.obtain_price(page)
        product, brand = self.obtain_name(page)
        unit_price, units = self.obtain_price_per_unit(page)
        categories = self.obtain_categories(page)
        discount = self.obtain_discount(page)
        dic = {"date": str(datetime.date.today()), "product": product, "brand": brand, "price": price,
               "categories": categories, "unit_price": unit_price, "units": units, "discount": discount}
        return dic

    def save_record(self, record: dict, filename: str):
        with open(os.path.join(self.data_path, 'tmp', hashlib.md5(filename.encode()).hexdigest() + '.json'), 'w+',
                  encoding='utf-8') as f:
            json.dump(record, f, ensure_ascii=False)

    def parse_results(self):
        out = []
        logging.info("Crawling finished. Processing tmp data.")
        for file in glob.glob(os.path.join(self.data_path, 'tmp', '*.json')):
            with open(file, 'r+', encoding='utf-8') as f:
                record = json.loads(f.read())
                out.append(record)
        with open(os.path.join(self.data_path,
                               datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d_%H%M') + '_dia.json'),
                  'a+', encoding='utf-8') as outfile:
            json.dump(out, outfile, ensure_ascii=False)
            shutil.rmtree(os.path.join(self.data_path, 'tmp'))

    def start_scraping(self):
        results = []

        for url in self.listaPaginasProducto:
            # TODO: Manage exceptions. Errors should not affect any more field than the one that fails.
            # Poner sleep en ejecuciones reales para evitar bloqueos y saturaciones del servidor.
            # time.sleep(1)
            try:
                record = self.get_info_from_url(url)
                self.save_record(record, record["product"])
                logging.info(record)
            except Exception as e:
                logging.warning(f"{url} failed. No information retrieved.")  # , e)
                logging.info(e)
        self.parse_results()
        return results
