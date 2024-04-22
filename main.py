from flask import Flask

app = Flask(__main__)

def home():
    return "Hello! This is the main page <h1>HELLO!<h1>"

if __name__ == "__main__":
    app.run()