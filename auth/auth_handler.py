import time
from typing import Dict
import jwt
from passlib.context import CryptContext

class AuthHandler:
    def __init__(self, secret: str, algorithm: str):
        self.__secret = secret
        self.__algorithm = algorithm
        self.__pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def token_response(self, token: str):
        return {
            "access_token": token,
            "token_type": 'bearer'
        }
    
    def signJWT(self, user_id: str, user_roler: str = 'user') -> Dict[str, str]:
        payload = {
            "user_id": user_id,
            "role": user_roler,
            "expires": time.time() + 3600
        }
        token = jwt.encode(payload, self.__secret, algorithm=self.__algorithm)
        return self.token_response(token)
    
    def decodeJWT(self, token: str) -> dict:
        try:
            decoded_token = jwt.decode(token, self.__secret, algorithms=[self.__algorithm])
            return decoded_token if decoded_token["expires"] >= time.time() else None
        except:
            return {}

    def verify_password(self, password, hashed_password):
        return self.__pwd_context.verify(password, hashed_password)

    def get_password_hash(self, password: str):
        return self.__pwd_context.hash(password)
    