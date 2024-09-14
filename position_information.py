import geocoder
import math

# IPアドレスから位置情報を取得
g = geocoder.ip("me")

# 取得した緯度・経度の情報を表示
if g.ok:
    me = [g.latlng[0], g.latlng[1]]
    print(f"緯度: {g.latlng[0]}, 経度: {g.latlng[1]}")
else:
    print("位置情報を取得できませんでした")

print(me)
pole_radius = 6356752.314245  # 極半径
equator_radius = 6378137.0  # 赤道半径
latlon_yokosukachuo = (38.2162416, 140.8264232)

lat_me = math.radians(me[0])
lon_me = math.radians(me[1])
lat_yokosukachuo = math.radians(latlon_yokosukachuo[0])
lon_yokosukachuo = math.radians(latlon_yokosukachuo[1])
print(lat_me)

lat_difference = lat_me - lat_yokosukachuo  # 緯度差
lon_difference = lon_me - lon_yokosukachuo  # 経度差
lat_average = (lat_me + lat_yokosukachuo) / 2  # 平均緯度

e2 = (math.pow(equator_radius, 2) - math.pow(pole_radius, 2)) / math.pow(equator_radius, 2)  # 第一離心率^2

w = math.sqrt(1 - e2 * math.pow(math.sin(lat_average), 2))
m = equator_radius * (1 - e2) / math.pow(w, 3)  # 子午線曲率半径
n = equator_radius / w  # 卯酉線曲半径
distance = math.sqrt(
    math.pow(m * lat_difference, 2) + math.pow(n * lon_difference * math.cos(lat_average), 2)
)  # 距離計測
print(distance / 1000)

# if __name__ == '__main__':
#     cal_distance()
