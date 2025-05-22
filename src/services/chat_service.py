import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

class ChatService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.baiyiai.online/v1/chat/completions"  # 默认使用https://api.baiyiai.online URL
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def send_message(self, message):
        try:
            payload = {
                "model": "gpt-4o-mini", #修改想用的模型名称
                "messages": [{"role": "user", "content": message}]
            }
            
            # 调试信息
            # print(f"正在发送请求到: {self.base_url}")
            # print(f"请求头: {self.headers}")
            # print(f"请求体: {payload}")
            
            response = requests.post(self.base_url, headers=self.headers, json=payload)
            
            # 调试信息
            # print(f"响应状态码: {response.status_code}")
            # print(f"响应内容: {response.text}")
            
            # 检查响应状态
            response.raise_for_status()
            
            # 检查响应内容是否为空
            if not response.text.strip():
                return "错误：服务器返回空响应"
            
            # 解析JSON响应
            response_data = response.json()
            
            if 'choices' in response_data and len(response_data['choices']) > 0:
                return response_data['choices'][0]['message']['content']
            else:
                return "错误：无法获取有效的响应内容"
                
        except requests.exceptions.RequestException as e:
            return f"网络请求错误: {str(e)}"
        except json.JSONDecodeError as e:
            return f"JSON解析错误: {str(e)}"
        except Exception as e:
            return f"发生未知错误: {str(e)}"

    def get_response(self, user_message):
        return self.send_message(user_message)