import logging
from DiaScraper import DiaScraper

if __name__ == '__main__':
    diaScraping = DiaScraper()
    diaScraping.start_scraping(reload=False)
    diaScraping.save_results()
    logging.info("Process finished.")
