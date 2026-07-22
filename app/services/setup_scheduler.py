
from app.src.dotenv_loader import check_interval_in_hours
from app.services.logger import logger
from apscheduler.schedulers.background import BackgroundScheduler
from .check_logic import check_next_appt

def setup_scheduler():
    scheduler = BackgroundScheduler()
    logger.info("Starting Scheduler...")    
    scheduler.add_job(check_next_appt, trigger="interval", hours=check_interval_in_hours)
    scheduler.start()
    