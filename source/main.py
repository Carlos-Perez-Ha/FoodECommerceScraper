import logging
import argparse
from distutils.util import strtobool
from DiaScraper import DiaScraper

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--reload_urls",
                        help="True for autonomous navigation. False for specific url scrapping from products_list.csv",
                        default=True,
                        choices=["True", "False"])
    args = parser.parse_args()
    diaScraping = DiaScraper()

    logging.info("Scrapping process started")
    logging.info(diaScraping.URLSite)
    logging.info(diaScraping.URLCompreOnline)
    diaScraping.start_scraping(strtobool(args.reload_urls))
    diaScraping.generate_dataset()
    logging.info("Process finished.")
