import os
import tkinter as tk
from tkinter import scrolledtext
import threading
from dotenv import load_dotenv
from services.chat_service import ChatService 
# 加载环境变量
load_dotenv()

class ChatApplication:
    def __init__(self, root):
        self.root = root
        root.title("AI 聊天程序")
        root.geometry("600x500") # 设置窗口大小

        # 初始化 ChatService
        api_key = os.getenv("AI_API_KEY")
        if not api_key:
            # 在GUI中显示错误
            self.show_error("错误：未找到AI_API_KEY环境变量")
            return
        self.chat_service = ChatService(api_key)

        # 创建组件
        self.create_widgets()

        # 配置文本样式 "tags"
        self.configure_tags()

    def create_widgets(self):


        # 使用更美观的字体和样式
        self.chat_display = scrolledtext.ScrolledText(self.root, state='disabled', wrap=tk.WORD, width=70, height=20, font=("Microsoft YaHei", 11), relief=tk.FLAT, padx=10, pady=10) 
        self.chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # 输入框和发送按钮的容器
        input_frame = tk.Frame(self.root)
        input_frame.pack(padx=10, pady=(0, 10), fill=tk.X)

        # 消息输入框
        self.msg_entry = tk.Entry(input_frame, width=60, font=("Arial", 10))
        self.msg_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.msg_entry.bind("<Return>", self.send_message_event) # 绑定回车键

        # 发送按钮
        self.send_button = tk.Button(input_frame, text="发送", command=self.send_message_event, font=("Arial", 10))
        self.send_button.pack(side=tk.RIGHT, padx=(5, 0))

        # 欢迎信息
        self.add_message("欢迎使用AI聊天程序！\n", "ai_welcome") # 给欢迎信息一个独立的 tag

    def configure_tags(self):
        """配置不同角色的消息样式"""
        self.chat_display.tag_configure(
            "user", 
            justify='right',  # 用户消息靠右
            background="#90EE90", # 淡绿色背景
            foreground="black",
            relief='raised',
            borderwidth=1,
            lmargin1=0, rmargin=10, lmargin2=50, # 左边缩进50，右边边距10
            spacing1=5, # 段前距
            spacing3=5  # 段后距
        )
        self.chat_display.tag_configure(
            "ai", 
            justify='left',  # AI消息靠左
            background="#F0F0F0", # 灰色背景
            foreground="black",
            relief='solid',
            borderwidth=1,
            lmargin1=10, rmargin=50, lmargin2=0, # 右边缩进50，左边边距10
            spacing1=5,
            spacing3=5
        )
        self.chat_display.tag_configure(
            "ai_welcome", # 欢迎语居中
            justify='center',
            foreground="grey",
        )
        self.chat_display.tag_configure(
            "thinking", # “思考中”的样式
            justify='left',
            foreground="grey",
            lmargin1=10,
        )

    def add_message(self, message,tag="ai"):
        """向聊天显示框添加消息"""
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, message + "\n", tag) 
        self.chat_display.config(state='disabled')
        self.chat_display.yview(tk.END)

    def send_message_event(self, event=None):
        """处理发送消息事件（按钮点击或回车）"""
        user_input = self.msg_entry.get()
        if not user_input.strip():
            return
        
        self.add_message(f"你： {user_input}", "user")
        self.msg_entry.delete(0, tk.END)

        # 禁用输入框和发送按钮，防止重复发送
        self.msg_entry.config(state='disabled')
        self.send_button.config(state='disabled')

        # 使用新的 add_message 方法，并传入 "thinking" tag
        self.add_message("AI：正在思考中...", "thinking")
        
        # 创建并启动一个新线程来获取AI响应，避免GUI冻结
        thread = threading.Thread(target=self.get_ai_response, args=(user_input,))
        thread.start()

    def get_ai_response(self, message):
        """在后台线程中调用API"""
        response = self.chat_service.get_response(message)
        
        # API调用完成后，安排在主线程中更新GUI
        # 使用 after() 可以安全地从其他线程操作Tkinter组件
        self.root.after(0, self.update_ui_with_response, response)

    def update_ui_with_response(self, response):
        """在主线程中更新UI"""
        # 删除 "正在思考中..." 这条消息
        self.chat_display.config(state='normal')
        # 获取所有文本，分割成行，移除最后一行，然后重新设置文本
        content = self.chat_display.get(1.0, tk.END)
        last_thinking_index = content.rfind("AI：正在思考中...")
        if last_thinking_index != -1:
            self.chat_display.config(state='normal')
            # 计算要删除的起始和结束位置
            start_index = f"1.0 + {last_thinking_index}c"
            end_index = f"{start_index} + 1l" # 删除整行
            self.chat_display.delete(start_index, end_index)
            self.chat_display.config(state='disabled')

        # 使用新的 add_message 方法，并传入 "ai" tag
        self.add_message(f"AI： {response}", "ai")

        # 重新启用输入和按钮
        self.msg_entry.config(state='normal')
        self.send_button.config(state='normal')

    def show_error(self, message):
        """显示错误信息并禁用输入"""
        error_label = tk.Label(self.root, text=message, fg="red", font=("Arial", 12))
        error_label.pack(pady=20)


if __name__ == "__main__":
    
    root = tk.Tk()
    app = ChatApplication(root)
    root.mainloop()