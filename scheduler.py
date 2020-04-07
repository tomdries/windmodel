import schedule
import time
from windscraper import *
get_zvn_measurement()
schedule.every(10).minutes.do(get_zvn_measurement)
schedule.every(1).hour.do(get_katwijk_measurements)

while True:
    schedule.run_pending()
    time.sleep(1)