from fastapi import FastAPI, File, UploadFile
from models import Student, db
from bson import ObjectId

import json
import csv, re

app = FastAPI()

@app.get("/")
def read_root():
    return {'message': 'hello world'}

# @app.post('/add-students')
# async def add_students(file: bytes = File(...)):    
#     return {'file_size': len(file)}

# assignment route
@app.post('/upload-students')
async def upload_students_csv(file: UploadFile = File(...)):
    # read content from file
    content = await file.read()
    # split into lines
    content_lines = content.decode('utf-8').splitlines()
    print(content_lines)
    # write to a csv file
    with open('new.csv', 'w', newline="") as csvf:
        csvwriter = csv.writer(csvf, delimiter='\t')
        for line in content_lines:
            csvwriter.writerow(re.split('\s+',line))
    # read csv file and insert into mongodb
    data = {}
    csvfilePath = 'new.csv'
    with open(csvfilePath) as csvf:
        csvReader = csv.DictReader(csvf)
        for rows in csvReader:
            id = rows['id']
            data[id] = rows
    res_ids = []
    for doc in data.values():
        print(doc)
        student = {
            "_id": ObjectId(),
            "student_id": doc['id'],
            "name": doc['name'],
            "department": doc['department']
        }
        res = db.students.insert_one(student)
        res_ids.append(res.inserted_id)
    return res_ids

# curl -X POST http://localhost:8000/add-students -H 'Content-Type: text/csv' -d @sample.csv

# curl -X POST "http://localhost:8000/add-students" -H  "accept: application/json" -H  "Content-Type: multipart/form-data" -F "file=@sample.csv"

# route to get all students
@app.get('/students')
async def get_students():
    students_list = []
    for aStudent in db.students.find():
        students_list.append(Student(**aStudent))
    return {
        'students': students_list
    }
# route to add a student
# data - json - name, department, student_id
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


#convert csv to json
# csvfilePath = 'sample.csv'
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