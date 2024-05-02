from flask import Flask, render_template, request, jsonify, url_for
import json
from flask_pymongo import PyMongo
from werkzeug.security import check_password_hash

app = Flask(__name__, template_folder='template', static_folder='static')
app.config['MONGO_URI'] = 'mongodb://localhost:27017/MajorWD'
mongo = PyMongo(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/police')
def police():
    # Fetch business details from the database
    businesses = mongo.db.business.find()
    return render_template('police.html', businesses=businesses)
    
@app.route('/business')
def business():
    return render_template('business.html')    

@app.route('/signup')
def signup():
    # Fetch police addresses from the database
    police_addresses = mongo.db.police.distinct('address')
    return render_template('signup.html', police_addresses=police_addresses)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST': 
        request_data = request.get_data()  # Get the request body as bytes
        decoded_data = request_data.decode('utf-8')  # Decode bytes to string
        json_data = json.loads(decoded_data)  # Parse JSON string to dictionary
        email = json_data.get('email')
        password = json_data.get('password')

        # Check if user exists in police collection or business collection
        user = None  # Initialize to None
        user_type= None
        # Consider combining police and business checks into a single query with search criteria
        # based on the user type from the form (if available)

       # Check if user exists in police collection
        police_user = mongo.db.police.find_one({'police_email': email, 'password': password})
        if police_user:
            return jsonify({'success': True, 'redirect_template': url_for('police')})

        # Check if user exists in business collection
        business_user = mongo.db.business.find_one({'business_email': email, 'password': password})
        if business_user:
            return jsonify({'success': True, 'redirect_template': url_for('business')})

        # If user not found in either collection or password doesn't match
        return jsonify({'success': False, 'message': 'Invalid email or password'}), 401
    else:
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

        # Check if email already exists
        if mongo.db.police.find_one({'police_email': police_email}):
            return jsonify({'error': 'Email already exists'}), 204

        nearest_police_station = request.form.get('nearestPoliceStation')  # New field added

        # Insert new police data
        police_collection = mongo.db.police
        police_collection.insert_one({
            'branch_name': branch_name,
            'police_email': police_email,
            'contact_number': contact_number,
            'address': address,
            'nearest_police_station': nearest_police_station,  # New field added
            'username': username,
            'password': password
        })
        return '', 204  # Return empty response with 204 status code for success
    else:
        return 'Invalid request method'

@app.route('/signup/business', methods=['POST'])
def signup_business():
    if request.method == 'POST':
        business_name = request.form.get('businessName')
        business_email = request.form.get('businessEmail')
        address = request.form.get('businessAddress')
        username = request.form.get('businessUsername')
        password = request.form.get('businessPassword')

        # Check if email already exists
        if mongo.db.business.find_one({'business_email': business_email}):
            return jsonify({'error': 'Email already exists'}), 204

        nearest_police_station = request.form.get('nearestPoliceStation')  # New field added

        # Insert new business data
        business_collection = mongo.db.business
        business_collection.insert_one({
            'business_name': business_name,
            'business_email': business_email,
            'address': address,
            'nearest_police_station': nearest_police_station,  # New field added
            'username': username,
            'password': password
        })
        # success - 204
        return '', 204 
    else:
        return 'Invalid request method'

if __name__ == '__main__':
    app.run(debug=True)
