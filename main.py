from flask import Flask, request, jsonify
import json
from controller import BaseResponse as bs

app = Flask(__name__)

@app.route('/')
def index():
    # obj.Response(status, status description, payload)
    newMessage = bs.Response(200, 'success', ['asd', 1, 1,2,34,])
    return newMessage.GetMessage()

@app.route('/getMessage', methods=['POST'])
def message():
    content = request.get_json()
    newMessage = bs.Response(200, 'success', content)
    return newMessage.GetMessage()


if __name__ == "__main__":
    app.run(debug=True)