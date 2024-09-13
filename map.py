import requests
import json
from pprint import pprint

url = "https://api.openweathermap.org/data/2.5/weather?zip={zip_place}&units=metric&appid={API_key}"
# xxxxx
url = url.format(zip_place="982-0033,JP", API_key="36b9d8939fe02ceeb259f6e9927873ec")

jsondata = requests.get(url).json()
pprint(jsondata)

print("天気：", jsondata["weather"][0]["main"])
print("天気詳細：", jsondata["weather"][0]["description"])

print("都市名：", jsondata["name"])
print("気温：", jsondata["main"]["temp"])
print("体感気温：", jsondata["main"]["feels_like"])
print("最低気温：", jsondata["main"]["temp_min"])
print("最高気温：", jsondata["main"]["temp_max"])
print("気圧：", jsondata["main"]["pressure"])
print("湿度：", jsondata["main"]["humidity"])

print("風速：", jsondata["wind"]["speed"])
print("風の方角：", jsondata["wind"]["deg"])
