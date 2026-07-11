

from app.services.logger import logger
from datetime import datetime, timezone
from app.models import Appt
from app.db_connector import SessionLocal
import requests as req


def check_next_appt(): 
    try:
        with SessionLocal() as db:
            # get closer reminde date of an appointment
            appts: Appt = db.query(Appt).filter(Appt.sent == False).order_by(Appt.reminde_date.asc())

            closer_appt = appts.first()


            # today date
            if closer_appt is None:
                logger.debug("No Closer Appointments ...")
                return 

            now = (datetime.now(timezone.utc)).strftime("%Y-%m-%dT%H:%M:%S")

            print(f"next reminding in : {closer_appt.reminde_date}")

            if now >= (closer_appt.reminde_date).strftime("%Y-%m-%dT%H:%M:%S"):

                response = send_sms(
                        closer_appt.phone_number,   
                        f"السلام عليكم ورحمت الله، يرجي من السيد {closer_appt.username} تذكر ان يوم غد بتاريخ {closer_appt.appt_at} موعد الحجامة، كن فالموعد", 
                        "192.168.100.5" #TODO: Change to Owner IP
                )                

                if response:
                    logger.success(f"Sent To: Dear [{closer_appt.username}] to [{closer_appt.phone_number}]")
                
                closer_appt.sent = True
                db.commit()

            else:
                print(f"next reminding in : {closer_appt.reminde_date}, Waiting...")

    except Exception as err:
        logger.warning(f"Error: [{err}]")
    

# send SMS with {message} to {number_phone}
def send_sms(phone, message, ip):
    gateway_url = f"http://{ip}:8080/send-sms"
    payload = {
        "phone": phone,
        "message": message
    }
    response = req.post(gateway_url, json=payload)
    return response.status_code == 200

