from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime, timedelta
from src.logger import scheduler_logger

import subprocess
import os

# Path to venv
VENV_PATH = os.path.join(os.path.dirname(__file__), '../venv')

# Python path within venv
# PYTHON_EXEC = os.path.join(VENV_PATH, 'python.exe')
PYTHON_EXEC = os.path.join(VENV_PATH, 'python3')

# Initialize the scheduler
scheduler = BlockingScheduler()

# Minutes to retry
minutes_retry = 5

# Time for everyday execution
hour_day = 8
# minute_day = 30

def execute_script():
    """
    Executes main.py using subprocess.
    """

    scheduler_logger.info(f"[{datetime.now()}] Executing script...")

    try: 

        script_path = os.path.join(os.path.dirname(__file__), "main.py")
        result = subprocess.run([PYTHON_EXEC, script_path], capture_output=True, text=True, check=True)
        output = result.stdout.strip()

        scheduler_logger.info(f"[{datetime.now()}] Script executed successfully.")

        if output != "[]":
            scheduler_logger.warning(f"Some job offer were unable to insert into the database:\n\t{output}.\nRetrying in {minutes_retry} minute(s)...")
            scheduler.add_job(execute_script, trigger='date', run_date=datetime.now() + timedelta(minutes=minutes_retry))

    except subprocess.CalledProcessError as e:
        scheduler_logger.warning(f"[{datetime.now()}] Error while executing main.py: {e}")
        scheduler_logger.warning(f"Retrying in {minutes_retry} minutes...")
        scheduler.add_job(execute_script, trigger='date', run_date = datetime.now() + timedelta(minutes=minutes_retry))


# Program the automation execution everyday at 08 hours
scheduler.add_job(execute_script, "cron", hour=hour_day, next_run_time=datetime.now())
# scheduler.add_job(execute_script, "interval", minutes=minute_day, next_run_time=datetime.now())

if __name__ == '__main__':
    scheduler_logger.info("Initilizing scheduler...")
    scheduler.start()