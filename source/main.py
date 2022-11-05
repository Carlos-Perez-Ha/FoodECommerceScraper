import requests
from bs4 import BeautifulSoup
import re
import builtwith
import whois
from utils import *
import logging

logging.basicConfig(level=logging.INFO)
# filename='log.log', filemode='w',


def obtain_name(soup):
    fetched_product = soup.find_all("div", "product-name container-center")
    product_name = [preprocess_str(product.text) for product in fetched_product][0]
    brand = [process_brand(product.text) for product in fetched_product][0]
    return product_name, brand


def obtain_price(soup):
    fetched_price = soup.find_all("span", "big-price")
    price = [process_price(price.text) for price in fetched_price][0]
    return float(price)


def obtain_categories(soup):
    fetched_categories = soup.find_all("span", itemprop="name")
    categories = [preprocess_str(category.text) for category in fetched_categories]
    return categories


def obtain_price_per_unit(soup):
    fetched_unit_prices = soup.find_all("span", "average-price")
    price = [process_price(unit_price.text) for unit_price in fetched_unit_prices][0]
    units = [process_unit_price(unit_price.text) for unit_price in fetched_unit_prices][0]
    return float(price), units


def get_info_from_url(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, features='html.parser')
    price = obtain_price(soup)
    product, brand = obtain_name(soup)
    unit_price, units = obtain_price_per_unit(soup)
    categories = obtain_categories(soup)
    dic = {"product": product, "brand": brand, "price": price, "categories": categories, "unit_price": unit_price,
           "units": units}
    return dic


def dia_scraping():
    URLS = ['https://www.dia.es/compra-online/platos-preparados/pizzas-refrigeradas/p/18126',
            'https://www.dia.es/compra-online/platos-preparados/verduras/p/278605',
            'https://www.dia.es/compra-online/platos-preparados/verduras/p/280403',
            'https://www.dia.es/compra-online/frescos/carne/pollo/p/261373',
            'https://www.dia.es/compra-online/frescos/carne/pollo/p/243944',
            'https://www.dia.es/compra-online/frescos/carne/vacuno/p/162436',
            'https://www.dia.es/compra-online/frescos/carne/mixto/p/272174',
            'https://www.dia.es/compra-online/cuidado-del-hogar/cuidado-de-la-ropa/p/269882',
            'https://www.dia.es/compra-online/cuidado-del-hogar/cuidado-de-la-ropa/p/274019',
            'https://www.dia.es/compra-online/cuidado-del-hogar/lavavajillas/p/225301',
            'https://www.dia.es/compra-online/cuidado-del-hogar/lavavajillas/p/231956',
            'https://www.dia.es/compra-online/cuidado-del-hogar/papel/p/276677',
            'https://www.dia.es/compra-online/cuidado-del-hogar-de-limpieza/bano/p/217231',
            'https://www.dia.es/compra-online/cuidado-del-hogar-de-limpieza/bano/p/232866',
            'https://www.dia.es/compra-online/cuidado-del-hogar-de-limpieza/bano/p/199564'
            'https://www.dia.es/compra-online/cuidado-del-hogar/papel/p/289917']
    for url in URLS:
        # TODO: Manage exceptions. Errors should not affect any more field than the one that fails.
        try:
            logging.info(get_info_from_url(url))
        except Exception as e:
            logging.warning(f"{url} failed. No information retrieved.")  # , e)
            logging.info(e)
            pass


if __name__ == '__main__':
    # utils.parseXML("../templates/sitemap.xml")
    dia_scraping()
