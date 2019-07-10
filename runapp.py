from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_cors import CORS

#SETTING DB CONFIG
app = Flask(__name__)
CORS(app)


#get all configurations
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
#SETTING UPLOAD PATH FOR FILES
UPLOAD_FOLDER = 'C:/Users/Gawayne/eventManagementSystem/event-app/mobile-app/src/assets/Flyers'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# need to comment this line before creating db from python shell
from views import *

if __name__=='__main__':
	app.run(debug=True, host='0.0.0.0')