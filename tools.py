
tool_1 = {
    "type":"function",
            "function":{
                "name":"serper_search",
                "description":"使用 serper_search 工具进行网络搜索，以获取最新的信息和数据。",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "q":{
                            "type":"string",
                            "description":"搜索关键词，例如 '苹果公司发布了什么最新产品？'"
                        },
                        "hl":{
                            "type":"string",
                            "description":"语言，例如 'zh-cn' 表示中文，'en-us' 表示英文。默认值为 'zh-cn'.",
                            "default":"zh-cn"
                        },
                        "num":{
                            "type":"integer",
                            "description":"返回的搜索结果数量，默认为20。",
                            "default":20
                        }
                    },
                    "required":["q"]
                }
            }
}

tool_2 = {

            "type":"function",
            "function":{
                "name":"get_weather",
                "description":"使用 get_weather 工具获取指定城市当前和未来三天的天气信息。",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "city_name":{
                            "type":"string",
                            "description":"城市名称，例如 '北京'"
                        }
                    },
                    "required":["city_name"]
                }
            }

}

tool_3 = {
    "type":"function",
            "function":{
                "name":"get_ll",
                "description":"根据旅游目的地的名称获取该地点的经纬度信息。",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "address":{
                            "type":"string",
                            "description":"结构化的地点信息，例如 '北京市朝阳区阜通东大街6号。'"
                        }
                    },
                    "required":["address"]
                }
            }
}

tool_4 = {
    
            "type":"function",
            "function":{
                "name":"get_hotel",
                "description":"根据旅游目的地（城市）的经纬度信息获取该旅游目的地的酒店信息。",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "location":{
                            "type":"string",
                            "description":"经纬度信息，格式为 '经度,纬度' 例如 '116.481488,39.990464'"
                        }
                    },
                    "required":["location"]
                }
            }
}

tools_config = [tool_1, tool_2, tool_3, tool_4]