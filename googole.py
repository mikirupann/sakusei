import googlemaps
from dotenv import load_dotenv
import os
from pprint import pprint 

load_dotenv()
map_api_key = os.getenv("map_API_key")

# Google Maps APIキーを設定（自分のAPIキーに置き換える）
gmaps = googlemaps.Client(key=map_api_key)

# 住所から緯度経度を取得
address = f"仙台駅"
geocode_result = gmaps.geocode(address)
pprint(geocode_result)

if geocode_result:
    location = geocode_result[0]["geometry"]["location"]
    print(location)
    lat = location["lat"]
    print(lat)
    lng = location["lng"]
    # print(f"住所: {address}")
    # print(f"緯度: {lat}, 経度: {lng}")
else:
    print("住所が見つかりませんでした。")
