import os
from dotenv import load_dotenv
from services.chat_service import ChatService

load_dotenv()

def main():
    api_key = os.getenv("AI_API_KEY")
    if not api_key:
        print("错误：未找到AI_API_KEY环境变量")
        return
        
    chat_service = ChatService(api_key)

    print("欢迎使用AI聊天程序！输入'退出'以结束对话。")
    
    while True:
        user_input = input("你： ")
        if user_input.lower() == '退出':
            print("再见！")
            break
        
        response = chat_service.get_response(user_input)
        print(f"AI： {response}")

if __name__ == "__main__":
    main()