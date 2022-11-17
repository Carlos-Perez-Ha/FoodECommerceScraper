# Scraping Dia eCommerce Site

**URL: https://www.dia.es/compra-online/**

## Robots.txt

        # For all robots
        User-agent: *
        
        # Block access to specific groups of pages
        Disallow: /compra-online/cart
        Disallow: /compra-online/checkout
        Disallow: /compra-online/my-account
        Disallow: /compra-online/*/reviewhtml/
        Disallow: /compra-online/ca/*
        Disallow: /compra-online/en/*
        Disallow: /compra-online/products/
        Disallow: /compra-online/productes/
        Disallow: /compra-online/prueba-compra-online
        
        # Allow search crawlers to discover the sitemap
        Sitemap: /compra-online/sitemap.xml
        
        
        # Block CazoodleBot as it does not present correct accept content headers
        User-agent: CazoodleBot
        Disallow: /
        
        # Block MJ12bot as it is just noise
        User-agent: MJ12bot
        Disallow: /
        
        # Block dotbot as it cannot parse base urls properly
        User-agent: dotbot/1.0
        Disallow: /
        
        # Block Gigabot
        User-agent: Gigabot
        Disallow: /

Se permite la consulta de las páginas de productos, que siguen este formato:
https://www.dia.es/compra-online/dulces-de-navidad/surtidos-navidenos/p/125266

## Sitemap y Tamaño

Sitemap: https://www.dia.es/compra-online/sitemap.xml

26880 URLs de producto.

## Tecnología

{'web-servers': ['Nginx'], 'javascript-frameworks': ['Prototype', 'React']}

Se aloja en un Nginx y usa Prototype y React (javascript dinamico)

## Propietario

Las URLs "tienda.mercadona.es" y "www.mercadona.es" devuelven nulos para whois. 
Lo sacamos de "www.mercadona.com"

```
  {
    "domain_name": "MERCADONA.COM",
    "registrar": "NOMINALIA INTERNET S.L.",
    "whois_server": "whois.nominalia.com",
    "referral_url": null,
    "updated_date": [
      "2022-04-13 10:41:32",
      "2022-04-13 00:00:00"
    ],
    "creation_date": [
      "1997-04-11 04:00:00",
      "2007-12-14 00:00:00"
    ],
    "expiration_date": [
      "2023-04-12 04:00:00",
      "2023-04-12 00:00:00"
    ],
    "name_servers": [
      "ARTEMIS.TTD.NET",
      "MINERVA.TTD.NET",
      "NS-CLOUD-A1.GOOGLEDOMAINS.COM",
      "NS-CLOUD-A2.GOOGLEDOMAINS.COM",
      "NS-CLOUD-A3.GOOGLEDOMAINS.COM",
      "NS-CLOUD-A4.GOOGLEDOMAINS.COM"
    ],
    "status": "ok https://icann.org/epp#ok",
    "emails": "abuse@nominalia.com",
    "dnssec": "unsigned",
    "name": "REDACTED FOR PRIVACY",
    "org": "Mercadona, S.A.",
    "address": "REDACTED FOR PRIVACY",
    "city": "REDACTED FOR PRIVACY",
    "state": "VALENCIA",
    "registrant_postal_code": "REDACTED FOR PRIVACY",
    "country": "ES"
  }
```