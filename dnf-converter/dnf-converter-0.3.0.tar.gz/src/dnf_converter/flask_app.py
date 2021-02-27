from flask import Flask, url_for, request, render_template, redirect, make_response
from werkzeug.utils import secure_filename
import os
from pathlib import Path
from .dnf_converter import get_dnfs

if not Path(str(Path.home())+"/upload_files").exists():
    os.mkdir(str(Path.home())+"/upload_files")
upload_files = str(Path.home())+"/upload_files" #Order für die hochgeladenen Dateien

extensions = set(['txt']) #Nur txt Dateien erlauben
app = Flask(__name__)

def allowed(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions #1.check: enthält die Datei einen Punkt 2.Check ist der rechte Teil hinter dem letzten Punkt in den Extentions

def read_file(file):
    file_content = open(os.path.join(upload_files, file.filename),'r')
    return file_content.read().split('\n')


@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST":
        if 'file' not in request.files:
            logic_expression = request.form["logic_expression"]
            result = get_dnfs([logic_expression])
            return render_template('index.html', result=result)
            
        file = request.files['file']
        if allowed(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(upload_files, filename))
            file_content = read_file(file)
            result = get_dnfs(file_content)
            print(result)
            return render_template('index.html', result = result)

    else:
        return render_template('index.html', result = {})

def start_flask():
    app.run(port=1337, debug = True)
if __name__ == '__main__':
    app.run(port=1337, debug = True)
    