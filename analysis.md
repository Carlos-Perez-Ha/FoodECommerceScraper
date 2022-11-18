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

    {'cdn': ['Akamai'], 'ecommerce': ['Hybris'], 'programming-languages': ['Java']}

El site se ha construido con Hybris, una herramienta ahora de SAP para construir 
sites de ecommerce de retail. Utiliza java para la ejecución del portal.

## Propietario

Las URLs "dia.es" y "dia.es/compra-online" devuelven nulos para whois. 
Quizas se debe a que utilizan Akamai como chaché.