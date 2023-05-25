from fastapi import APIRouter, Header, Request, Query, Body
from fastapi.responses import JSONResponse
from auth.jwt import get_user_id_from_jwt
from controller.user import *
from model.user import *


router = APIRouter()


@router.get("", summary="유저 정보 조회", description="토큰으로 유저 정보 조회")
def route_get_user(Authorization: str = Header(None)):
    print(Authorization)
    user_id = get_user_id_from_jwt(Authorization)
    status_code, result = get_user(user_id)

    return JSONResponse(status_code=status_code, content=result)


@router.get("/chk", description="아이디 가져오기")
def route_get_user_id(user_id):
    # print(user_id)
    status_code, result = get_user_id(user_id)

    return JSONResponse(status_code=status_code, content=result)


@router.post("", description="유저 등록")
def route_post_user(user_info: dict):
    # print(user_info)
    status_code = post_user(user_info)
    print("유저 등록")
    return JSONResponse(status_code=status_code, content={"status_code": status_code})


@router.post("/login", summary="로그인", description="로그인 및 토큰 발급")
def route_post_login(login_info: dict):
    status_code, result = post_user_login(login_info)

    return JSONResponse(status_code=status_code, content=result)
