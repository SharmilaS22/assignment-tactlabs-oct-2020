import json
import csv

csvfilePath = 'sample.csv'
jsonfilePath= 'output.json'

data = {}

with open(csvfilePath) as csvf:
    csvReader = csv.DictReader(csvf)
    for rows in csvReader:
        id = rows['ID']
        data[id] = rows

with open(jsonfilePath, 'w') as jsonf:
    jsonf.write(json.dumps(data, indent=0))