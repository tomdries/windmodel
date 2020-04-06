from requests import get

url = 'https://www.zvnoordwijk.nl/weer/gauges.htm'
response = get(url)

winddata = response.text.partition('var winddata =')[2][11:42]
time = response.text.partition('weergave van')[2][:6]
date = response.text.partition('weergave van')[2][10:18]

print(date)
winddata = winddata.replace('"','').split(',')
max_speed = winddata[0]
avg_speed = winddata[2]
avg_heading = winddata[3]

print(time, max_speed, avg_speed, avg_heading)


# import re

# m = re.search('(?<=abc)def', respon)

# m.group(0)
# 'def'
