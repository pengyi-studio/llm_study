# 这是我在gihub上上传的第一个文件，请多多包涵。有各种意见都可以留言，谢谢
# 这是一个简单的function calling的demo，生成回复并不稳定，但搭建的过程让我掌握了agent的基本思想，对agent有了一个初步的认识

# 需要自己创建.env文件（第一次上传没搞好）


# AI 旅行助手悠悠
本项目是一个基于 OpenAI API 和多工具集成的智能旅行助手，支持多轮对话、外部工具调用（如天气查询、酒店搜索、联网检索等），并具备深度分析与研究任务能力。核心功能由 agent.py 实现，支持自定义模型、API Key、工具配置等。

## 主要功能
- 智能对话：支持多轮问答，自动调用外部工具获取信息。
- 工具集成：集成天气查询、酒店搜索、联网检索等多种工具。
- 深度分析：可根据用户需求，主动追问并生成详细分析报告。
- 支持自定义模型和 API Key，兼容 DeepSeek API。

## 目录结构
agent_try.py         # 示例入口
agent.py             # 主体逻辑，AI助手核心
get_hotel.py         # 酒店查询工具
get_ll.py            # 联网检索工具
get_weather.py       # 天气查询工具
prompts.py           # 提示词模板
requirements.txt     # 依赖包列表
tools.py             # 工具配置
web_search.py        # 网络搜索工具
__pycache__/         # Python缓存

## 安装方法
1.克隆项目到本地
```git clone <项目地址>```
2.安装依赖
```pip install -r requirements.txt```
3.配置环境变量
查看.env文件配置api_key
