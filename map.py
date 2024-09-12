import requests
from datetime import datetime

# 気象庁データの取得
area = "040000"  # 宮城県のエリアコード
jma_url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{area}.json"


# 気象庁データの取得
response = requests.get(jma_url)
response.raise_for_status()
jma_json = response.json()


# 日付データの取得
time = jma_json[0]["timeSeries"][0]["timeDefines"]
# 天気データの取得
jma_weather = jma_json[0]["timeSeries"][0]["areas"][0]["weathers"]

# "今日", "明日", "明後日"の対応付け
days = ["今日", "明日", "明後日"]

for i, (date, weather) in enumerate(zip(time, jma_weather)):
    # 日付を月と日のみのフォーマットで表示
    formatted_date = datetime.fromisoformat(date).strftime("%m月%d日")
    tenki = f"{days[i]} ({formatted_date}): {weather}"
    print(f"{days[i]} ({formatted_date}): {weather}")
