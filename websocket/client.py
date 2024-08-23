import asyncio
import websockets

async def send_message():
    async with websockets.connect('ws://localhost:8765') as websocket:
        while True:
            message = input("Enter message to send (type 'exit' to quit): ")
            if message.lower() == 'exit':
                break
            await websocket.send(message)  # 发送消息到服务器
            response = await websocket.recv()  # 接收服务器回复
            print(f"Received from server: {response}")

# 运行客户端
asyncio.run(send_message())
