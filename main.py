import json
import base64
import os
from flask import Flask, request
from cloudevents.http import from_http

app = Flask(__name__)

@app.route('/', methods=['GET'])
def handle_hello_world():
    name = os.getenv("POD_NAME", "Python")
    return {"message": f"Hello {name}!"}, 200

@app.route('/pubsub', methods=['POST'])
def handle_pubsub_message():
    envelope = request.get_json()

    if not envelope:
        return {"error": "no pub/sub message recieved"}, 400
    
    if not isinstance(envelope, dict) or "message" not in envelope:
        return {"error": "invalid pub/sub message"}, 400

    message_data = envelope["message"]
    if isinstance(message_data, dict) and "data" in message_data:
        data = base64.b64decode(message_data["data"]).decode("utf-8").strip()
        envelope["message"]["data"] = data

    print("Recieved PubSub Message")
    print(json.dumps(envelope, indent=2))

    return "", 204

@app.route('/eventarc', methods=['POST'])
def handle_eventarc_message():
    print("Received EventArc Message")
    print(json.dumps(request.get_data(), indent=2))
    
    return "", 204

@app.route('/apigee', methods=['GET'])
def handle_apigee_request():
    print('Recieved Request from Apigee')
    return {"message": "Hello Apigee!"}, 200

@app.route('/v1/cloud-endpoints', methods=['GET'])
def handle_cev1_request():
    print('Recieved Request from Cloud Endpoints')
    return {"message": "Hello Cloud Endpoints!", "version": 1.0}, 200

@app.route('/v2/cloud-endpoints', methods=['GET'])
def handle_cev2_request():
    print('Recieved Request from Cloud Endpoints')
    return {"msg": "Hello Cloud Endpoints!", "ver": 2.0}, 200

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)












