#----------- hava.py -----------

from flask import Flask, jsonify
import shelve
from flask_cors import CORS


app = Flask(__name__)
CORS(app)



@app.route("/data")
def get_data():
    with shelve.open("patie") as db:
        return jsonify(db.get("list", {}))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, use_reloader=False)
