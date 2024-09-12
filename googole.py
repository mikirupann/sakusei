import googlemaps

# Google Maps APIキーを設定（自分のAPIキーに置き換える）
API_KEY = "AIzaSyDRbhDg494_Oe5Xlpa684GFAsHaZpl0jCo"
gmaps = googlemaps.Client(key=API_KEY)

# 住所から緯度経度を取得
address = "東京タワー, 東京, 日本"
geocode_result = gmaps.geocode(address)

if geocode_result:
    location = geocode_result[0]["geometry"]["location"]
    lat = location["lat"]
    lng = location["lng"]
    print(f"住所: {address}")
    print(f"緯度: {lat}, 経度: {lng}")
else:
    print("住所が見つかりませんでした。")
