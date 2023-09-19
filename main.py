from fastapi import FastAPI, Depends, websockets
from app.register.register_db import register_db
from app.register.register_exception import register_exception
from app.register.register_router import register_router
from base_config import Config
from app.schemas.response_schema import CommonResponse
from app.middleware.flyele_token import FlyeleToken
from app.register.register_middleware import register_middleware

app = FastAPI()


@app.websocket("/ws")
async def websocket(websocket: websockets.WebSocket):
    await websocket.accept()
    await websocket.send_json({"msg": "Hello WebSocket"})
    await websocket.close()


app.response_model_exclude_none = True
app.response_model_exclude_unset = True

register_db(app)
register_exception(app)
register_middleware(app)
register_router(app)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=Config.SERVER_PORT, reload=True)
