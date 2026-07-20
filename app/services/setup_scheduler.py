
from app.services.logger import logger
from apscheduler.schedulers.background import BackgroundScheduler
from .check_logic import check_next_appt

def setup_scheduler():
    scheduler = BackgroundScheduler()
    logger.info("Starting Scheduler...")    
    scheduler.add_job(check_next_appt, trigger="interval", seconds=5)
    scheduler.start()
