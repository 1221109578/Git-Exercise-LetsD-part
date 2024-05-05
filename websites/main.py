from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('Home.html')


@app.route("/package")
def package():
    return render_template('package.html')

if __name__ == "__main__":
    app.run(debug=True)