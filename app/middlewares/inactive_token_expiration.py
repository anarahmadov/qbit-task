from fastapi import HTTPException, status
from datetime import datetime, timedelta
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from ..routers.utils import revoke_if_inactive


class InactiveTokenExpiration(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            token_id = request.headers.get("token_id")
            foo = revoke_if_inactive(token_id=token_id)
            if not foo:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail={"msg": "Session expired"},
                )

            return await call_next(request)
        except Exception as e:
            return HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"error": e.__class__.__name__, "messages": e.args},
            )
