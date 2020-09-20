from speech2text import transcribe, parse, renderEntities, DISEASE_SYMPTOMS
from db.sql_queries import getReviews

from flask import Flask, render_template, redirect, request, session, flash
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import pyrebase

import os
import pandas as pd

app = Flask(__name__)   

app.secret_key = '#d\xe9X\x00\xbe~Uq\xebX\xae\x82\x1fs\t\xb4\x99\xa3\x87\xe6.\xd1_'

#Rajat config
firebaseConfig = {
  "apiKey": "AIzaSyBVFdtJnB1lwuEm9nQTuaCcTB6K1poFeLA",
  "authDomain": "hackmit-818a9.firebaseapp.com",
  "databaseURL": "https://hackmit-818a9.firebaseio.com",
  "projectId": "hackmit-818a9",
  "storageBucket": "hackmit-818a9.appspot.com",
  "messagingSenderId": "442362680118",
  "appId": "1:442362680118:web:5c913853152f4a16d3d997",
  "measurementId": "G-DZDRSBKZ5Q"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

db = firebase.database()

from firebase import firebase as fb
fileNameTableDatabase = fb.FirebaseApplication('https://hackmit-818a9.firebaseio.com/fileNameTable')

# Create user_data directory if not exists
user_data_dir = "user_data"
if not os.path.exists(user_data_dir):
	os.makedirs(user_data_dir, exist_ok=True)

# Disease data
DISEASE_INFO = {}

getDiseaseID = lambda s : s.strip().lower().replace(' ', '_')
description_df = pd.read_csv('datasets/disease_data/symptom_Description.csv')
for i, row in description_df.iterrows():
	disease_id = getDiseaseID(row['Disease'])
	description = row['Description']
	DISEASE_INFO[disease_id] = {"name" : row['Disease'], "description" : description}

precaution_df = pd.read_csv('datasets/disease_data/symptom_precaution.csv')
for i, row in precaution_df.iterrows():
	disease_id = getDiseaseID(row['Disease'])
	precautions = []
	for n in range(1, 5):
		precautions.append(row[f'Precaution_{n}'])
	DISEASE_INFO[disease_id]["precautions"] = precautions

@app.route("/")                   
def home():
	return render_template('index.html')

@app.route("/upload")                   
def upload():
	return render_template('upload.html')

@app.route("/uploader", methods=['POST'])                   
def uploader():		
	try:
		f = request.files['file']
		path = os.path.join(user_data_dir, secure_filename(f.filename))
		f.save(path)
		currFileName = path # f.filename
	except:
		return redirect("/upload")
	
	db.child("fileNameTable").set(currFileName) 
	return redirect("/visualize")


@app.route("/visualize")                   
def visualize():
	# fileName = fileNameTableDatabase.get('/fileNameTable', None)   
	# recognized_text = getTranscript(fileName)

	with open('test_data/transcription.txt', 'r') as f:
		recognized_text = f.read()
	doc = parse(recognized_text)
	annotated_transcript = renderEntities(doc)
	
	disease_info = []
	drug_names = []
	for ent in doc.ents:
		print(ent.label_, ent.ent_id_)
		if ent.label_ == "DISEASE" and ent.ent_id_ in DISEASE_INFO.keys():
			disease_info.append( DISEASE_INFO[ent.ent_id_] )
		elif ent.label_ == "DRUG":
			drug_names.append(ent.text.lower())

	print(disease_info)
	return render_template("visualize.html", 
		annotated_transcript=annotated_transcript, 
		disease_info=disease_info,
		reviews= [getReviews(drug_name=drug) for drug in drug_names])


if __name__ == "__main__":        
    app.run(debug=True)
