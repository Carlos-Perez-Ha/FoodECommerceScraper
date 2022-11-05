import re
import datetime
import os
import json


def create_data_folder():
    today = str(datetime.date.today()).replace('-', '')
    data_path = os.path.join(os.getcwd(), 'data', today)
    os.makedirs(os.path.join(data_path, 'tmp'), exist_ok=True)
    return data_path





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

def process_discount(text):
    match = re.search('\\b\\d+\\%', text)
    return text[match.start(): match.end()].replace(",", ".")


def process_brand(text):
    text = preprocess_str(text)
    match = re.search('\\b[A-Z ]+\\b', text)
    return text[match.start(): match.end()].replace(",", ".").strip()
