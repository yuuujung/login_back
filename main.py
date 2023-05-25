from db_connection import exec_query
from route import user
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from exception import *

app = FastAPI()

app.include_router(user.router, prefix="/user", tags=["유저"])
app.include_router(user.router, prefix="/user/chk", tags=["중복 아이디 체크"])
app.include_router(user.router, prefix="/user/login", tags=["로그인"])


@app.get("/")
async def root():
    return {"message": "Hello World"}


origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(USERDBRequestFailException)
async def db_request_exception_handler(request: Request, exc: USERDBRequestFailException):
    return JSONResponse(status_code=400, content=exc.response_content)
