from pydantic import BaseModel
from fastapi_jwt_auth import AuthJWT
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi_jwt_auth import AuthJWT
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session


def init_auth(secret_key, get_db, usercrud, tokenUrl="/login"):
    """Parameters:
    secret_key: secret_key for JWT,
    get_db: Generator function,
    usercrud: usercrud object obtained by initialising CRUDUser,
    tokenUrl: Url to get access token

    Returns: login function and get_user function
    Please Note: JWT tokens are made from email attribute in User.
    """
    reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=tokenUrl)

    class Settings(BaseModel):
        authjwt_secret_key: str = secret_key

    @AuthJWT.load_config
    def get_config():
        return Settings()

    def login(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
        curuser = usercrud.authenticate(
            db, email=user.username, password=user.password
        )
        if not curuser:
            raise HTTPException(
                status_code=400, detail="Incorrect email or password")
        else:
            print(curuser)
            access_token = Authorize.create_access_token(
                subject=user.username, expires_time=24*60)
            return {"access_token": access_token,
                    "token_type": "bearer"}

    def get_user(token: str = Depends(reusable_oauth2), Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
        try:
            Authorize.jwt_required()
            current_user_email = Authorize.get_jwt_subject()
            person = usercrud.get_by_email(db, email=current_user_email)
            return person
        except Exception as e:
            print("Exception in get_user")
            return e
    return login, get_user
