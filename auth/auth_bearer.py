from pydantic import BaseModel
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .auth_handler import AuthHandler


class JWTBearer(HTTPBearer):
    def __init__(self, auth: AuthHandler, auto_error: bool = True ):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.__auth = auth()
        
    async def __call__(self, request: Request):
        credentials: str = request.headers.get('Authorization')
        if credentials:
            credentials=credentials.split(" ")[-1]
            if not self.verify_jwt(credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False
        print("verifying")
        try:
            payload = self.__auth.decodeJWT(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid