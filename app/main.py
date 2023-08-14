from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import Page, add_pagination, paginate
from .serializers import userSerializers
# from app.config import settings
from app.routers import auth ,role_based #, user, posts
from .database import Employee
from .schemas import EmployeeOut

app = FastAPI()
origins = [
    # "http://localhost:3000",
    # "localhost:3000",
    # "http://localhost:3001",
    # "localhost:3001",
    # "http://192.168.1.16",
    # "http://192.168.1.16:3000",
    # "192.168.1.16:3000",
    # "http://192.168.1.152",
    # "http://192.168.1.152:3000"
    # "192.168.1.152:3000"
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(role_based.router, tags=['Role Based'], prefix='/api')

app.include_router(auth.router, tags=['Auth'], prefix='')
# app.include_router(user.router, tags=['User'], prefix='/api/users')
# app.include_router(posts.router, tags=['Post'], prefix='/api/posts')


@app.get('/api/healthchecker')
def root():
    return {
        "message": "welcome to fastapi :)"
    }
    
    





add_pagination(app)