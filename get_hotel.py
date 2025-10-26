import requests
import json
import os
from dotenv import load_dotenv
load_dotenv(override=True)

def get_hotel(location="116.473168,39.993015"):
    # 结构化的地址信息必须要求其他function返回的地址信息足够详细，因此必须给大模型设置专门的提示词，不行的话就会返回不完整的地址，导致无法查询到经纬度
    """
    根据目标城市的经纬度坐标信息获取该城市中的具有特色的酒店的相关信息
    args:
        address (str): 结构化的经纬度坐标信息，例如 "116.473168,39.993015"
    return:
        dict: 酒店信息的 JSON 数据
    """
    url = "https://restapi.amap.com/v5/place/around?parameters"
    
    params = {
        'key': "ebd76b4057c009b6bb098f6d73e55a17",
        'location': location, # 直接使用地点名称
        'types':"100100",
        'radius': 20000,
        'show_fields':'business',
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

def process_search_results(search_results, hotel_num=10):
    """
    处理 search 查询的返回值，返回一个列表snippets

    参数:
        search_results (dict): search 查询的返回值，是一个 JSON 格式的字典。

    返回:
        list: 包含经度和维度信息的snippet。
    """
    snippets = []
    sum = 0

    # 处理 organic 搜索结果，提取 snippet
    for i, element in enumerate(search_results["pois"]):
        if search_results["pois"][i]["business"].get('tag') or search_results["pois"][i]["business"].get('rating') and sum < hotel_num:
            message = {
                "name": search_results["pois"][i]["name"],
                "address": search_results["pois"][i]["address"],
                "tag": search_results["pois"][i]["business"].get("tag"),
                "rating": search_results["pois"][i]["business"].get("rating"),
            }
            snippets.append(message)
            sum += 1
            continue
        else:
            continue
    return snippets


if __name__ == "__main__":
    hotel_info = get_hotel(location="116.473168,39.993015")
    print("hotel_info:")
    print(hotel_info)