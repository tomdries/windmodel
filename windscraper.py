from requests import get
from datetime import datetime, timedelta
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
import numpy as np
import pandas as pd
import pytz

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

    now = datetime.now(pytz.timezone('Europe/Amsterdam')).replace(tzinfo=None)

    scrape_time = now.strftime('%H:%M')
    scrape_date = now.strftime('%d-%m-%y')
    measurement_age = now - measurement_timestamp
    measurement = ','.join([scrape_date, scrape_time, measurement_date, measurement_time, str(measurement_age.seconds), max_speed, avg_speed, avg_heading])
    with open('data_zvn.csv', "a") as file_object:
        file_object.write(measurement + '\n')

def get_katwijk_measurements():

    ## SCRAPE WINDMETING:
    url = 'https://windmeting.nl/windmeting.html'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    driver=webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(3)
    driver.get(url)
    print('waiting for windmeting...')
    sleep(10)
    wind_max = driver.execute_script('return data.windM')
    wind = driver.execute_script('return data.wind')
    direction = driver.execute_script('return data.dir')
    measurement_date = driver.execute_script('return tenSecAr[60]')
    measurement_time = driver.execute_script('return tenSecAr[61]')
    driver.close()
    ## TESTWAARDEN
    # wind = ['14.3', '14.8', '14.4', '14.9', '14.7', '14.7', '14.6', '13.9', '13.6', '13.1', '12.4', '12.1', '12.5', '12.3', '13.2', '13.5', '12.8', '12.7', '12.8', '12.8', '13', '13.2', '13.2', '13', '13.3', '12.7', '14.6', '14.7', '14.8', '14.7', '13.4', '13.8', '14', '13.5', '15', '14.8', '14.3', '15', '14.3', '14.9', '13.9', '14.3', '14.3', '13.8', '13.6', '12.4', '13.1', '13.2', '13.7', '13.7', '14.8', '13.7', '13.4', '13.4', '12.5', '12.6', '12.9', '12.7', '12.2', '13.1']
    # wind_max = ['12.8317', '12.9565', '12.4091', '12.8976', '12.1298', '12.2195', '12.3578', '11.5556', '11.5071', '11.0587', '10.8143', '10.9244', '11.2156', '11.0762', '10.9848', '11.3262', '11.1578', '10.3378', '11.1829', '10.9783', '11.4093', '11.2864', '11.3674', '11.0805', '11.5283', '11.1442', '12.0455', '12.2957', '12.3075', '12.8543', '12.3477', '12.1674', '11.4587', '12.1878', '13.2174', '12.4386', '12.6881', '13.5957', '12.3512', '12.6244', '12.5311', '12.0548', '12.2522', '11.2167', '11.62', '11.1333', '10.7244', '11.7149', '12.2571', '12.0045', '12.7109', '12.0024', '11.7848', '11.2767', '11.2636', '11.0522', '11.695', '10.9085', '10.9605', '11.1442'] 
    # direction =  ['240.622', '244.627', '243.33', '245.907', '243.404', '241.506', '243.341', '241.294', '236.018', '233.383', '234.999', '237.452', '238.281', '236.729', '236.925', '235.817', '238.085', '237.431', '235.817', '235.373', '235.913', '235.103', '235.395', '236.945', '238.704', '238.769', '234.701', '233.883', '234.818', '231.748', '']
    # measurement_date = '06/04/2020'
    # measurement_time = '16:12'

    wind = wind[1::2] # gooi de helft weg
    wind_max = wind_max[1::2] 

    measurement_timestamp = measurement_time + ' ' + measurement_date
    measurement_timestamp = datetime.strptime(measurement_timestamp, '%H:%M %d/%m/%Y')
    measurement_time_list = []

    #construct measurement timestamps
    for dt in range(-58,1,2):
        dt = timedelta(minutes=dt)
        measurement_time_list.append(measurement_timestamp + dt)
    
    direction = direction[:-1]

    # check if windmeting is online:
    now = datetime.now(pytz.timezone('Europe/Amsterdam')).replace(tzinfo=None)
    if now - measurement_timestamp < timedelta(minutes = 90):
        status = 1
    else:
        status = 0

    df = pd.DataFrame({'scrape_time': [now]*30,
                        'measurement_time': measurement_time_list,
                        'wind_speed': wind,
                        'wind_speed_max': wind_max,
                        'direction': direction,
                        'online': [status]*30
                        })
    print(now, ': succesfully appended data')

    df.to_csv('data_katwijk.csv',mode='a', header = False,  index=False)

        