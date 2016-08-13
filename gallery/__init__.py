"""
The flask application package.
"""

from flask import Flask
UPLOAD_FOLDER = 'uploads'
app = Flask('gallery')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key'
import gallery.views


