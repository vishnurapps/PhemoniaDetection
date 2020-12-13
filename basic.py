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
import glob
import base64

UPLOAD_FOLDER = './uploads'
SAVED_PATH = './data'
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
        name = request.values.get('name')
        path = f"./data/{name}.json"
        if os.path.isfile(path):
            with open(path) as f:
                d = json.load(f)
                print(d)
            return jsonify(d)
        else:
            return jsonify(
                statuscode=404
            )


def get_dcm_files(base_dir):
    for entry in os.scandir(base_dir):
        if entry.is_file() and (entry.name.endswith(".dic") or entry.name.endswith("dcm") or entry.name.endswith("")):
            yield entry.path
        elif entry.is_dir():
            yield from get_dcm_files(entry.path)
        else:
            # print(f"Neither a file, nor a dir: {entry.path}")
            pass


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/poll', methods=['GET', 'POST'])
def return_latest_file():
    newest = max(glob.iglob('./data/*'), key=os.path.getctime)
    print(newest)
    with open(newest) as f:
        d = json.load(f)
        print(d)
    return jsonify(d)


@app.route('/ehl', methods=['GET', 'POST'])
def process_data():
    print("hit came to ehl endpoint")
    image_path = str(request.args.get('imageUrl'))
    print("image_path is ", image_path)
    folder_path = image_path + '/'
    print("folder_path is ", folder_path)
    uuid = image_path.split('/')[-1]
    print('The uuid is ', uuid)
    for dicom in get_dcm_files('/tmp/' + folder_path):
        dcm_full_path = dicom
    dcm_name = dcm_full_path.split('/')[-1]
    print(dcm_full_path)
    info = pydicom.dcmread(dcm_full_path)

    patientname = ''
    if("PatientName" in info):
        pname = info.PatientName
        patientname = pname.family_name + " " + pname.given_name
    print('Name:', patientname)
    patientid = ''
    if("PatientID" in info):
        patientid = info.PatientID
    print('Id:', patientid)
    studydate = ''
    if("StudyDate" in info):
        studydate = info.StudyDate
    print('study date:', studydate)
    birthdate = ''
    if("PatientBirthDate" in info):
        birthdate = info.PatientBirthDate
    print('DOB:', birthdate)
    sex = ''
    if("PatientSex" in info):
        sex = info.PatientSex
    print(sex)
    age = ''
    if("PatientAge" in info):
        age = info.PatientAge
    print(age)
    modality = ''
    if("Modality" in info):
        modality = info.Modality
    print(modality)
    finalresult = {
        "name": patientname,
        "patientid": patientid,
        "pathology": jsonresult['data']['disease'],
        "studydate": studydate,
        "birthdate": birthdate,
        "age": age,
        "sex": sex,
        "modality": modality,
        "image": jsonresult['data']['path'],
        "statuscode": 200}
    with open(f"./data/{patientname}.json", "w") as outfile:
        json.dump(finalresult, outfile)
    return jsonify(finalresult)


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
            # print(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            result = predict_disease('./uploads/'+filename)
            jsonresult = json.loads(result)
            print()
            info = pydicom.dcmread('./uploads/'+filename)

            patientname = ''
            if("PatientName" in info):
                pname = info.PatientName
                patientname = pname.family_name + " " + pname.given_name
            print('Name:', patientname)
            patientid = ''
            if("PatientID" in info):
                patientid = info.PatientID
            print('Id:', patientid)
            studydate = ''
            if("StudyDate" in info):
                studydate = info.StudyDate
            print('study date:', studydate)
            birthdate = ''
            if("PatientBirthDate" in info):
                birthdate = info.PatientBirthDate
            print('DOB:', birthdate)
            sex = ''
            if("PatientSex" in info):
                sex = info.PatientSex
            print(sex)
            age = ''
            if("PatientAge" in info):
                age = info.PatientAge
            print(age)
            modality = ''
            if("Modality" in info):
                modality = info.Modality
            print(modality)
            with open(jsonresult['data']['path'], "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
        finalresult = {
            "name": patientname,
            "patientid": patientid,
            "pathology": jsonresult['data']['disease'],
            "studydate": studydate,
            "birthdate": birthdate,
            "age": age,
            "sex": sex,
            "modality": modality,
            "image": encoded_string.decode("ascii"),
            "statuscode": 200}
        with open(f"./data/{patientname}.json", "w") as outfile:
            json.dump(finalresult, outfile)
    return jsonify(finalresult)


@app.route('/patients', methods=['GET', 'POST'])
def patients():
    patient_names = [item.split(".")[0] for item in os.listdir("data")]
    return jsonify({"names": patient_names})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("5011"), debug=True)
