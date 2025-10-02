from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/logs'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Info(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    
    def __repr__(self):
        return f'<User {self.username}>'

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Basic validation
        if not username or not password:
            return "Username and password are required!", 400
        
        # Hash the password before storing
        hashed_password = generate_password_hash(password)
        
        # Check if user already exists
        existing_user = Info.query.filter_by(username=username).first()
        if existing_user:
            return "Username already exists!", 400
        
        # Create new user
        user = Info(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for('success', username=username))
    
    return render_template('index.html')

@app.route('/success')
def success():
    username = request.args.get('username', 'User')
    return render_template('success.html', username=username)

# Create tables before first request
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)