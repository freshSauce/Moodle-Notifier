import requests

TOKEN = "123456789:ABCDEF1234567890ABCDEF1234567890ABC"
BOT_URL = f"https://api.telegram.org/bot{TOKEN}"

def send_message(chat_id, text):
    url = f"{BOT_URL}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    result = requests.post(url, json=data)
    if result.status_code != 200:
        print("Error sending message")