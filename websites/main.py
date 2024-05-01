from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('Home.html')

@app.route("/login", methods = ["POST", "GET"])
def login():
    return render_template('login.html')

@app.route("/myaccount")
def user():
    return render_template('myaccount.html')

@app.route("/signup")
def signup():
    return render_template('signup.html')

if __name__ == "__main__":
    app.run(debug=True)