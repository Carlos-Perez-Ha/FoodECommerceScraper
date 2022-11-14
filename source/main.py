import logging
from DiaScraper import DiaScraper

logging.basicConfig(level=logging.INFO)
# filename='log.log', filemode='w',


if __name__ == '__main__':
    diaScraping = DiaScraper()
    diaScraping.start_scraping(reload=False)
    diaScraping.parse_results()
    logging.info("Process finished.")
