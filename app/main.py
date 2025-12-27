from fastapi import FastAPI
from .router import poste, user, auth, vote
from . import models, config
from .database import engine


models.Base.metadata.create_all(bind=engine)


app = FastAPI()

@app.get("/healthcheck", tags=["Health Check"])
def health_check():
    print(config.settings)
    return {"status": "OK"}

app.include_router(poste.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


