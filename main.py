from flask import Flask, render_template, redirect, request, session

app = Flask(__name__)   

@app.route("/")                   
def home():
	return "yo"

if __name__ == "__main__":        
    app.run()