from apscheduler.schedulers.blocking import BlockingScheduler
import subprocess
import datetime
import pytz

# Set Indian timezone
IST = pytz.timezone('Asia/Kolkata')

scheduler = BlockingScheduler(timezone=IST)

def log(msg):
    print(f"{datetime.datetime.now(IST)} → {msg}")

def generate_tokens():
    log("Running generate_tokens...")
    subprocess.run(["python", "-m", "app.scripts.generate_tokens"])

def fetch_candle():
    log("Running fetch_candle...")
    subprocess.run(["python", "-m", "app.scripts.fetch_candle"])

def run_alerts():
    log("Starting run_alerts (WebSocket)...")
    subprocess.Popen(["python", "-m", "app.scripts.run_alerts"])
    # Popen = non-blocking → important

# Schedule Jobs
scheduler.add_job(generate_tokens, 'cron', hour=8, minute=55)
scheduler.add_job(fetch_candle, 'cron', hour=9, minute=30)
scheduler.add_job(run_alerts, 'cron', hour=9, minute=30)

log("Scheduler started...")

scheduler.start()