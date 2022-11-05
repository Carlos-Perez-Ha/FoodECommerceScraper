import bs4
import requests
from bs4 import BeautifulSoup
import re


class DiaScraper:
    """
    Objeto para descargar información de la pagina de DIA
    """

    URLSiteMap = 'https://www.dia.es/sitemap.xml'

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

    def cargar_paginas_producto(self):
        """
        Carga las paginas de producto que haya en el sitemap en la
        varible 'listaPaginasProducto'
        :return:
        """

        sitemap = self.get_page(self.URLSiteMap)

        self.print_page(sitemap)

        paginas_producto = sitemap.find_all("loc", string=re.compile('.+\/p\/\d+'))

        for p in paginas_producto:
            self.listaPaginasProducto.append(p.string)



