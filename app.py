from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

import os
import os.path
from os import path

HERE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(HERE,'filestorage.db')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ DB_PATH
db = SQLAlchemy(app)

class ItemFile(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(300))
	data = db.Column(db.LargeBinary) # blob type into sqlite

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
	print('request: {}'.format(request))
	file = request.files['inputFile']

	newFile = ItemFile(name=file.filename, data=file.read())
	db.session.add(newFile)
	db.session.commit()

	return 'Saved ' + file.filename + ' into DB!'

def init_db():
	db.create_all()

if __name__ == '__main__':
	if not path.exists(DB_PATH):
		init_db()
	app.run(debug=True)