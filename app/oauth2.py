
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

#-------------------------------------------------------------------------------
# Function to create access token
#-------------------------------------------------------------------------------
def create_access_token(data: dict):
    """
    Docstring for create_access_token
    
    :param data: Description
    :type data: dict
    """
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    to_encode.update({"iat": datetime.utcnow()})
    to_encode.update({"nbf": datetime.utcnow()})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

#-------------------------------------------------------------------------------
# Function to verify access token   
#-------------------------------------------------------------------------------
def verify_access_token(token: str, credentials_exception):
    """
    Docstring for verify_access_token
    
    :param token: Description
    :type token: str
    :param credentials_exception: Description
    """
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])

        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = schemas.TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception
    return token_data


#-------------------------------------------------------------------------------
# Function to get current user
#-------------------------------------------------------------------------------
def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Docstring for get_current_user
    
    :param token: Description
    :type token: str
    :return: Description
    :rtype: TokenData
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}, 
    )
    return verify_access_token(token=token, credentials_exception=credentials_exception)