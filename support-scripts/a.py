import json
import csv

def json_to_csv(json_file, csv_file):
    with open(json_file, 'r', encoding="utf8") as json_file:
        data = json.load(json_file)

    with open(csv_file, 'w', newline='', encoding="utf8") as csv_file:
        csv_writer = csv.writer(csv_file)

        # Write data
        for key, value in data.items():
            csv_writer.writerow([key, value])

# Example usage
remotes = ['remote1', 'remote2', 'remote3', 'remote4']
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

for remote in remotes:
    for l in letters:
        json_to_csv('./files/'+remote+'/'+l+'.json', './files/'+remote+'/'+l+'.csv')

# json_to_csv('./files/remote3/a.json', './files/remote3/a.csv')