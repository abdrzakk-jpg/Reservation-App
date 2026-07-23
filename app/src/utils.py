from datetime import datetime, timezone
from app.db_connector import SessionLocal

# define `now` formatted date var
now = (datetime.now(timezone.utc)).strftime("%Y-%m-%dT%H:%M:%S") 

#* define 'get_db' dependency
def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()



# sms-msg generator
def generate_sms_msg( username: str, date: datetime, msg: str = "السلام عليكم ورحمت الله، يرجي من السيد `{username}` تذكر ان يوم غدٍ بتاريخ {date} موعد الحجامة\nكن فالموعد"):
    return msg.format(username=username, date=date.strftime("%Y-%m-%d"))
