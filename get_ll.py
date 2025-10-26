import requests
import json
import os
from dotenv import load_dotenv
load_dotenv(override=True)

def get_ll(address="北京"):
    # 结构化的地址信息必须要求其他function返回的地址信息足够详细，因此必须给大模型设置专门的提示词，不行的话就会返回不完整的地址，导致无法查询到经纬度
    """
    通过旅游目的地城市的名称获取该地点的经纬度信息
    args:
        address (str): 结构化的地点信息，例如 "北京市朝阳区阜通东大街6号。"
    return:
        dict: 经纬度信息的 JSON 数据
    """
    url = "https://restapi.amap.com/v3/geocode/geo?parameters"
    
    params = {
        'key': "ebd76b4057c009b6bb098f6d73e55a17",
        'address': address, # 直接使用地点名称
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
    处理 search 查询的返回值，返回一个列表snippets

    参数:
        search_results (dict): search 查询的返回值，是一个 JSON 格式的字典。

    返回:
        list: 包含经度和维度信息的snippet。
    """
    snippets = []

    # 处理 organic 搜索结果，提取 snippet
    snippets.append({"formatted_address": search_results['geocodes'][0]['formatted_address']})
    
    result = search_results['geocodes'][0]['location'].split(",", 1)
    message = {
        "longitude": result[0],
        "latitude": result[1],
    }
    snippets.append(message)

    return snippets
# 处理搜索结果，包括筛选和格式整理

if __name__ == "__main__":
    ll_info = get_ll(address="北京市朝阳区阜通东大街6号")
    print("经纬度信息:")
    print(type(ll_info))
    print(ll_info)
