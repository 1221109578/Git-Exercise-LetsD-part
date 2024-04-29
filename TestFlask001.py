from flask import Flask
from TestFlask002 import views

app = Flask(__name__)
app.register_blueprint(views, url_prefix='/views')

if __name__ == "__main__":
    app.run(debug=True, port=5000)