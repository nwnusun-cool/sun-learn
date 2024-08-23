import asyncio
import websockets
from urllib.parse import urlencode

async def send_message_with_query_params():
    # 构造带参数的 URL
    query_params = {"param1": "value1", "param2": "value2"}
    url = f'ws://localhost:8765?{urlencode(query_params)}'

    # 连接服务器
    async with websockets.connect(url) as websocket:
        print(f"Connected to {url}")

        # 等待服务器的欢迎消息
        welcome_msg = await websocket.recv()
        print(f"Received from server: {welcome_msg}")

        # 发送其他消息给服务器
        while True:
            message = input("Enter message to send (type 'exit' to quit): ")
            if message.lower() == 'exit':
                break
            await websocket.send(message)
            response = await websocket.recv()
            print(f"Received from server: {response}")

# 运行客户端
asyncio.run(send_message_with_query_params())
