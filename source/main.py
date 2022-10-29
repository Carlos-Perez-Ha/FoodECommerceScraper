import requests
from bs4 import BeautifulSoup
import re
import builtwith
import whois

URL = 'tienda.mercadona.es'


def mercadona_scraping():

    page = requests.get('http://' + URL)

    soup = BeautifulSoup(page.content, features='html.parser')

    pass


if __name__ == '__main__':

    mercadona_scraping()

    print(builtwith.builtwith('http://'+URL))

    print(whois.whois('http://www.mercadona.com'))
