from fastapi import FastAPI
from models import Student, db

import json
import csv

app = FastAPI()

#convert csv to json
csvfilePath = 'sample.csv'
jsonfilePath= 'output.json'

data = {}

with open(csvfilePath) as csvf:
    csvReader = csv.DictReader(csvf)
    for rows in csvReader:
        id = rows['id']
        data[id] = rows

with open(jsonfilePath, 'w') as jsonf:
    jsonf.write(json.dumps(data, indent=0))
#json file created

@app.get("/")
def read_root():
    return {'message': 'hello world'}

@app.get('/students')
async def get_students():
    students_list = []
    for aStudent in db.students.find():
        students_list.append(Student(**aStudent))
    return {
        'students': students_list
    }

@app.post('/students')
async def add_student(stud: Student):
    if hasattr(stud, 'id'):
        delattr(stud, 'id')
    ret = db.students.insert_one(stud.dict(by_alais='True'))
    stud.id = ret.inserted_id
    return {
        'student': stud
    }
