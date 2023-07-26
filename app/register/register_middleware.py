from fastapi import FastAPI

from app.middleware.whitelist_middleware import ip_whitelist_middleware


def register_middleware(app: FastAPI) -> None:
    app.add_middleware(ip_whitelist_middleware)