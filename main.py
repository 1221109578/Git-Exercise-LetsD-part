from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/admin")
def about():
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)