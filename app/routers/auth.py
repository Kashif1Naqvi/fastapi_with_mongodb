from datetime import datetime, timedelta
from bson.objectid import ObjectId
from fastapi import APIRouter, Response, status, Depends, HTTPException
from app.serializers.userSerializers import userEntity, userResponseEntity, assignScreens
from .. import schemas, utils
from app import oauth2
# from app.oauth2 import AuthJWT
from ..config import settings
from ..database import User, UsersRoles, UserScreenRole, Screen
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()
ACCESS_TOKEN_EXPIRES_IN = settings.ACCESS_TOKEN_EXPIRES_IN
REFRESH_TOKEN_EXPIRES_IN = settings.REFRESH_TOKEN_EXPIRES_IN


# REGISTER USER
@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
async def register(payload: schemas.CreateUserSchema):
    
    user = User.find_one({"email": payload.email.lower()})
    if user:
        raise HTTPException(stauts_code=status.HTTP_409_CONFLICT, detail="Acccount already exist")

    if payload.password != payload.passwordConfirm:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password could not match")


    payload.password = utils.hash_password(payload.password)
    del payload.passwordConfirm
    payload.verified = True
    payload.email = payload.email.lower()
    payload.created_at = datetime.utcnow()
    payload.updated_at = payload.created_at
    result = User.insert_one(payload.dict())
    
    new_user = userResponseEntity(User.find_one({'_id': result.inserted_id}))
    
    return {"status": "success", "user": new_user}
    
    
#  LOGIN USER
@router.post('/login')
def login(user_credential: OAuth2PasswordRequestForm =  Depends()):
    try:
        user  = userEntity(User.find_one({'email': user_credential.username}))
        print("1")
        
        if not user:
            print("2")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Incorrect Email or password")    
        
        
        if not utils.verify_password(user_credential.password, user['password']):
            print("3")
            print("user_credential.password", user_credential.password)
            print("user_credential.username", user_credential.username)
            print("user['password']", user['password'])
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Incorrect Email or password")    
        print("4")
        print(user)
        
        screen_list = utils.get_screen_id(user["id"])
        
        token = oauth2.create_access_token(data={"user_id": user["id"]})
        
        
        return { "access_token": str(token), "token_type": "Bearer", "status": "success", "screens_list": screen_list, "username": user['name']}
    
    except Exception as e:
        print("login excpetion", e)

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Incorrect Email or password")    

# @router.post('/refresh')
# def refresh_token(response: Response, Authorized: AuthJWT = Depends()):
#     try:
#         # method to ensure that the refresh token cookie was included in the incoming request.
#         Authorized.jwt_refresh_token_required()
        
#         # method to retrieve the payload stored in the token.
#         user_id = Authorized.get_jwt_subject()
        
#         if not user_id:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
#                                 detail="Could not refresh access token")
#         user = userEntity(User.find_one({"_id": ObjectId(str(user_id))}))
        
        
#         if not user:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#                                 detail='The user belonging to this token no logger exist')
        
#         access_token = Authorized.create_access_token(
#             subject=str(user["id"]),
#             expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN)
#         )
        
#     except Exception as e:
#         error = e.__class__.__name__
#         if error == 'MissingTokenError':
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Please provide refresh token"
#             )
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    

#     response.set_cookie('access_token', access_token, ACCESS_TOKEN_EXPIRES_IN * 60,
#                         ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, False, 'lax')


#     response.set_cookies('logged_in', 'True', ACCESS_TOKEN_EXPIRES_IN * 60,
#                         ACCESS_TOKEN_EXPIRES_IN * 60 , '/', None, False, False, 'lax')
    
    
#     return {"status": "success", "access_token": access_token}


# @router.get('/logout', status_code=status.HTTP_200_OK)
# def logout(response: Response, user_id: str = Depends(oauth2.require_user)):
#     return {'status': 'success'}