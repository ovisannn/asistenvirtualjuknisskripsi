from flask import Flask
import json
from controller import BaseResponse as bs

app = Flask(__name__)

@app.route('/')
def index():
    newMessage = bs.Response(200, 'success', ['asd', 1, 1,2,34,])
    return newMessage.GetMessage()


if __name__ == "__main__":
    app.run(debug=True)