from fastapi import FastAPI, Depends
from app.register.register_db import register_db
from app.register.register_exception import register_exception
from app.register.register_router import register_router
from base_config import Config
from app.schemas.response_schema import CommonResponse
from app.middleware.flyele_token import FlyeleToken

app = FastAPI()

app.response_model_exclude_none = True
app.response_model_exclude_unset = True

register_db(app)
register_exception(app)
register_router(app)


# @app.get("/hello/{name}", response_model=CommonResponse)
# async def say_hello(name: str):
#     return {"code": 0, "message": "1", "data": {}, "error_msg": 1}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=Config.SERVER_PORT, reload=True)
