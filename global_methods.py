import yaml
from urllib.parse import quote, unquote
import json
import os
import csv
import string


def load_yaml_config(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def get_text_from_file(file_path): 
    with open(file_path, 'r') as file:
        # Read the entire content of the file
        content = file.read()

    return content


def remove_punctuation(text):
    return ''.join([char for char in text if char not in string.punctuation])
