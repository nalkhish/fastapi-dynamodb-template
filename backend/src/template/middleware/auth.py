from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint


class AuthException(Exception):
    pass


class AuthMiddleware(BaseHTTPMiddleware):
    async def auth(self):
        """Auth or raise AuthException"""
        pass

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        try:
            await self.auth()
        except AuthException:
            return JSONResponse({"error": "Invalid credentials"}, status_code=401)

        response = await call_next(request)
        return response
