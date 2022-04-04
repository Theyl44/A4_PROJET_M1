#! /usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for
from subprocess import run, PIPE
import subprocess

UPLOAD_FOLDER = 'static/music/'
ALLOWED_EXTENSIONS = {'mp3','wav'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] =  24 * 1024 * 1024
app.config['MAX_CONTENT_PATH'] = 32767              


@app.route("/", methods = ['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route("/about")
def about_page():
    return render_template("about_us.html")
    
@app.route("/readme")
def read_me():
    return render_template("read_me.html")

@app.route("/show")
def show():
    return render_template("show.html")


@app.route("/temp")
def temp():
    return render_template("temp.html")

@app.route('/audio', methods=['POST'])
def audio():
    with open('static/music/audio_from_interface.wav', 'wb') as f:
        f.write(request.data)
    proc = run(['ffprobe', '-of', 'default=noprint_wrappers=1', 'static/music/audio_from_interface.wav'], text=True, stderr=PIPE)
    return proc.stderr

@app.route('/upload' , methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        f.save("./static/music/audio_from_interface.wav")
        return redirect(url_for('index')) 

@app.route('/to_say' , methods=['GET', 'POST'])
def to_say():
    if request.method == 'POST':
        if request.form.get('to_say'):
            #on recupere ce qui a été mis dans le formulaire et on enregistre le tout dans un fichier txt
            result = request.form['to_say']
            file = open("static/to_say.txt", "w")
            file.write(result)
            file.close() 
            return redirect(url_for('index')) 

@app.route('/process' , methods=['GET', 'POST'])
def process():
    if request.method == 'POST':
        if request.form.get('process'):
            subprocess.call("./demo_cli.py", shell=True)
            return redirect(url_for('show')) 



if __name__ == "__main__":
    app.run(debug=True)
