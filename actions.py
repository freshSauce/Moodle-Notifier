import requests
from time import sleep
import os
from concurrent.futures import ThreadPoolExecutor
from models import Users
from process import Process

executor = ThreadPoolExecutor(max_workers=10)
BOT_URL = f"https://api.telegram.org/bot{os.getenv('BOT_TOKEN')}"


def send_message(chat_id, text):
    url = f"{BOT_URL}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    result = requests.post(url, json=data)
    if result.status_code != 200:
        print("Error sending message")
        print(result.json())


def start_or_help(chat_id):
    message = """¡Bienvenido a Moodle Notifier!
Este bot busca notificarte automáticamente de las tareas que tengas en Moodle.
¿Cómo empezar?
El bot te pedirá que te registres con tu usuario y contraseña de Moodle.
Por ejemplo:
/login usuario contraseña
Sencillo, ¿verdad? :)
Para ver las tareas que tienes pendientes usa /homework
Para volver a leer este menú usa /start o bien /help.
¡Buena suerte!
Creado por [freshSauce](https://t.me/freshSauce)
"""
    send_message(chat_id, message)


def start_monitor(chat_id, app):
    executor.submit(monitor, chat_id, app)


def monitor(chat_id, app):
    with app.app_context():
        while True:
            user = Process(chat_id)
            if not user.user:
                return
            result = user.get_homework()
            if "No hay tareas" in result["message"] and result["status"] == "success":
                pass
            elif (
                result["status"] == "success"
                and "No hay tareas" not in result["message"]
            ):
                send_message(
                    chat_id,
                    result["message"],
                )
            else:
                user = Process(chat_id)
                result = user.login()
                if result["status"] == "success":
                    result = user.get_homework()
                    if "No hay tareas" in result["message"]:
                        pass
                    else:
                        send_message(chat_id, result["message"])
                else:
                    send_message(chat_id, result["message"])
            sleep(600)


def reload_monitor(app):
    with app.app_context():
        _all = Users.query.all()
    for user in _all:
        start_monitor(user.telegram_id, app)
