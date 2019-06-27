#!/usr/bin/env python3
from flask import Flask, request, jsonify
from flask_sockets import Sockets

app = Flask(__name__)
sockets = Sockets(app)


@app.route("/ncco")
def answer_call():
    ncco = [
        {
            "action": "talk",
            "text": "Please wait while we connect you to the echo server",
        },
        {
            "action": "connect",
            "from": "NexmoTest",
            "endpoint": [
                {
                    "type": "websocket",
                    "uri": "wss://{0}/socket".format(request.host),
                    "content-type": "audio/l16;rate=16000",
                }
            ],
        },
    ]

    return jsonify(ncco)


@sockets.route("/socket", methods=["GET"])
def echo_socket(ws):
    while not ws.closed:
        message = ws.receive()
        ws.send(message)


if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    server = pywsgi.WSGIServer(("", 3000), app, handler_class=WebSocketHandler)
    server.serve_forever()
