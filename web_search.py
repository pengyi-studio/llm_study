from dotenv import load_dotenv
import os
import http.client
import json
load_dotenv(override=True)

def serper_search(q="apple inc", hl="zh-cn",num = 5): # q是默认搜索关键词，hl是默认语言
    """
    使用 Serper API 进行常规搜索的函数

    参数:
        q (str): 搜索关键词，默认为 "apple inc"
        hl (str): 语言，默认为 "zh-cn"（中文）

    返回:
        dict: 搜索结果的 JSON 数据
    """
    search_results = make_request(q, hl, "/search", num)
    return process_search_results(search_results)


def make_request(q, hl, endpoint, num=5):
    """
    发送请求到 Serper API 的通用函数

    参数:
        q (str): 搜索关键词
        hl (str): 语言
        endpoint (str): API 的 endpoint

    返回:
        dict: 搜索结果的 JSON 数据
    """
    # 加载.env文件
    load_dotenv(override=True)

    api_key = os.getenv("SERPER_API_KEY")
    
    # 这种请求方法使用的是python的内置库，相对于requests库来说，更接近底层操作，但是需要手动处理较多细节
    # 所以对于日常个人开发来说，使用第三方库requests会更方便一些，但有些特定情况可能仍需要使用python的内置库，因此要注意区分而不能一概而论
    conn = http.client.HTTPSConnection("google.serper.dev") # 这些在serper官网上都有，不用担心是抄袭，代码没有专利，可以随便抄
    payload = json.dumps({
        "q": q,
        "hl": hl,
        "num": num
    })
    headers = {
        'X-API-KEY': "f6c3cbf69d262c6b313186425c6926c5b9d211d8",
        'Content-Type': 'application/json'
    }
    conn.request("POST", endpoint, payload, headers)
    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))


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
    if 'organic' in search_results:
        for result in search_results['organic']:
            message = {
                "title": result['title'],
                "url": result['link'],
                "content": result['snippet']
            }
            snippets.append(message)

    return snippets

if __name__=='__main__':
    # 假设 search_results 是 search 函数的返回值
    search_results = serper_search(q="中国境内哪些地方是观赏秋季红叶的著名地点？这些地方的最佳观赏期是什么时候？")
    snippets, questions = process_search_results(search_results)
    
    # 打印 search_results 以查看完整的返回值
    print("search_results:")
    print(search_results)

    # 打印 snippet 列表
    print("\nSnippets:")
    for snippet in snippets:
        print(snippet)
    
    # 打印 question 列表
    print("\nQuestions:")
    for question in questions:
        print(question)