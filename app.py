from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename
import numpy as np

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOADED_FILES_DEST'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
firstTime=True
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
@app.route('/')
def home():
    return render_template('index.html')
 
@app.route('/', methods=['POST'])
def upload_image():
    global firstTime
    if 'file' not in request.files and request.form['hiddenImg']=="nothing":
        flash('No file received')
        return redirect(request.url)
    file = request.files['file']
    if file and file.filename!='' and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        print('Entering file handling routine for '+filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and analyzed')
        import graph
        graph.main('static/uploads/' + filename)
        sample=False
        return render_template('index.html', filename=filename, sample=sample)
    elif file.filename == '':
        if 'hiddenImg' in request.form and request.form['hiddenImg']!="nothing":
            sample=True
            return render_template('index.html', filename=request.form['hiddenImg'], sample=sample)
        else:
            flash('Unknown Error')
            return redirect(request.url)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)
 
@app.route('/display/<filename>')
def display_image(filename):
    print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='downloads/' + filename), code=301)

@app.route('/display2/<filename>')
def display_image2(filename): #filename="out.png"
    print('display_image2 filename: ' + filename)
    return redirect(url_for('static', filename='sample_outputs/' + filename), code=301)
 
if __name__ == "__main__":
    app.run()

#Written by Adam Rizk

