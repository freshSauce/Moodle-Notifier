from flask import Flask, request
from actions import send_message, reload_monitor, start_monitor
from process import Process
from database import create_db
import os
from models import create_tables

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
create_db(app)
create_tables(app)
reload_monitor(app)


def parser(request):
    chat_id = request.json["message"]["chat"]["id"]
    text = request.json["message"]["text"]
    return chat_id, text


@app.route("/receive_request", methods=["POST"])
def receive_request():
    chat_id, text = parser(request)
    command = text.split()[0]
    if command == "/start":
        send_message(chat_id, "Bienvenido al bot de Moodle ITSPA!")

    elif command == "/login":
        args = text.split()[1:]
        if len(args) == 2:
            user = Process(chat_id, args[0], args[1])
            result = user.login()
            send_message(chat_id, result["message"])
            if result["status"] == "success":
                send_message(chat_id, "¡Iniciando monitoreo!")
                start_monitor(chat_id, app)

    elif command == "/tareas":
        user = Process(chat_id)
        result = user.get_homework()

        send_message(
            chat_id,
            result["message"],
        )
        if result["status"] == "error" and "Sesión expirada" in result["message"]:
            user = Process(chat_id)
            result = user.login()
            send_message(chat_id, result["message"])
            if result["status"] == "success":
                result = user.get_homework()
                send_message(chat_id, result["message"])

    elif command == "/deletedb" and chat_id == int(os.getenv("ADMIN_ID")):
        create_tables(app, drop=True)
        send_message(chat_id, "Base de datos eliminada")

    return "OK", 200
