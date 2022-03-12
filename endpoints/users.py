
from fastapi import APIRouter, Body, Depends, HTTPException
from dependency_injector.wiring import Provide, inject
from fastapi.security import OAuth2PasswordRequestForm


from infrastructure.container import Container
from auth.auth_handler import AuthHandler
from models.user_model import UserDbModel, UserLoginModel
from db_connections.mongo_db_connection import MongoDbConnection

router = APIRouter()

@router.post('/user/signup', status_code=202)
@inject
async def user_signup(
    mongo_db: MongoDbConnection = Depends(
        Provide[Container.mongo_db_connection_provider]
    ),
    user: UserLoginModel = Body(...),
    auth: AuthHandler = Depends(
        Provide[Container.auth_provider]
    )
):
    # return auth.signJWT(user.username)
    psw_hashed = auth.get_password_hash(user.password)
    user = UserDbModel(username=user.username, hashed_password=psw_hashed)
    res = mongo_db.add_user(user)
    print(res)
    if res == -1:
        raise HTTPException(status_code=400, detail="Username is already taken")
    return auth.signJWT(user.username)

@router.post("/token")
@inject
async def token(
    mongo_db: MongoDbConnection = Depends(
        Provide[Container.mongo_db_connection_provider]
    ),
    auth: AuthHandler = Depends(
        Provide[Container.auth_provider]
    ),
    user: UserLoginModel = Body(...),
):
    userDb: UserDbModel = mongo_db.get_user(user.username)
    if not userDb:
        print("yes")
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    if not auth.verify_password(user.password, userDb.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    return auth.signJWT(user.username)