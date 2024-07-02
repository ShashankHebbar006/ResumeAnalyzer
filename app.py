from flask import Flask, render_template,request,redirect,url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
import logging
from EntityExtractor import EntityExtractor
import time
from models import User

# form filename import classname

# logging.basicConfig(filename="app.log",
#                     format='%(asctime)s %(message)s',
#                     filemode='w')

app = Flask(__name__)
app.secret_key = '123456'
# Configure Temporary Data Storage
app.config['UPLOAD_FOLDER'] = 'uploads'

# Configure the database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# Initialize the database
db = SQLAlchemy(app)

# Create the database tables
# @app.before_first_request
# def create_tables():
#     db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/resumeanalyzer/',methods=['GET','POST'])
def resumeAnalyzer():
    if request.method == 'POST':
        file = request.files['file']
        file_name = secure_filename(file.filename)

        # Delete all previous uploads 
        if len(os.listdir(app.config['UPLOAD_FOLDER'])) > 0:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'],os.listdir(app.config['UPLOAD_FOLDER'])[0]))

        # If no file is uploaded display "No file uploaded"
        if not(file_name):
            message = 'Error: No file uploaded'
            # args = 'Error'

        # If non-PDF file is uploaded display "Only PDF files are allowed"
        elif not(file_name.endswith('.pdf')):
            message = 'Error: Only PDF files are allowed'
            # args = 'Error'

        # If PDF file is uploaded save PDF file in "uploads"
        else:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],file_name))
            message = f"File uploaded successfully:{file_name}"
            # message = "Enter Job Description"
            # args = 'Success'

        return redirect(url_for('uploaded_file',message=message))
        
    return render_template('resumeanalyzerpage.html')

@app.route('/resumeanalyzer/<message>/')
def uploaded_file(message):
    output =' Please re-upload the file and try again'
    if 'Error' not in message:
        message = 'Success'
        ee = EntityExtractor(app.config['UPLOAD_FOLDER'])
        dict_string = ee.extract_data()

        # time.sleep(3)
        # flash("Parsing resume please wait...")
        return render_template('output.html',output=dict_string)
        # return redirect(url_for('add_resume',message=message))

    # return render_template('resumeanalyzerpage.html', message=message,output=output)
    return render_template('resumeanalyzerpage.html',message='Failed')

@app.route('/resumeanalyzer/<message>/hi/', methods=['POST'])
def add_resume(message):
    ee = EntityExtractor(app.config['UPLOAD_FOLDER'])
    dict_string = ee.extract_data()
    # return jsonify({'message': 'User added', 'username': username}), 201
    # return dict_string
    # return redirect(url_for('uploaded_file',message=message))
    return render_template('resumeanalyzerpage.html',message=message,output=dict_string)

    # render_template('resumeanalyzerpage.html', message="message",output=output)

# @app.route('/resumeanalyzer/<args>')
# def uploaded_file(args):
#     if not('.pdf' in args):
#         return render_template('resumeanalyzerpage.html', message=args)
#     return render_template('resumeanalyzerpage.html', filename=args)

if __name__ == '__main__':
    app.run(debug=True)