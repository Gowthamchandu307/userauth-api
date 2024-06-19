from fastapi import  APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app import crud, models
from app.database import get_db
from pydantic import BaseModel
import secrets

router = APIRouter()

def generate_secret_key(length=32):
    """Generate a random secret key."""
    return secrets.token_hex(length)

SECRET_KEY = generate_secret_key()
ALGORITHM = "HS256"


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(username: str, password: str, db: Session):
    user = crud.get_user_by_username(db, username)
    if not user or not pwd_context.verify(password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid username or password')
    return user

def create_access_token(username: str, user_id: int, email: str, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id, 'email': email}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get('id')
        username: str = payload.get('sub')
        user_email: str = payload.get('email')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user.')
        return {'id': user_id, 'username': username, 'user_email': user_email}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')

@router.post("/token", tags=["token"], summary="Login to get an access token", response_model=models.TokenResponse)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid username or password')
    
    token_expires = timedelta(minutes=20)
    access_token = create_access_token(user.username, user.id, user.email, token_expires)
    return {'message': 'Login successful', 'access_token': access_token, 'token_type': 'bearer'}

@router.get("/token/user_authorized", tags=["token"], status_code=status.HTTP_200_OK, response_model=models.UserAuthorizedResponse)
async def user(current_user: models.User = Depends(get_current_user)):
    return {"message": "User authorized", "user": current_user}