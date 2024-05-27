import csv
import json

def process_csv_to_json_array(input_file, output_file):
    data = []
    with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            data.append(row)
    
    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, indent=4)  # Use indent for pretty printing

# Specify the path to your input CSV file and the desired output JSON file
input_path = 'src/dataset/citation.csv'
output_path = 'src/dataset/undirected.json'

process_csv_to_json_array(input_path, output_path)