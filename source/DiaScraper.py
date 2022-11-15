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
import sys


class DiaScraper:
    """
    Objeto para descargar información de la pagina de DIA
    """

    URLSiteMap = '/sitemap.xml'
    URLSite = 'https://www.dia.es'
    URLCompreOnline = 'https://www.dia.es/compra-online/'

    PRODUCTS_CSV_FILE = "products_list.csv"
    LOG_FILE = os.path.join('..', 'logs', 'logs.log')

    HEADERS = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/107.0.0.0 Safari/537.36 '
    }

    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s",
                        handlers=[
                            logging.FileHandler(LOG_FILE),
                            logging.StreamHandler(sys.stdout)
                        ])

    def __init__(self):

        # Lista de paginas de producto del site
        self.listaPaginasProducto = []
        self.data_path = create_data_folder()
        self.execution_datetime = datetime.datetime.now()

    def __get_xml_page(self, url: str) -> bs4.BeautifulSoup:
        """
        :param url:
        :return: Devuelve un objeto BeautifulSoup para operar con la pagina cargada
        """

        session = requests.Session()
        # Se simula navegacion humana, con retraso de 1 segundo entre llamadas
        time.sleep(1)
        page = session.get(url, headers=self.HEADERS)
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
        page = session.get(url, headers=self.HEADERS)
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
        try:
            product_name = [preprocess_str(product.text) for product in fetched_product][0]
            brand = [process_brand(product.text) for product in fetched_product][0]
        except (IndexError, AttributeError):
            logging.warning('Product name not found')
            product_name = None
            brand = None
        return product_name, brand

    @staticmethod
    def __obtain_price(page: bs4.BeautifulSoup) -> float:
        try:
            fetched_price = page.find_all("span", "big-price")
            price = float([process_price(price.text) for price in fetched_price][0])
        except (IndexError, AttributeError):
            logging.warning('Product price not found')
            price = None
        return price

    @staticmethod
    def __obtain_categories(page: bs4.BeautifulSoup) -> List[str]:
        fetched_categories = page.find_all("span", itemprop="name")
        try:
            categories = [preprocess_str(category.text) for category in fetched_categories]
        except AttributeError:
            categories = None
        return categories

    @staticmethod
    def __obtain_price_per_unit(page: bs4.BeautifulSoup) -> Tuple[float, str]:
        fetched_unit_prices = page.find_all("span", "average-price")
        try:
            price = float([process_price(unit_price.text) for unit_price in fetched_unit_prices][0])
            units = [process_unit_price(unit_price.text) for unit_price in fetched_unit_prices][0]
        except (IndexError, AttributeError):
            logging.warning('Unit price not found')
            price = None
            units = None
        return price, units

    @staticmethod
    def __obtain_discount(page: bs4.BeautifulSoup) -> str:
        try:
            fetched_discount = page.find_all("span", "product_details_promotion_description")
            discount_percentage = [process_discount(discount.text) for discount in fetched_discount][0]
        except (IndexError, AttributeError):
            discount_percentage = None
        return discount_percentage

    def __cargar_paginas_producto(self):
        """
        Carga las paginas de producto que haya en el sitemap en la
        varible 'listaPaginasProducto'
        :return:
        """

        sitemap = self.__get_xml_page(self.URLSite + self.URLSiteMap)

        paginas_producto = sitemap.find_all("loc", string=re.compile('.+/p/\d+'))

        for p in paginas_producto:
            self.listaPaginasProducto.append(p.string)

    def __cargar_paginas_producto_autonomo_con_opcion(self, reload: bool):
        """
        Carga las paginas de producto con navegacion autonomo.

        :param reload: True si geremos volver a lanzar el escaneo online.
            False si queremos cargar los productos del fichero csv cacheado (PRODUCTS_CSV_FILE))
        """

        if reload:
            self.__cargar_paginas_producto_autonomo()
        else:
            self.__read_products_from_csv()

    def __read_products_from_csv(self):
        with open(self.PRODUCTS_CSV_FILE, "r") as f:
            for url in f:
                self.listaPaginasProducto.append(url.strip())

    def __write_products_to_csv(self):
        with open(self.PRODUCTS_CSV_FILE, "w") as f:
            for url in self.listaPaginasProducto:
                f.write(url + "\n")

    def __cargar_paginas_producto_autonomo(self):
        """
        Carga la lista de productos navegando por el menú de catalogo de productos
        y por la paginación de cada categoría.
        """

        home = self.__get_html_page(self.URLCompreOnline)

        # Busco todos los tags que hacen referencia a categorías de producto
        categories_list_tags = home.find_all("a", class_="go-to-category")

        # Recorro todas las categorias de productos
        for categoria_tag in categories_list_tags:

            url_catetoria = categoria_tag["href"]

            pagina_categoria = self.__get_html_page(self.URLSite + url_catetoria)

            # self.__print_page(pagina_categoria, pagina_categoria.title.string.strip()+".html")

            # Obtengo las paginas de productos de la categoria
            pagination = self.__obtain_pagination(pagina_categoria, url_catetoria)

            # Para cada pagina de producto
            for products_page in pagination:

                pagina_categoria = self.__get_html_page(self.URLSite + products_page)

                logging.info("Escaneando pagina: " + products_page)

                # Busco todos los tags que hacen referencia a enlaces a Producto
                product_main_link_tags = pagina_categoria.find_all("a", class_="productMainLink")

                logging.info("Numero de productos: " + str(len(product_main_link_tags)))

                # Recorro todos los tags de enlace a Producto
                for producto_tag in product_main_link_tags:
                    url_producto = producto_tag["href"]

                    self.listaPaginasProducto.append(self.URLSite + url_producto)

        # Guardamos los productos en fichero para caché
        self.__write_products_to_csv()

    @staticmethod
    def __obtain_pagination(category_page: bs4.BeautifulSoup, categoria_url: str) -> List[str]:
        """
        Devuelve todas las urls de las paginas de la categoria, segun la peginación que encuentre.
        Busca la etiqueta "scan" que contiene el numero máximo de páginas y construye todas
        las URLs para llamarlas.
        :param category_page: pagina de la categoria
        :param categoria_url: url de la pagina de la categoria
        :return:
        """

        paginator_bottom = category_page.find("div", class_="paginatorBottom")

        # navegamos hasta la paginacion
        pagination_list = paginator_bottom.find("div", class_="pagination-list-and-total")

        # obtenemos el span con el texto "de X" siendo X el numero maximno de paginas, por ejemplo "de 21"
        span = str(pagination_list.span.string)

        # Sacamos el numero decimal del texto
        numb = int(re.search('\d+', span).group())

        lista_paginas = []

        # Construimos las paginas de navegacion
        for n in range(numb):

            # la primera pagina no tiene paginacion
            if n == 0:
                lista_paginas.append(categoria_url)
            else:
                url_paginacion = categoria_url + "?page=" + str(n)
                lista_paginas.append(url_paginacion)

        return lista_paginas

    def __get_info_from_url(self, url: str) -> dict:
        page = self.__get_html_page(url)
        price = self.__obtain_price(page)
        product, brand = self.__obtain_name(page)
        unit_price, units = self.__obtain_price_per_unit(page)
        categories = self.__obtain_categories(page)
        discount = self.__obtain_discount(page)
        if any([price is None, product is None, brand is None, unit_price is None, units is None]):
            logging.warning(f"{url} failed. Missing information.")
        dic = {"date": datetime.datetime.strftime(self.execution_datetime, '%Y-%m-%d'), "product": product,
               "brand": brand, "price": price,
               "categories": categories, "unit_price": unit_price, "units": units, "discount": discount}
        return dic

    def __save_record(self, record: dict, filename: str):
        with open(os.path.join(self.data_path, 'tmp', hashlib.md5(filename.encode()).hexdigest() + '.json'), 'w+',
                  encoding='utf-8') as f:
            json.dump(record, f, ensure_ascii=False)

    def parse_results(self):
        json_output = {"data": []}
        logging.info("Crawling finished. Processing tmp data.")
        for file in glob.glob(os.path.join(self.data_path, 'tmp', '*.json')):
            with open(file, 'r+', encoding='utf-8') as f:
                record = json.loads(f.read())
                json_output["data"].append(record)
        with open(os.path.join(self.data_path,
                               datetime.datetime.strftime(self.execution_datetime, '%Y%m%d_%H%M') + '_dia.json'),
                  'a+', encoding='utf-8') as outfile:
            json.dump(json_output, outfile, ensure_ascii=False)
            shutil.rmtree(os.path.join(self.data_path, 'tmp'))

    def start_scraping(self, reload: bool):
        """
        Funciona principal que realiza el proceso de scraping
        :return:
        """

        self.__cargar_paginas_producto_autonomo_con_opcion(reload)

        for product_url in self.listaPaginasProducto:
            record = self.__get_info_from_url(product_url)
            logging.info(record)
            try:
                self.__save_record(record, record["product"])
            except AttributeError:
                logging.warning(f"{product_url} failed. No information retrieved.")
        return
