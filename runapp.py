from flask import Flask
from flask_sqlalchemy import SQLAlchemy 

#SETTING DB CONFIG
app = Flask(__name__)
app.config.from_pyfile('config.py')
db=SQLAlchemy(app)
#SETTING UPLOAD PATH FOR FILES
UPLOAD_FOLDER = 'C:/Users/Admin/Desktop/venv/venv/eventapp/Flyers'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from views import *


if __name__=='__main__':
	app.run(debug=True)