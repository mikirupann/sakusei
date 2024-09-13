import requests
import json

code = "070000"
jma_url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{code}.json"
response = requests.get(jma_url)
response.raise_for_status()
jma_json = response.json()
# 日付データの取得
time = jma_json[0]["timeSeries"][0]["timeDefines"]
# 天気データの取得
jma_weather = jma_json[0]["timeSeries"][0]["areas"][0]["weathers"]
jma_weather = jma_weather.replace("　", "")
print(jma_weather)
