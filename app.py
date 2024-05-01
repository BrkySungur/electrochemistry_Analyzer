from flask import (Flask, flash, jsonify, redirect, render_template, request,
                   session, url_for)
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/GCD')
def gcd():
    return render_template('gcd.html')



if __name__ == '__main__':
    app.run(debug=True, load_dotenv=True)
