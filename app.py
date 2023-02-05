from flask import Flask, request

app = Flask(__name__)

def parser(request):
    chat_id = request.json['message']['chat']['id']
    text = request.json['message']['text']
    return chat_id, text

@app.route('/receive_request', methods=['POST'])
def receive_request():
    chat_id, text = parser(request)
    print(chat_id, text)
    return 'OK', 200


