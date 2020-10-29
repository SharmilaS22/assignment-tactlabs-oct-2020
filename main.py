from fastapi import FastAPI
from models import Student, db
from bson import ObjectId

import json
import csv

app = FastAPI()


#convert csv to json
csvfilePath = 'sample.csv'
# jsonfilePath= 'output.json'

# data = {}

# with open(csvfilePath) as csvf:
#     csvReader = csv.DictReader(csvf)
#     for rows in csvReader:
#         id = rows['id']
#         data[id] = rows

# res_ids = []
# for doc in data.values():
#     print(doc)
#     student = {
#         "_id": ObjectId(),
#         "student_id": doc['id'],
#         "name": doc['name'],
#         "department": doc['department']
#     }
#     res = db.students.insert_one(student)
#     res_ids.append(res.inserted_id)

# with open(jsonfilePath, 'w') as jsonf:
#     jsonf.write(json.dumps(data, indent=4))

# json_data = json.dumps(data) 
# print(json_data)

#json file created


@app.get("/")
def read_root():
    return {'message': 'hello world'}

@app.post('/add-students')
async def add_students():
    return {'msg': "post route"}


# curl -X POST http://localhost:8000/add-students -H 'Content-Type: text/csv' -d @sample.csv

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
    setattr(stud, 'id', ObjectId())
    ret = db.students.insert_one(stud.dict(by_alias='True'))
    stud.id = ret.inserted_id
    return {
        'student': stud
    }
