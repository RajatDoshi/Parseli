from flask import Flask, render_template, redirect, request, session

app = Flask(__name__)   

@app.route("/")                   
def home():
	return render_template('index.html')

@app.route("/upload")                   
def upload():
	return render_template('upload.html')

@app.route("/visualize")                   
def visualize():
	return render_template('visualize.html')


if __name__ == "__main__":        
    app.run()
