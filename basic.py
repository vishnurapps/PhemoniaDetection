from flask import Flask
from flask import request, redirect, url_for
from flask import flash
from flask_cors import CORS, cross_origin
import requests
import os
from werkzeug.utils import secure_filename
from flask import jsonify
import pydicom
from processdata import predict_disease
import json

UPLOAD_FOLDER = './uploads'
SAVED_PATH='./data'
ALLOWED_EXTENSIONS = {'dcm'}

 
app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

cors = CORS(app, resources={
    r"/*": {
       "origins": "*"
    }
})

 

@app.route('/search', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        name= request.values.get('name')
        path=SAVED_PATH+'/'+name
        if os.path.isdir(path):
            files = os.listdir(path)
            print(files)
            return jsonify(
            name="naveena",
            patientid="001",
            pathology="pathologydata",
            studydate="10-12-20",
            birthdate="30-1-90",
            age="30",
            sex="Male",
            modality="CT",
            image="C:\\Users\\V.Sreekanth Reddy\\Pictures\\Camera Roll\\clouds.jpg"
            )
        else:
            return jsonify(
            name="pandu",
            patientid="001",
            pathology="pathologydata",
            studydate="10-12-20",
            birthdate="30-1-90",
            age="30",
            sex="Male",
            modality="CT",
            image="C:\\Users\\V.Sreekanth Reddy\\Pictures\\Camera Roll\\clouds.jpg"
            )

 
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

 

@app.route('/sendimage', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return 'failed'
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return 'No file selected'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            #print(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            result = predict_disease('./uploads/'+filename)
            jsonresult = json.loads(result)
            print()
            info=pydicom.dcmread('./uploads/'+filename)
            
            patientname = ''
            if("PatientName" in info):
                pname = info.PatientName
                patientname = pname.family_name+ " " + pname.given_name
            print('Name:', patientname)
            patientid=''
            if("PatientID" in info):
                patientid=info.PatientID
            print('Id:',patientid)
            studydate=''
            if("StudyDate" in info):
                studydate=info.StudyDate
            print('study date:',studydate)
            birthdate=''
            if("PatientBirthDate" in info):
                birthdate=info.PatientBirthDate
            print('DOB:',birthdate)
            sex=''
            if("PatientSex" in info):
                sex=info.PatientSex
            print(sex)
            age=''
            if("PatientAge" in info):
                age=info.PatientAge
            print(age)
            modality=''
            if("Modality" in info):
                modality=info.Modality
            print(modality)
        finalresult={
        "patientname":patientname,
        "patientid":patientid,
        "pathology":jsonresult['data']['disease'],
        "studydate":studydate,
        "birthdate":birthdate,
        "age":age,
        "sex":sex,
        "modality":modality,
        "image":jsonresult['data']['path'],
        "statuscode":200}
        with open(f"./data/{patientname}.json", "w") as outfile:  
            json.dump(finalresult, outfile)
    return jsonify(finalresult)
@app.route('/patients', methods=['GET', 'POST'])
def patients():
    patient_names = [item.split(".")[0] for item in os.listdir("data")]
    return jsonify({"names":patient_names})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("5011"), debug = True)
