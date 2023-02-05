from bs4 import BeautifulSoup
from time import time, sleep
import requests as r
import sys
import re
from database import Database

db = Database("database.db")

login_page = "https://virtual.itspa.edu.mx/login/index.php"

s = r.session()

result = s.get(login_page)

login_key = BeautifulSoup(result.content, "lxml").find(
    "input", attrs={"name": "logintoken"}
)["value"]

data = {"logintoken": login_key, "username": "21092006", "password": "Vazbelm007"}

result = s.post(login_page, data=data)

try:
    content = BeautifulSoup(result.content, "lxml")
    find_key = content.find(string=lambda x: "sesskey" in x) or content.find("a", href=lambda x: "sesskey" in x)
    sess_key = re.search(r'"sesskey":"(.+?)"', find_key).group(1) or re.search(r"sesskey=(.+?)", find_key["href"]).group(1)
    if not sess_key:
        raise TypeError
    print("Sesion iniciada correctamente.")
    db.insert("21092006", "Vazbelm007")
    
except TypeError:
    if "Datos erróneos" in result.text:
        print("Verifica tu usuario y contraseña.")
        sys.exit(1)

now = int(time())
data = (
    '[{"index":0,"methodname":"core_calendar_get_action_events_by_timesort","args":{"limitnum":6,"timesortfrom": '
    + str(now)
    + ', "limittononsuspendedevents":true}}]'
)

get_calendar = s.post(
    "https://virtual.itspa.edu.mx/lib/ajax/service.php",
    params={"sesskey": sess_key, "info": "core_calendar_get_action_events_by_timesort"},
    data=data,
)

homework = get_calendar.json()[0].get("data").get("events")

if homework:
    for event in homework:
        print(event)
else:
    print("No hay tareas pendientes.")

