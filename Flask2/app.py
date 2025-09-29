from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

try:
    # Use 'with open' to ensure the file is closed correctly,
    # even if an error occurs. Replace 'config.json' with your actual file name.
    with open('config.json', 'r') as c:
        params = json.load(c)["params"]
except FileNotFoundError:
    print("Error: The configuration file was not found.")
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")
local_server = True
app = Flask(__name__)
if (local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']
db = SQLAlchemy(app)

class Contacts(db.Model):
    sno= db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    msg = db.Column(db.Text(50), nullable=False)
    date = db.Column(db.String(12))





@app.route('/')
def home():
    return render_template('index.html',params=params)
@app.route('/about')
def about():
    return render_template('about.html' ,params=params)
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')      
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry =Contacts(name=name, email=email, phone=phone, msg=message, date=datetime.now())
        db.session.add(entry)
        db.session.commit()


    return render_template('contact.html' ,params=params)
@app.route('/post')
def post():
    return render_template('post.html' ,params=params)
if __name__ == '__main__':
    app.run(debug=True)