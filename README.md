# FoodECommerceScraper

Repo for scraping food prices from eCommerce (Supermarket) in order to check inflation and
order uses.

## Authors:

- Oscar Promio opromio@uoc.edu
- Carlos Perez cperezha@uoc.edu

## Files

- /source : source code directory
  - main.py : executable module.
  - DiaScraper.py: Scraper code.
  - Utils.py: utilities library.
  - products_list.csv: cache file. Can be edited for debugging purposes. See "Usage" section.
- analysis.md : initial scraping analysis.
- sitemap.xml : sitemap file.
- requirements.txt : python libs.
- memoria.pdf: memoria del trabajo realizado.

## Usage

Recommended version is Python 3.8. Navigate source directory and Run:

    python -m main --reload_urls <reload>

To run start scraping. The process is divided in two steps:

1. Get a list of the products to scrape from online site and persist it on file.
2. Iterate the list and get every single product's properties and persist them on file.

``` <reload>``` parameter indicates wheter to use a previously chached products list file (```products_list.csv```)
or to scrape the products list file again from the online site. Can be ```False``` for using chached file or 
```True``` to reload the list.

## Dataset

Because of copyright issues, we connot share the final dataset. 

This is a simulated published dataset: **ZENODO** Doi URL: 


[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7334808.svg)](https://doi.org/10.5281/zenodo.7334808)
