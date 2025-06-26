import os
import logging
from flask import Flask, request, render_template, Response, stream_with_context, jsonify
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
    ]
)

app = Flask(__name__)
CORS(app)
# creating an API object
api = Api(app)

# Logging middleware to log incoming requests
@app.before_request
def log_request_info():
    logging.info(f"Incoming Request: {request.method} {request.url}")
    logging.info(f"Headers: {request.headers}")
    logging.info(f"Body: {request.get_data()}")

# Logging middleware to log responses
@app.after_request
def log_response_info(response):
    logging.info(f"Outgoing Response: {response.status}")
    logging.info(f"Headers: {response.headers}")

    # Avoid logging the body for streaming responses
    if not response.is_streamed:
        logging.info(f"Body: {response.get_data()}")

    return response

@app.route('/')
def index_get():
    # Render the base HTML template when the home page is accessed
    logging.info("Rendering the base HTML template")
    return render_template('base.html')

@app.route("/chat", methods=["POST"])
def predict():
    msg = request.json
    msg = json.dumps(msg)
    logging.info(f"Received chat message: {msg}")

    # Stream the response from llm_response
    def generate():
        for chunk in llm_response(msg):
            logging.info(f"Streaming response chunk: {chunk}")
            yield f"data: {json.dumps({'response': chunk})}\n\n"  

    return Response(stream_with_context(generate()), content_type="text/event-stream")

# Error handler to log exceptions
@app.errorhandler(Exception)
def handle_exception(e):
    logging.error(f"Exception occurred: {e}", exc_info=True)
    return jsonify(error=str(e)), 500

if __name__ == '__main__':
    logging.info("Starting the Flask application")
    app.run(debug=True, host='0.0.0.0')