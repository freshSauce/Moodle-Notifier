from flask import Flask, request
from actions import * 
from process import User
app = Flask(__name__)

def parser(request):
    chat_id = request.json['message']['chat']['id']
    text = request.json['message']['text']
    return chat_id, text

@app.route('/receive_request', methods=['POST'])
def receive_request():
    chat_id, text = parser(request)
    command = text.split()[0]
    if command == '/start':
        send_message(chat_id, 'Bienvenido al bot de Moodle ITSPA!')
    elif command == '/login':
        args = text.split()[1:]
        if len(args) == 2:
            user = User(chat_id, args[0], args[1])
            result = user.login()
            send_message(chat_id, result['message'])
    return 'OK', 200


