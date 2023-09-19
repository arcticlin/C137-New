from fastapi import FastAPI, Depends, websockets
from starlette.websockets import WebSocket, WebSocketDisconnect

from app.register.register_db import register_db
from app.register.register_exception import register_exception
from app.register.register_router import register_router
from base_config import Config
from app.schemas.response_schema import CommonResponse
from app.middleware.flyele_token import FlyeleToken
from app.register.register_middleware import register_middleware
from app.services.ws.client_store import connected_clients
app = FastAPI()


# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     while True:
#         # 接收
#         data = await websocket.receive_text()
#         # 发送
#         await websocket.send_text(f"接收到文本: {data}")

# @app.websocket("/ws/{token}")
# async def websocket_endpoint(websocket: WebSocket, token: str):
#     try:
#         # UserToken.parse_token(token)
#         await websocket.accept()
#         if websocket not in connected_clients:
#             await websocket.send_text("Welcome to websocket")
#         connected_clients.add(websocket)
#         while True:
#             data = await websocket.receive_text()
#             for client in connected_clients:
#                 await client.send_text(data)
#     except WebSocketDisconnect:
#         connected_clients.remove(websocket)
#         await websocket.close()
#     except Exception as e:
#         connected_clients.remove(websocket)
#         await websocket.close(code=1000)
#         raise e


app.response_model_exclude_none = True
app.response_model_exclude_unset = True

register_db(app)
register_exception(app)
register_middleware(app)
register_router(app)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=Config.SERVER_PORT, reload=True)
