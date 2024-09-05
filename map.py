import requests

# 気象庁データの取得
area = int(130000)
jma_url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{area}.json"
jma_json = requests.get(jma_url).json()


jma_date = jma_json[0]["timeSeries"][0]["timeDefines"][0]
jma_weather = jma_json[0]["timeSeries"][0]["areas"][0]["weathers"][0]
# jma_rainfall = jma_json["Feature"][0]["Property"]["WeatherList"]["Weather"][0]["Rainfall"]
# 全角スペースの削除
jma_weather = jma_weather.replace("　", "")

print(jma_date)
print(jma_weather)
# print(jma_rainfall)

