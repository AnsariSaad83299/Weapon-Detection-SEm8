from flask import Flask,render_template


app = Flask(__name__, template_folder='template', static_folder = 'static')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/police')
def police():
    return render_template('police.html')

@app.route('/business')
def business():
    return render_template('business.html')

if (__name__ == '__main__'):
    app.run(debug=True)