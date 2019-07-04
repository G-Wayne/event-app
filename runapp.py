from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


#get all configurations
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

# need to comment this line before creating db from python shell
from views import *

if __name__=='__main__':
	app.run(debug=True, host='0.0.0.0')