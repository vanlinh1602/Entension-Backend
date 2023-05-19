from flask import Flask, jsonify, request
from lib.image import *
from routers.index import *
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/getImage', methods=['POST'])
def image():
    req = request.get_json()
    res = handleGetImage(data=req)
    return jsonify(res)

@app.route('/detectBubble', methods=['POST'])
def upload_image():
    req = request.get_json()
    res = handleDetectBubble(req)
    return jsonify(res)

if __name__ == '__main__':
    app.run(port=8000)