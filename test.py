


import requests as req
from app.src.dotenv_loader import ip



def send_sms(phone, message, ip):
    gateway_url = f"http://{ip}:8080/send-sms"
    payload = {
        "phone": phone,
        "message": message
    }
    try:
        response = req.post(gateway_url, json=payload)
        return response.status_code == 200
    except Exception as _:

        return -1

phone = "066666666"
msg = "Test"
response = send_sms(phone, msg, ip)
print(response)
