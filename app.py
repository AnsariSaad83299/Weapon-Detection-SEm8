from flask import Flask, render_template, request, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__, template_folder='template', static_folder='static')
app.config['MONGO_URI'] = 'mongodb://localhost:27017/MajorWD'
mongo = PyMongo(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup')
def signup():
    # Fetch police addresses from the database
    police_addresses = mongo.db.police.distinct('address')
    return render_template('signup.html', police_addresses=police_addresses)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup/police', methods=['POST'])
def signup_police():
    if request.method == 'POST':
        branch_name = request.form.get('branchName')
        police_email = request.form.get('policeEmail')
        contact_number = request.form.get('contactNumber')
        address = request.form.get('address')
        username = request.form.get('policeUsername')
        password = request.form.get('policePassword')

        police_collection = mongo.db.police
        police_collection.insert_one({
            'branch_name': branch_name,
            'police_email': police_email,
            'contact_number': contact_number,
            'address': address,
            'username': username,
            'password': password
        })
        return 'Police signup successful'
    else:
        return 'Invalid request method'

@app.route('/signup/business', methods=['POST'])
def signup_business():
    if request.method == 'POST':
        business_name = request.form.get('businessName')
        business_email = request.form.get('businessEmail')
        contact_number = request.form.get('businessContactNumber')
        nearest_police_station = request.form.get('nearestPoliceStation')
        username = request.form.get('businessUsername')
        password = request.form.get('businessPassword')

        business_collection = mongo.db.business
        business_collection.insert_one({
            'business_name': business_name,
            'business_email': business_email,
            'contact_number': contact_number,
            'nearest_police_station': nearest_police_station,
            'username': username,
            'password': password
        })
        return 'Business signup successful'
    else:
        return 'Invalid request method'

if __name__ == '__main__':
    app.run(debug=True)
