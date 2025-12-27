from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter
from fastapi.params import Body
from typing import List, Optional

from sqlalchemy import func
from .. import models, schemas, oauth2
from ..database import get_db   
from sqlalchemy.orm import Session

router = APIRouter(prefix="/posts", tags=["Posts"])

#-------------------------------------------------------------------------------
# Get All Posts Endpoint
#-------------------------------------------------------------------------------
@router.get("/", response_model=List[schemas.PostOut],
            status_code=status.HTTP_200_OK, description="Retrieve all posts", 
            summary="Get All Post Endpoint" ,response_description="List of posts")
def get_posts(db:Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    """Retrieve all posts from the database."""
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    resultat = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id)
    return resultat

#-------------------------------------------------------------------------------
# Create Post Endpoint
#-------------------------------------------------------------------------------
@router.post("/createposts", response_model=schemas.PostResponse,
             status_code=status.HTTP_201_CREATED, description="Create a new post", 
             summary="Create Post Endpoint", response_description="The created post")
def create_post(payload: schemas.PostCreate = Body(...), db:Session = Depends(get_db),
                current_user_id: str = Depends(oauth2.get_current_user)):
    """Create a new post in the database."""
    new_post = models.Post(owner_id=current_user_id.user_id, **payload.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

#-------------------------------------------------------------------------------
# Get Post by ID Endpoint
#-------------------------------------------------------------------------------
@router.get("/{id}",response_model = schemas.PostResponse, 
            status_code=status.HTTP_200_OK, description="Retrieve a post by ID", 
            summary="Get Post by ID Endpoint", response_description="The requested post")
def get_post(id: int, db:Session = Depends(get_db)):
    """Retrieve a specific post by its ID from the database."""
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    return post


#-------------------------------------------------------------------------------
# Delete Post Endpoint
#-------------------------------------------------------------------------------
@router.delete("/{id}",response_model= None, 
               status_code=status.HTTP_204_NO_CONTENT, description="Delete a post by ID",
               summary="Delete Post Endpoint", response_description="No content")
def delete_post(id: int, db:Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    """Delete a specific post by its ID from the database."""
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    post = deleted_post.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")

    if post.owner_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT, 
                    content=f"Post with id: {id} has been deleted successfully", 
                    media_type="application/json", headers={"X-Deleted-Post-ID": str(id)})

#-------------------------------------------------------------------------------
# Update Post Endpoint
#-------------------------------------------------------------------------------
@router.put("/{id}", response_model= schemas.PostResponse, 
            status_code=status.HTTP_200_OK, description="Update a post by ID", 
            summary="Update Post Endpoint", response_description="The updated post")
def update_post_in_db(id: int, payload: schemas.PostUpdate = Body(...), db: Session = Depends(get_db)):
    """Update a specific post by its ID in the database."""
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")
    post_query.update(payload.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()