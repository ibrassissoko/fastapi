from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, validator, EmailStr



# --------------------------
# Modèle de base pour un utilisateur
# --------------------------
class UserBase(BaseModel):
    email: EmailStr = Field(..., description="Email address of the user")

# --------------------------
# Modèle pour la réponse d'un utilisateur
# --------------------------
class UserResponse(UserBase):
    id: UUID = Field(..., description="Unique identifier  of the user")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when the user was created")

    class Config:
        from_attributes = True
        json_schema_extra  = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "abc123@gmail.com",
                "created_at": "2024-01-01T12:00:00Z",
            }
        }



#--------------------------
# Modèle de base pour un post
#--------------------------
class PostBase(BaseModel):
    title: str = Field(..., max_length=100, description="Title of the post")
    content: str = Field(..., description="Content of the post")
    published: bool = Field(default=True, description="Publication status of the post")
    rating: Optional[int] = Field(None, ge=0, le=5, description="Rating of the post")
    

#--------------------------
# Modèle pour la création d'un post
#--------------------------
class PostCreate(PostBase):

    @validator('title')
    def title_no_bad_words(cls, v):
        bad_words = ['spam', 'advertisement', 'clickbait']
        if any(bad_word in v.lower() for bad_word in bad_words):
            raise ValueError('Title contains inappropriate content')
        return v
    
    @validator('content')
    def content_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Content must not be empty or whitespace')
        return v
    

    class config:
        json_schema_extra = {
            "example": {
                "title": "My First Post",
                "content": "This is the content of my first post.",
                "published": True
            }
        }

#--------------------------
# Modèle pour la réponse d'un post
#--------------------------
class PostResponse(PostBase):
    id: int = Field(..., description="Unique identifier of the post")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when the post was created")
    owner_id: UUID = Field(..., description="Identifier of the user who created the post")
    owner : UserResponse = Field(..., description="Details of the post owner")

    class config:
        from_attributes = True
        json_schema_extra  = {
            "example": {
                "id": 1,
                "title": "My First Post",
                "content": "This is the content of my first post.",
                "published": True,
                "rating": 5,
                "created_at": "2024-01-01T12:00:00Z"
            }
        }


# --------------------------
# Modèle pour la mise à jour d'un post
# --------------------------
class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=200, description="Title of the post")
    content: Optional[str] = Field(None, min_length= 1,description="Content of the post")
    published: Optional[bool] = Field(None, description="Publication status of the post")
    rating: Optional[int] = Field(None, ge=0, le=5, description="Rating of the post")

     # Validation personnalisée pour le titre
    @validator("title")
    def title_no_bad_words(cls, v):
        if v:  # seulement si le titre est fourni
            bad_words = ["spam", "fake", "test"]
            if any(word in v.lower() for word in bad_words):
                raise ValueError("Le titre contient des mots interdits")
        return v

    # Validation pour le contenu
    @validator("content")
    def content_not_empty(cls, v):
        if v and not v.strip():  # si fourni, il ne doit pas être vide
            raise ValueError("Le contenu ne peut pas être vide")
        return v

    class Config:
        from_attributes = True
        json_schema_extra  = {
            "example": {
                "title": "Titre mis à jour",
                "content": "Nouveau contenu du post",
                "published": False,
                "rating": 5
            }
        }

# --------------------------
# Modèle pour la réponse d'un post avec le nombre de votes
# --------------------------

class PostOut(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        from_attributes = True



# --------------------------
# Modèle pour la création d'un utilisateur
# --------------------------

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description="Password of the user")

    @validator("password")
    def password_strength(cls, v):
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return v
    
    @validator("email")
    def email_must_be_valid(cls, v):
        if "@" not in v:
            raise ValueError("Invalid email address")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "abc123@gmail.com",
                "password": "strongpassword123"
            }
        }
    

# --------------------------
# Modèle pour le login d'un utilisateur
# --------------------------
class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="Email address of the user")
    password: str = Field(..., description="Password of the user")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "abc123@gmail.com",
                "password": "strongpassword123"
            }
        }

# --------------------------
# Modèle pour le token d'authentification
# --------------------------
class Token(BaseModel):
    access_token: str = Field(..., description="Access token for authentication")
    token_type: str = Field(..., description="Type of the token, e.g., Bearer")

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }
# --------------------------
# Modèle pour les données du token
# --------------------------
class TokenData(BaseModel):
    user_id: Optional[UUID] = Field(None, description="Unique identifier of the user from the token")
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "550e8400-e29b-41d4-a716-446655440000"
            }
        }

# --------------------------
# Modèle pour le vote
# --------------------------
class Vote(BaseModel):
    post_id: int = Field(..., description="Identifier of the post to vote on")
    dir: int = Field(..., ge=0, le=1, description="Direction of the vote: 1 for upvote, 0 for remove vote")

    class Config:
        json_schema_extra = {
            "example": {
                "post_id": 1,
                "dir": 1
            }
        }