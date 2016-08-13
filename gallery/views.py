#coding:cp1252
import os, glob, operator
from flask import request, redirect, url_for, send_from_directory, flash, render_template
from werkzeug.utils import secure_filename
from flask import render_template
from gallery import app

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS or \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_path(filename):
    return os.path.join(os.path.dirname(__file__), app.config['UPLOAD_FOLDER'], filename)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(upload_path(filename))
            file.close()
            return redirect(url_for('gallery'))
            #return redirect(url_for('uploaded_file', filename=filename))
    return render_template('upload.html')

@app.route('/', methods=['GET', 'POST'])
@app.route('/gallery', methods=['GET'])
def gallery():
    os.chdir(os.path.dirname(__file__))
    images = {}
    for ending in ALLOWED_EXTENSIONS:
        images.update({os.path.basename(x): os.path.getmtime(x) for x in glob.glob(os.path.join(app.config['UPLOAD_FOLDER'], '*.' + ending))})
    return render_template('gallery.html',
        images_sorted=tuple(x[0] for x in sorted(images.items(), key=operator.itemgetter(1), reverse=True)),
        gallery_url='uploaded_file')

@app.route('/gallery/<filename>', methods=['GET'])
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/stats', methods=['GET'])
def stats():
    return render_template('stats.html')