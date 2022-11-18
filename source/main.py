import logging
import sys
from DiaScraper import DiaScraper

if __name__ == '__main__':

    if len(sys.argv) > 1 and sys.argv[1] in ['True', 'False']:
        reload = eval(sys.argv[1])
    else:
        reload = False

    diaScraping = DiaScraper()

    logging.info("Scrapping process started")
    logging.info(diaScraping.URLSite)
    logging.info(diaScraping.URLCompreOnline)
    diaScraping.start_scraping(reload)
    diaScraping.save_results()
    diaScraping.generate_dataset()
    logging.info("Process finished.")
