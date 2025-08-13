# server/server.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import util

app = Flask(__name__)
CORS(app)  # allows requests from your Netlify site

# load model and columns at import so it works under gunicorn
util.load_saved_artifacts()

@app.route("/", methods=["GET"])
def health():
    return jsonify(status="ok")

@app.route("/get_location_names", methods=["GET"])
def get_location_names():
    return jsonify({"locations": util.get_location_names()})

@app.route("/predict_home_price", methods=["POST"])
def predict_home_price():
    # accept JSON or form data
    data = request.get_json(silent=True) or request.form
    # accept a few common sqft keys used in tutorials
    sqft_raw = data.get("total_sqft") or data.get("sqft") or data.get("Squareft") or data.get("area")
    if sqft_raw is None:
        return jsonify({"error": "total_sqft is required"}), 400

    try:
        total_sqft = float(sqft_raw)
        location = data["location"]
        bhk = int(data["bhk"])
        bath = int(data["bath"])
    except Exception as e:
        return jsonify({"error": f"bad input: {e}"}), 400

    est = util.get_estimated_price(location, total_sqft, bhk, bath)
    return jsonify({"estimated_price": est})
