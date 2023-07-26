from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware.trustedhost import TrustedHostMiddleware


allowed_ips = ["127.0.0.1", "113.111.11.68"]


async def ip_whitelist_middleware(request: Request, call_next):
    if request.client.host not in allowed_ips:
        raise HTTPException(status_code=403, detail="Forbidden")
    response = await call_next(request)
    return response