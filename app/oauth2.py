# fastapi_jwt_auth package to use the public and private keys, the RS256 algorithm

import base64
from jose import JWTError, jwt
from typing import List
from datetime import datetime, timedelta
from pydantic import BaseModel
from fastapi import Depends, HTTPException, status
from .serializers.userSerializers import userEntity
from app import schemas
from fastapi.security import OAuth2PasswordBearer
from .config import settings
from .database import User
from bson.objectid import ObjectId


schemas_auth = OAuth2PasswordBearer(tokenUrl="login")


# class Settings(BaseModel):
#     try:
#         print("=========================================")
#         authjwt_secret_key: str = "secret"
#         authjwt_algorithms: str = settings.JWT_ALGORITHM
#         authjwt_decode_algorithms: List[str] = [settings.JWT_ALGORITHM]
#         authjwt_token_location: set = {'cookies', 'headers'}
#         authjwt_access_cookie_key: str = 'access_token'
#         authjwt_refresh_cookie_key: str = 'refresh_token'
#         authjwt_cookie_csrf_protect: bool = False
#         authjwt_public_key: str = base64.b64decode(settings.JWT_PUBLIC_KEY).decode('utf-8')
#         authjwt_private_key: str = base64.b64decode(settings.JWT_PRIVATE_KEY).decode('utf-8')    
        
#     except Exception as e:
#         print("pydentic errors", e)    
    
# @AuthJWT.load_config
# def get_config():
#     return Settings()
    
    
def NotVerified(Exception):
    pass


def UserNotFound(Exception):
    pass

def create_access_token(data: dict()):
    
    encode_data = data.copy()
    
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES_IN)
    
    # encode_data.update({"exp", expire})
    encode_data['exp'] = expire
    print("encode_data", encode_data)
    token = jwt.encode(encode_data, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    return token

def verify_access_token(token: str, credential_exceptions):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        print("payload", payload)
        id : str = payload.get('user_id')
        if id is None:
            raise credential_exceptions
        token_data = schemas.TokenData(id=id)
    except JWTError as e:
        print("e", e)
        raise credential_exceptions
    
    return token_data



def require_user(token: str = Depends(schemas_auth)):
    try:
        credential_exceptions = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not to be validated.", headers={"WWW-Authenticate": "Bearer"})
        token = verify_access_token(token, credential_exceptions)

        
        user = userEntity(User.find_one({'_id': ObjectId(str(token.id))}))
        


        if not user:
            raise UserNotFound('User no longer exist')
    
    except Exception as e:
        print("e", e)
        error = e.__class__.__name__
        print(error)
        
        if error == 'MissingTokenError':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are not logged in"
            )
        
        if error == 'UserNotFound':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User no longer exist"
            )
        
        
        if error == 'NotVerified':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="please verify your account"
            )
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="token is no longer valid or expired")
    return user