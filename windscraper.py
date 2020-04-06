from requests import get
from datetime import datetime
from time import sleep

def get_zvn_measurement():
    url = 'https://www.zvnoordwijk.nl/weer/gauges.htm'
    response = get(url)

    winddata = response.text.partition('var winddata =')[2][11:42]
    winddata = winddata.replace('"','').split(',')

    measurement_time = response.text.partition('weergave van')[2][1:6]
    measurement_date = response.text.partition('weergave van')[2][10:18]
    measurement_timestamp = measurement_time + ' ' + measurement_date
    measurement_timestamp = datetime.strptime(measurement_timestamp, '%H:%M %d-%m-%y')

    max_speed = winddata[0]
    avg_speed = winddata[2]
    avg_heading = winddata[3]

    now = datetime.now()
    scrape_time = now.strftime('%H:%M')
    scrape_date = now.strftime('%d-%m-%y')
    measurement_age = now - measurement_timestamp
    return ','.join([scrape_date, scrape_time, measurement_date, measurement_time, str(measurement_age.seconds), max_speed, avg_speed, avg_heading])
    

def append_measurement(data, measurement):
    with open(data, "a") as file_object:
        file_object.write(measurement + '\n')

while True:
    append_measurement('data.csv', get_zvn_measurement())
    sleep(60*5)
        