from apscheduler.schedulers.blocking import BlockingScheduler


scheduler = BlockingScheduler()

def sayHello():
    print ("Teelo")

scheduler.add_job(sayHello, "interval", seconds=1)    
scheduler.start()