from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return '''<!doctype html>
    <html>
    
    '''

@app.route("/about")
def about():
    return "<h1>Hello Death!<h1>"

if __name__ == "__main__":
    app.run(debug=True)