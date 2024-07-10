from flask import *

myapp = Flask(__name__)

from data import search_data

@myapp.route("/")
def hello():
    return redirect("/search?blocks-max=150&no-teigi=on")

@myapp.route("/search")
def searchresult():
    blocks_max = request.args.get("blocks-max")
    no_clone = request.args.get("no-clone")
    no_teigi = request.args.get("no-teigi")

    result_data = search_data(blocks_max=blocks_max, no_clone=no_clone, no_teigi = no_teigi )

    return render_template("index.html", test_data = result_data, hits=len(result_data), blocks_max = blocks_max, no_clone = no_clone, no_teigi = no_teigi)

if __name__ == "__main__":
    myapp.run(debug = True)