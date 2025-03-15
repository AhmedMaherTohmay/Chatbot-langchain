import os
import logging
from flask import Flask, request, jsonify, render_template
from flask_restful import Api
from flask_cors import CORS
from chat import llm_response
import json

# Create a folder for log files if it doesn't exist
log_folder = "logs"
os.makedirs(log_folder, exist_ok=True)  # Ensures the folder exists

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(log_folder, "app.log")),  # Save logs in the "logs" folder
        logging.StreamHandler()  # Print logs to the console
    ]
)

app = Flask(__name__)
CORS(app)
# creating an API object
api = Api(app)

@app.route('/')
def index_get():
    logging.info("Accessed the home page")
    return render_template('base.html')

@app.route("/predict", methods=["POST"])
def predict():
    try:
        msg = request.json
        logging.info(f"Received request data: {msg}")
        
        msg = json.dumps(msg)
        query = llm_response(msg)
        query = {"answer": query}
        
        logging.info(f"Generated response: {query}")
        return jsonify(query)
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return jsonify({"error": "An error occurred"}), 500

if __name__ == '__main__':
    logging.info("Starting the Flask application")
    app.run(debug=True)
