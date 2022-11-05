import bs4
import requests
from bs4 import BeautifulSoup
import re
import logging
from utils import *


class DiaScraper:
    """
    Objeto para descargar información de la pagina de DIA
    """

    URLSiteMap = 'https://www.dia.es/sitemap.xml'

    logging.basicConfig(level=logging.INFO)

    def __init__(self):

        # Lista de paginas de producto del site
        self.listaPaginasProducto = []

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
    def obtain_name(soup):
        fetched_product = soup.find_all("div", "product-name container-center")
        product_name = [preprocess_str(product.text) for product in fetched_product][0]
        brand = [process_brand(product.text) for product in fetched_product][0]
        return product_name, brand

    @staticmethod
    def obtain_price(soup):
        fetched_price = soup.find_all("span", "big-price")
        price = [process_price(price.text) for price in fetched_price][0]
        return float(price)

    @staticmethod
    def obtain_categories(soup):
        fetched_categories = soup.find_all("span", itemprop="name")
        categories = [preprocess_str(category.text) for category in fetched_categories]
        return categories

    @staticmethod
    def obtain_price_per_unit(soup):
        fetched_unit_prices = soup.find_all("span", "average-price")
        price = [process_price(unit_price.text) for unit_price in fetched_unit_prices][0]
        units = [process_unit_price(unit_price.text) for unit_price in fetched_unit_prices][0]
        return float(price), units

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

    def dia_scraping(self):

        for url in self.listaPaginasProducto:
            # TODO: Manage exceptions. Errors should not affect any more field than the one that fails.
            try:
                logging.info(self.get_info_from_url(url))
            except Exception as e:
                logging.warning(f"{url} failed. No information retrieved.")  # , e)
                logging.info(e)
                pass

    def get_info_from_url(self, url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, features='html.parser')
        price = self.obtain_price(soup)
        product, brand = self.obtain_name(soup)
        unit_price, units = self.obtain_price_per_unit(soup)
        categories = self.obtain_categories(soup)
        dic = {"product": product, "brand": brand, "price": price, "categories": categories, "unit_price": unit_price,
               "units": units}
        return dic




