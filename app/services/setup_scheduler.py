
from app.services.logger import logger
from apscheduler.schedulers.background import BackgroundScheduler
from .check_logic import check_next_appt

def setup_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_next_appt, trigger="interval", hours=1)