from flask import Flask
from flask import request, redirect, url_for
from flask import flash
from flask_cors import CORS, cross_origin
import requests
import os
from werkzeug.utils import secure_filename
from flask import jsonify
import pydicom

UPLOAD_FOLDER = './uploads'
SAVED_PATH='./data'
ALLOWED_EXTENSIONS = {'dcm'}

 
app = Flask(__name__)
cors = CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CORS_HEADERS'] = 'Content-Type'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

 

@app.route('/search', methods=['GET', 'POST'])
@cross_origin()
def login():
    if request.method == 'POST':
        name= request.values.get('name')
        path=SAVED_PATH+'/'+name
        if os.path.isdir(path):
            files = os.listdir(path)
            print(files)
            return jsonify(
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
@cross_origin()
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
            #return redirect(url_for('upload_file', filename=filename))
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
        return jsonify(
        patientid=patientid,
        pathology="pathologydata",
        studydate=studydate,
        birthdate=birthdate,
        age=age,
        sex=sex,
        modality=modality,
        image="C:\\Users\\V.Sreekanth Reddy\\Pictures\\Camera Roll\\clouds.jpg"
    )

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("5011"), debug = True)
