import requests
import json
from pprint import pprint




    prefectures = Prefecture.select()  # 全都道府県を取得
    weather_data = None
    if request.method == "POST":
        prefecture = request.form["prefecture"]
        prefecture = Prefecture.get(Prefecture.name == prefecture)
        code = prefecture.area_code

        # 気象庁APIから天気データを取得
        jma_url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{code}.json"
        response = requests.get(jma_url)
        response.raise_for_status()
        jma_json = response.json()

        # 日付データの取得
        time = jma_json[0]["timeSeries"][0]["timeDefines"]
        # 天気データの取得
        jma_weather = jma_json[0]["timeSeries"][0]["areas"][0]["weathers"]
        print(jma_weather)

        # "今日", "明日", "明後日"の対応付け
        days = ["今日", "明日", "明後日"]

        # 天気データの整形
        weather_data = []
        for i, (date, weather) in enumerate(zip(time, jma_weather)):
            formatted_date = datetime.fromisoformat(date).strftime("%m/%d")
            weather_data.append({
                "date": f"{days[i]} ({formatted_date})",
                "weather": weather
            })