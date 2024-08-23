import asyncio
import websockets


# 定义处理连接的函数
async def handle_client(websocket, path):
    # 这里是处理连接的逻辑
    try:
        while True:
            message = await websocket.recv()  # 接收客户端发送的消息
            print(f"Received message from client: {message}")
            await websocket.send(f"Echoing back: {message}")  # 回复客户端
    except websockets.exceptions.ConnectionClosedError:
        print("Client connection closed unexpectedly.")


# 启动 WebSocket 服务器
async def start_server():
    server = await websockets.serve(handle_client, '0.0.0.0', 8765)
    print("WebSocket server started. Listening on ws://localhost:8765")
    await server.wait_closed()


# 运行服务器
asyncio.run(start_server())
