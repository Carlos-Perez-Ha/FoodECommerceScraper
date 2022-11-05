import xml.etree.ElementTree as ET
import re


def parseXML(xmlfile):
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    pass


def preprocess_str(text):
    rm_chars = ["\r", "\n", "\t"]
    for char in rm_chars:
        text = text.replace(char, "")
    return text.replace(",", ".").strip()


def process_unit_price(text):
    match = re.search('\\€.+$', text)
    return text[match.start(): match.end()]


def process_price(text):
    match = re.search('\\d+,\\d+', text)
    return text[match.start(): match.end()].replace(",", ".")


def process_brand(text):
    text = preprocess_str(text)
    match = re.search('\\b[A-Z ]+\\b', text)
    return text[match.start(): match.end()].replace(",", ".").strip()
