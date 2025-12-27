from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import models, utils, oauth2
from ..database import get_db
router = APIRouter( prefix="/auth" ,tags=["Authentication"])

#-------------------------------------------------------------------------------
# User Login Endpoint
#-------------------------------------------------------------------------------
@router.post("/login",    
             status_code= status.HTTP_200_OK, description="Authenticate a user and return user details",
             summary="User Login Endpoint", response_description="The authenticated user details")
def login_user(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Docstring for login_user
    
    :param user_credentials: Description
    :type user_credentials: schemas.UserLogin
    :param db: Description
    :type db: Session
    """
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    access_token = oauth2.create_access_token(data = {"sub": str(user.id)})

    return {"access_token": access_token, "token_type": "bearer"}