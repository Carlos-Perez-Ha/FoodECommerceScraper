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
    mercadona_scraping()

    print(builtwith.builtwith('http://'+URL))

    print(whois.whois('http://www.mercadona.com'))
