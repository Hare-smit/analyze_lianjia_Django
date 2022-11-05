from concurrent.futures.thread import ThreadPoolExecutor
from funtinos .get_location import *
from funtinos.get_weather import *
# weather = get_weathers("珠海")
# print(weather.get("text"))

def main():
    li=[]
    location = "116.42840695847197, 39.9627094556211"
    with ThreadPoolExecutor(max_workers=8) as pool:
        li.append(pool.submit(surrounding, (location, "美食", "中餐")))
        li.append( pool.submit(surrounding, (location, "交通设施", "地铁站")))
        li.append(  pool.submit(surrounding, (location, "交通设施", "公交车站")))
        li.append( pool.submit(surrounding, (location, "交通设施", "充电站")))
        li.append( pool.submit(surrounding, (location, "购物", "购物中心")))
    print(li)
    l=li[0]
    print(l)
if __name__ == '__main__':
    location = ['和平里五区 - 和平里', 116.42840695847197, 39.9627094556211]

    tt=surrounding(location,"美食$交通设施","")
    print(tt)