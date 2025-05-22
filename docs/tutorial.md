# AI聊天程序使用教程

## 项目简介
这是一个基于Python开发的AI聊天程序，通过调用AI API实现智能对话功能。

## 项目结构
```
python-ai-chat/
├── src/
│   ├── main.py           # 主程序入口
│   └── services/
│       └── chat_service.py    # AI服务通信模块
└── .env                  # 环境配置文件
```

## 环境要求
- Python 3.8+
- pip包管理器

## 必需的Python包
```bash
python-dotenv
requests
```

## 安装步骤
1. 克隆或下载项目代码
2. 安装依赖包：
```bash
pip install python-dotenv requests
```
3. 在项目根目录创建`.env`文件，添加以下内容：
```
AI_API_KEY=你的API密钥
```

## 配置说明
1. **API密钥配置**
   - 在`.env`文件中设置`AI_API_KEY`
   - 密钥格式：通常为一串字符串

2. **API设置**
   - 默认使用baiyiai.online的API服务，访问 https://api.baiyiai.online 获取APIkey
   - 可在`chat_service.py`中修改base_url配置其他服务商

## 使用方法
1. 运行程序：
```bash
python src/main.py
```

2. 程序交互：
   - 输入问题并按回车发送
   - 输入"退出"结束对话

## 主要功能
- 实时AI对话
- 支持连续对话
- 错误处理和提示
- 简单的命令行界面

## 常见问题解决
1. **API密钥错误**
   - 检查.env文件是否正确配置
   - 确认API密钥格式是否正确

2. **网络连接问题**
   - 检查网络连接状态
   - 确认API服务器是否可访问

3. **响应解析错误**
   - 检查API返回格式
   - 查看详细错误信息

## 开发扩展
如果想扩展功能，可以：
1. 修改`chat_service.py`添加新的API功能
2. 在`main.py`中增加用户交互选项
3. 添加图形界面支持

## 注意事项
- 请勿泄露API密钥
- 建议定期检查API额度使用情况
- 保持网络环境稳定

## 技术支持
如遇到问题，请检查：
1. 控制台错误信息
2. API响应内容
3. 网络连接状态

## 版权说明
本项目仅供学习使用，请遵守AI服务提供商的使用条款。
