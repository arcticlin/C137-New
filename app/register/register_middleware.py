from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.middleware.request_middle import RequestMiddleware
from app.middleware.whitelist_middleware import ip_whitelist_middleware
from base_config import Config


def register_middleware(app: FastAPI) -> None:
    origins = [
        "http://localhost.tiangolo.com",
        "https://localhost.tiangolo.com",
        "http://localhost",
        "http://localhost:8080",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:58891",
        # "http://116.21.70.238:3000",
    ]
    # CORS
    if Config.MIDDLEWARE_CORS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    # app.add_middleware(ip_whitelist_middleware)
    if Config.MIDDLEWARE_ACCESS:
        app.add_middleware(RequestMiddleware)
