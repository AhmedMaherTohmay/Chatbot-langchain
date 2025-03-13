from flask import Flask, request, jsonify, render_template
from flask_restful import Api
import pandas as pd
from flask_cors import CORS
from chat import llm_response
import json

app = Flask(__name__)
CORS(app)
# creating an API object
api = Api(app)

@app.route('/')
def index_get():
    # Render the base HTML template when the home page is accessed
    return render_template('base.html')

@app.route("/predict",methods=["post"])
def predict():
    msg = request.json
    msg = json.dumps(msg)
    query = llm_response(msg)
    query = {"answer": query}
    print(query)
    return jsonify(query)

if __name__ == '__main__':
    app.run(debug=True)