from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter
from fastapi.params import Body
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(prefix="/user", tags=["Users"])


#-------------------------------------------------------------------------------
# User Registration Endpoint
#-------------------------------------------------------------------------------
@router.post("/register", response_model=schemas.UserResponse, 
             status_code=status.HTTP_201_CREATED, description="Register a new user",
             summary="User Registration Endpoint", response_description="The created user")
def create_user(user: schemas.UserCreate = Body(...), db: Session = Depends(get_db)):
    user.password = utils.hash_password(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

#-------------------------------------------------------------------------------
# Get User by id Endpoint
#-------------------------------------------------------------------------------
@router.get("/users/{id}", response_model=schemas.UserResponse,
            status_code=status.HTTP_200_OK, description="Retrieve a user by ID",
            summary="Get User by ID Endpoint", response_description="The requested user")
def get_user(id: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} was not found")
    return user