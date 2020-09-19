from flask import Flask, render_template, redirect, request, session, flash
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import pyrebase

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
		f.save(secure_filename(f.filename))
		currFileName = f.filename
	except:
		return redirect("/upload")
	
	db.child("fileNameTable").set(currFileName) 
	return redirect("/visualize")


@app.route("/visualize")                   
def visualize():
	#wrote out the firebase command for you
	fileName = fileNameTableDatabase.get('/fileNameTable', None)   
	return fileName
	#return render_template("visualize.html")


if __name__ == "__main__":        
    app.run()
