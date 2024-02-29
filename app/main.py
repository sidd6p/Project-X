from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from . import models, database
from .routes import posts, users, auth, votes


models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {"message": "Hello World!"}


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)
