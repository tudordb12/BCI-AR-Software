from flask import Flask, Response
import time
import json

app = Flask(__name__)

def generate_data():
    while True:
        value=input("a")
        yield f"{json.dumps(value)}\n\n"


@app.route('/stream')
def stream():
    return Response(generate_data(), mimetype='text/event-stream')
   
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
