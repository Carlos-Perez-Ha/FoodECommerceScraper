import bs4
import requests
from bs4 import BeautifulSoup
import logging
from utils import *
from typing import Tuple, List
import hashlib
import glob
import shutil
import time


class DiaScraper:
    """
    Objeto para descargar información de la pagina de DIA
    """

    __URLSiteMap = '/sitemap.xml'
    __URLSite = 'https://www.dia.es'
    __URLCompreOnline = 'https://www.dia.es/compra-online/'

    __headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/107.0.0.0 Safari/537.36 '
    }

    logging.basicConfig(level=logging.INFO)

    def __init__(self):

        # Lista de paginas de producto del site
        self.listaPaginasProducto = []
        self.data_path = create_data_folder()

    def __get_xml_page(self, url: str) -> bs4.BeautifulSoup:
        """
        :param url:
        :return: Devuelve un objeto BeautifulSoup para operar con la pagina cargada
        """

        session = requests.Session()
        # Se simula navegacion humana, con retraso de 1 segundo entre llamadas
        time.sleep(1)
        page = session.get(url, headers=self.__headers)
        soup = BeautifulSoup(page.content, features='xml')

        return soup

    def __get_html_page(self, url: str) -> bs4.BeautifulSoup:
        """
        :param url:
        :return: Devuelve un objeto BeautifulSoup para operar con la pagina cargada
        """

        session = requests.Session()
        # Se simula navegacion humana, con retraso de 1 segundo entre llamadas
        time.sleep(1)
        page = session.get(url, headers=self.__headers)
        soup = BeautifulSoup(page.content, features='html.parser')

        return soup

    @staticmethod
    def __print_page(page: bs4.BeautifulSoup, ruta: str):
        """
        imprime la pagina escrapeada en la ruta correspondiente.
        """
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(page.prettify())

    @staticmethod
    def __obtain_name(page: bs4.BeautifulSoup) -> Tuple[str, str]:
        fetched_product = page.find_all("div", "product-name container-center")
        product_name = [preprocess_str(product.text) for product in fetched_product][0]
        brand = [process_brand(product.text) for product in fetched_product][0]
        return product_name, brand

    @staticmethod
    def __obtain_price(page: bs4.BeautifulSoup) -> float:
        fetched_price = page.find_all("span", "big-price")
        price = [process_price(price.text) for price in fetched_price][0]
        return float(price)

    @staticmethod
    def __obtain_categories(page: bs4.BeautifulSoup) -> List[str]:
        fetched_categories = page.find_all("span", itemprop="name")
        categories = [preprocess_str(category.text) for category in fetched_categories]
        return categories

    @staticmethod
    def __obtain_price_per_unit(page: bs4.BeautifulSoup) -> Tuple[float, str]:
        fetched_unit_prices = page.find_all("span", "average-price")
        price = [process_price(unit_price.text) for unit_price in fetched_unit_prices][0]
        units = [process_unit_price(unit_price.text) for unit_price in fetched_unit_prices][0]
        return float(price), units

    @staticmethod
    def __obtain_discount(page: bs4.BeautifulSoup) -> str:
        try:
            fetched_discount = page.find_all("span", "product_details_promotion_description")
            discount_percentage = [process_discount(discount.text) for discount in fetched_discount][0]
        except Exception:
            discount_percentage = None
        return discount_percentage

    def __cargar_paginas_producto(self):
        """
        Carga las paginas de producto que haya en el sitemap en la
        varible 'listaPaginasProducto'
        :return:
        """

        sitemap = self.__get_xml_page(self.__URLSite+self.__URLSiteMap)

        paginas_producto = sitemap.find_all("loc", string=re.compile('.+/p/\d+'))

        for p in paginas_producto:
            self.listaPaginasProducto.append(p.string)

    def cargar_paginas_producto_autonomo(self):

        home = self.__get_html_page(self.__URLCompreOnline)

        # Busco todos los tags que hacen referencia a categorías de producto
        categories_list_tags = home.find_all("a", class_="go-to-category")

        # Recorro todas las categorias de productos
        for categoria_tag in categories_list_tags:

            url_catetoria = categoria_tag["href"]

            pagina_categoria = self.__get_html_page(self.__URLSite + url_catetoria)

            # self.__print_page(pagina_categoria, pagina_categoria.title.string.strip()+".html")

            # Obtengo las paginas de productos de la categoria
            pagination = self.__obtein_pagination_2(pagina_categoria)

            # Para cada pagina de producto
            for products_page in pagination:

                # Salto a la pagina que toque. La primera vez no salto y escaneo
                if products_page != "":
                    pagina_categoria = self.__get_html_page(self.__URLSite + products_page)

                logging.info("Escaneando pagina: " + pagina_categoria.title.string.strip())

                # Busco todos los tags que hacen referencia a enlaces a Producto
                product_main_link_tags = pagina_categoria.find_all("a", class_="productMainLink")

                logging.info("Numero de productos: " + str(len(product_main_link_tags)))

                # Recorro todos los tags de enlace a Producto
                for producto_tag in product_main_link_tags:

                    url_producto = producto_tag["href"]

                    self.listaPaginasProducto.append(self.__URLSite + url_producto)

        self.__print_page(home, "home.html")

        # self.__print_page(pagina_producto, "pagina_producto.html")

    @staticmethod
    def __obtein_pagination(category_page: bs4.BeautifulSoup) -> List[str]:

        paginator_bottom = category_page.find("div", class_="paginatorBottom")

        pagination_list = paginator_bottom.find("select", class_="pagination-list")

        options = pagination_list.find_all("option")

        urls_paginacion = []

        for option_pagina in options:

            url_paginacion = option_pagina["value"]

            urls_paginacion.append(url_paginacion)

        return urls_paginacion

    @staticmethod
    def __obtein_pagination_2(category_page: bs4.BeautifulSoup) -> List[str]:

        paginator_bottom = category_page.find("div", class_="paginatorBottom")

        pagination_list = paginator_bottom.find("div", class_="pagination-list-and-total")

        span = str(pagination_list.span.string)

        numb = re.search('\d', span)

        print(numb)

        return None


    def __get_info_from_url(self, url: str) -> dict:
        page = self.__get_html_page(url)
        price = self.__obtain_price(page)
        product, brand = self.__obtain_name(page)
        unit_price, units = self.__obtain_price_per_unit(page)
        categories = self.__obtain_categories(page)
        discount = self.__obtain_discount(page)
        dic = {"date": str(datetime.date.today()), "product": product, "brand": brand, "price": price,
               "categories": categories, "unit_price": unit_price, "units": units, "discount": discount}
        return dic

    def __save_record(self, record: dict, filename: str):
        with open(os.path.join(self.data_path, 'tmp', hashlib.md5(filename.encode()).hexdigest() + '.json'), 'w+',
                  encoding='utf-8') as f:
            json.dump(record, f, ensure_ascii=False)

    def __parse_results(self):
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
        """
        Funciona principal que realiza el proceso de scraping
        :return:
        """
        results = []

        self.__cargar_paginas_producto()

        i = 1

        for product_url in self.listaPaginasProducto:
            # TODO: Manage exceptions. Errors should not affect any more field than the one that fails.
            # Poner sleep en ejecuciones reales para evitar bloqueos y saturaciones del servidor.
            # time.sleep(1)
            try:
                record = self.__get_info_from_url(product_url)
                self.__save_record(record, record["product"])
                logging.info(record)
            except Exception as e:
                logging.warning(f"{product_url} failed. No information retrieved.")  # , e)
                logging.info(e)

            i += 1

            if i == 10 :
                break

        self.__parse_results()
        return results


if __name__=="__main__":
    diaScraper = DiaScraper()
    diaScraper.cargar_paginas_producto_autonomo()
