from openai import OpenAI
import os
import web_search, get_weather, get_ll, get_hotel
import json
from tools import tools_config



def create_function_response_messages(messages, response):
    # 先追加需要调用外部工具的模型响应，然后调用外部工具，再追加外部工具的响应（若同时调用多个外部函数则依次追加）
    # 也就是说追加了有两轮追加消息的操作，即返回的message是包含了两次追加消息的结果
    # 函数的基本逻辑是：处理完一个response蕴含的所有信息并追加到messages
    """
    调用外部工具，并更新消息列表
    :param messages: 原始消息列表
    :param response: 模型某次包含外部工具调用请求的响应结果
    :return：messages，追加了外部工具运行结果后的消息列表
    """

    available_functions = {
        "serper_search": web_search.serper_search,
        "get_weather": get_weather.get_weather,
        "get_ll": get_ll.get_ll,
        "get_hotel": get_hotel.get_hotel,
    }
    
    # 提取function call messages
    function_call_messages = response.choices[0].message.tool_calls

    # 将function call messages追加到消息列表中
    messages.append(response.choices[0].message.model_dump())

    # 提取本次外部函数调用的每个任务请求
    for function_call_message in function_call_messages:
        
        # 提取外部函数名称
        tool_name = function_call_message.function.name
        # 提取外部函数参数
        tool_args = json.loads(function_call_message.function.arguments)       
        
        # 查找外部函数
        fuction_to_call = available_functions[tool_name]


        # 运行外部函数
        print(f"开始调用外部函数 {tool_name}，参数：{tool_args}")
        try:
            # tool_args['g'] = globals()
            # 运行外部函数
            function_response = fuction_to_call(**tool_args)
        except Exception as e:
            function_response = "函数运行报错如下:" + str(e)

        # 拼接消息队列
        # 这是这个函数里第二次追加消息
        messages.append(
            {
                "role": "tool",
                "content": json.dumps(function_response), # 将外部函数的返回值转为JSON格式字符串，所以外部函数的返回值必须是可JSON序列化的
                "tool_call_id": function_call_message.id,
            }
        )
    print("外部函数调用完成")
    #print("返回messages为：\n", messages)
    return messages     



def chat_base(messages, client, model, tools):
    """
    获得一次模型对用户的响应。若其中需要调用外部函数，
    则会反复多次调用create_function_response_messages函数获得外部函数响应。
    """
    print("开始调用模型...")
    client = client
    model = model
    
    try:
        response = client.chat.completions.create(
            model=model,  
            messages=messages,
            tools=tools,
        )
        
    except Exception as e:
        print("模型调用报错" + str(e))
        return None

    if response.choices[0].finish_reason == "tool_calls":
        i = 1
        while True:
            print(f"模型请求调用外部函数，开始第 {i} 轮调用外部函数")
            i += 1
            messages = create_function_response_messages(messages, response)
            response = client.chat.completions.create(
                model=model,  
                messages=messages,
                tools=tools,
            )
            if response.choices[0].finish_reason != "tool_calls":
                print("模型不再请求调用外部函数，准备结束对话。")
                break

    print("模型调用完成")
    return response

if __name__ == "__main__":
    
    client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")
    model = "deepseek-chat"
    tools = tools_config
    user_input = input("请输入你的旅行问题：")
    messages = [
        {"role":"system", "content":"你是一个专业的旅行规划专家，请根据用户的提问为用户规划旅行方案,并且在需要时调用外部工具获取相关信息后再给出最终回答。回答请尽可能具体，详细"},
        {"role":"user", "content": user_input}
    ]
    response = chat_base(messages, client, model, tools)
    print("模型最终回答：")
    print(response.choices[0].message.content)