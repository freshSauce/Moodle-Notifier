from bs4 import BeautifulSoup
from time import time
import requests as r
import pickle
import re
import os
from models import Users
from database import db


class Process:
    def __init__(self, telegram_id=None, username=None, password=None):
        self.user = db.session.get(Users, {"telegram_id": telegram_id})
        self.telegram_id = telegram_id
        if not self.user:
            self.username = username
            self.password = password
            self.sess_key = None
            self.s = r.session()

        else:
            self.username = self.user.username
            self.password = self.user.password
            self.sess_key = self.user.sess_key
            self.s = r.session()
            self.s.cookies.update(pickle.loads(self.user.cookies))
        self.login_page = f"https://{os.getenv('SCHOOL_DOMAIN')}/login/index.php"

    def login(self):
        self.s.cookies = r.cookies.RequestsCookieJar()
        result = self.s.get(self.login_page)
        login_key = BeautifulSoup(result.content, "lxml").find(
            "input", attrs={"name": "logintoken"}
        )["value"]
        data = {
            "logintoken": login_key,
            "username": self.username,
            "password": self.password,
        }
        result = self.s.post(self.login_page, data=data)
        try:
            content = BeautifulSoup(result.content, "lxml")
            find_key = content.find(string=lambda x: "sesskey" in x) or content.find(
                "a", href=lambda x: "sesskey" in x
            )
            self.sess_key = re.search(r'"sesskey":"(.+?)"', find_key).group(
                1
            ) or re.search(r"sesskey=(.+?)", find_key["href"]).group(1)
            if not self.sess_key:
                raise TypeError
            user = db.session.get(Users, {"telegram_id": self.telegram_id})
            if not user:
                user = Users(
                    telegram_id=self.telegram_id,
                    username=self.username,
                    password=self.password,
                    sess_key=self.sess_key,
                    cookies=pickle.dumps(self.s.cookies),
                )
                db.session.add(user)
            else:
                if user.password != self.password:
                    user.password = self.password
                user.sess_key = self.sess_key
                user.cookies = pickle.dumps(self.s.cookies)
            db.session.commit()
            return {"status": "success", "message": "Sesion iniciada correctamente."}

        except TypeError:
            if "Datos erróneos" in result.text:
                return {
                    "status": "error",
                    "message": "Verifica tu usuario y contraseña.",
                }

    def get_homework(self):
        if not self.user:
            return {"status": "error", "message": "Inicia sesión."}

        now = int(time())
        data = (
            '[{"index":0,\
            "methodname":"core_calendar_get_action_events_by_timesort",\
            "args":{"limitnum":6,"timesortfrom": '
            + str(now)
            + ', "limittononsuspendedevents":true}}]'
        )
        try:
            get_calendar = self.s.post(
                f"https://{os.getenv('SCHOOL_DOMAIN')}/lib/ajax/service.php",
                params={
                    "sesskey": self.sess_key,
                    "info": "core_calendar_get_action_events_by_timesort",
                },
                data=data,
            )
            homework = get_calendar.json()[0].get("data").get("events")
            if homework:
                return {"status": "success", "message": homework}
            else:
                return {"status": "success", "message": "No hay tareas pendientes."}
        except (IndexError, AttributeError):
            return {
                "status": "error",
                "message": "Sesión expirada. Iniciando sesión nuevamente.",
            }

    def change_password(self, new_password):
        user = db.session.get(Users, {"telegram_id": self.telegram_id})
        user.password = new_password
        db.session.commit()
        return {"status": "success", "message": "Contraseña cambiada correctamente."}
