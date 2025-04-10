from flask import Flask, render_template, request, redirect, session
from grievance_classifier import classify_grievance
from pymongo import MongoClient
import pyrebase

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Firebase Config
firebase_config = {
    "apiKey": "your_api_key",
    "authDomain": "your_project_id.firebaseapp.com",
    "databaseURL": "https://your_project_id.firebaseio.com",
    "projectId": "your_project_id",
    "storageBucket": "your_project_id.appspot.com",
    "messagingSenderId": "sender_id",
    "appId": "app_id"
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

# MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['grievances']
grievance_collection = db['entries']

@app.route('/')
def home():
    if 'user' in session:
        return redirect('/dashboard')
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    try:
        user = auth.sign_in_with_email_and_password(
            request.form['email'], request.form['password']
        )
        session['user'] = user['email']
        return redirect('/dashboard')
    except:
        return "Login failed. Try again."

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')
    grievances = grievance_collection.find()
    return render_template('dashboard.html', grievances=grievances)

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        grievance_text = request.form['grievance']
        category = classify_grievance(grievance_text)
        grievance_collection.insert_one({
            'user': session.get('user', 'Anonymous'),
            'text': grievance_text,
            'category': category
        })
        return redirect('/dashboard')
    return render_template('submit.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
