import yaml
from urllib.parse import quote, unquote
import json
import os
import csv


def load_yaml_config(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def get_text_from_file(file_path): 
    with open(file_path, 'r') as file:
        # Read the entire content of the file
        content = file.read()

    return content

def get_search_terms():
    csv_file_path = 'search_terms.csv'
    search_terms = []

    with open(csv_file_path, mode='r') as file: # open the csv file, read
        # Create a CSV reader object
        csv_reader = csv.reader(file)
        
        # Iterate over each row in the CSV file
        for row in csv_reader:
            # Append each row to the data array
            search_terms.append(row)
    return search_terms





# ====================================================================================================
# Checkpoint Functions
# ====================================================================================================
import json
import os

CHECKPOINT_FILE = 'checkpoint.json'

def save_checkpoint(search_term_index, cleaned_papers_list, concept_edges_list):
    checkpoint = {
        'search_term_index': search_term_index,
        'cleaned_papers': cleaned_papers_list,
        'concept_edges': concept_edges_list
    }
    with open(CHECKPOINT_FILE, 'w') as f:
        json.dump(checkpoint, f)

def load_checkpoint(start_term_input):
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, 'r') as f:
            checkpoint = json.load(f)
            return checkpoint['search_term_index'], checkpoint['cleaned_papers'], checkpoint['concept_edges']
    else:
        return start_term_input, [], []  # Start from the beginning if no checkpoint exists

