import requests
import json
import os
from dotenv import load_dotenv
load_dotenv(override=True)

# 这里的jupyter notebook文件好像不能访问本地的.env文件，所以直接在代码里写了

def get_weather(city_name="北京"):
    """
    通过城市名称获取实时天气信息
    args:
        city_name (str): 城市名称，例如 "北京"
    return:
        dict: 天气信息的 JSON 数据
    """
    url = "https://restapi.amap.com/v3/weather/weatherInfo"
    
    params = {
        'key': "ebd76b4057c009b6bb098f6d73e55a17",
        'city': city_name, # 直接使用城市名称
        'extensions': 'all',
        'output': 'JSON'
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if data.get('status') == '1':
            return process_search_results(data)
        else:
            print(f"请求失败: {data.get('info')}")
            return None
    except Exception as e:
        print(f"发生错误: {e}")
        return None

def process_search_results(search_results):
    """
    处理 search 查询的返回值，返回两个列表，第一个是 snippet，第二个是 question。

    参数:
        search_results (dict): search 查询的返回值，是一个 JSON 格式的字典。

    返回:
        tuple: 一个包含两个列表的元组，第一个列表是 snippet，第二个列表是 question。
    """
    snippets = []

    # 处理 organic 搜索结果，提取 snippet

    for result in search_results['forecasts'][0]['casts']:
        message = {
            "date": result['date'],
            "week": result['week'],
            "dayweather": result['dayweather'],
            "nightweather": result['nightweather'],
            "daytemp": result['daytemp'],
            "nighttemp": result['nighttemp'],
            "daypower": result['daypower'],
            "nightpower": result['nightpower'],
        }
        snippets.append(message)

    return snippets

if __name__ == "__main__":
    weather_data = get_weather("北京")
    print(type(weather_data))
    print(weather_data)
    # print(weather_data["forecasts"][0]["casts"])