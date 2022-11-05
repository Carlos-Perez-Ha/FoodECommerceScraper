import logging
from DiaScraper import DiaScraper

logging.basicConfig(level=logging.INFO)
# filename='log.log', filemode='w',


if __name__ == '__main__':
    diaScraping = DiaScraper()
    diaScraping.cargar_paginas_producto()
    diaScraping.start_scraping()
    logging.info("Process finished.")
