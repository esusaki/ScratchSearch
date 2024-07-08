from flask import *

myapp = Flask(__name__)

from data import test_data

@myapp.route("/")
def hello():
    return render_template("index.html", test_data = test_data)

if __name__ == "__main__":
    myapp.run(debug = True)