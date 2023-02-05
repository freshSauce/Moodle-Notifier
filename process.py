from bs4 import BeautifulSoup
from time import time
import requests as r
import sys
import re
from database import Database

db = Database("database.db")

class User:
    def __init__(self, telegram_id, username, password):
        self.telegrma_id = telegram_id
        self.username = username
        self.password = password
        self.login_page = "https://virtual.itspa.edu.mx/login/index.php"
        self.s = r.session()
        self.sess_key = None
    
    def login(self):
        result = self.s.get(self.login_page)
        login_key = BeautifulSoup(result.content, "lxml").find(
            "input", attrs={"name": "logintoken"}
        )["value"]
        data = {"logintoken": login_key, "username": self.username, "password": self.password}
        result = self.s.post(self.login_page, data=data)
        try:
            content = BeautifulSoup(result.content, "lxml")
            find_key = content.find(string=lambda x: "sesskey" in x) or content.find("a", href=lambda x: "sesskey" in x)
            self.sess_key = re.search(r'"sesskey":"(.+?)"', find_key).group(1) or re.search(r"sesskey=(.+?)", find_key["href"]).group(1)
            if not self.sess_key:
                raise TypeError
            db.insert(self.telegram_id, self.username, self.password)
            return {"status": "success", "message": "Sesion iniciada correctamente."}
            
            
        except TypeError:
            if "Datos erróneos" in result.text:
                return {"status": "error", "message": "Verifica tu usuario y contraseña."}

    def get_homework(self):
        now = int(time())
        data = (
            '[{"index":0,"methodname":"core_calendar_get_action_events_by_timesort","args":{"limitnum":6,"timesortfrom": '
            + str(now)
            + ', "limittononsuspendedevents":true}}]'
        )
        try:
            get_calendar = self.s.post(
                "https://virtual.itspa.edu.mx/lib/ajax/service.php",
                params={"sesskey": self.sess_key, "info": "core_calendar_get_action_events_by_timesort"},
                data=data,
            )
            homework = get_calendar.json()[0].get("data").get("events")
            if homework:
                return {"status": "success", "message": homework}
            else:
                return {"status": "success", "message": "No hay tareas pendientes."}
        except (AttributeError, IndexError):
            return {"status": "error", "message": "Sesión inválida. Iniciando sesión nuevamente."}
    
    def update_password(self, password):
        self.password = password
        db.update(self.username, self.password)
        return {"status": "success", "message": "Contraseña actualizada correctamente."}