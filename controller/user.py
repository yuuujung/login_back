from db_connection import connect_db, exec_query, exec_fetch_query
from query import user as query
from fastapi.encoders import jsonable_encoder
from starlette.status import *
from mysql.connector import errors
from datetime import datetime, timedelta
from exception import USERDBRequestFailException

import mysql
import jwt
import json


# 유저 정보 가져오기
def get_user(user_id):
    result = exec_fetch_query(query.SELECT_USER + ";", {"user_id": user_id})

    if not result:
        return HTTP_404_NOT_FOUND, {"message": "회원 정보를 찾을 수 없습니다.", "result": {}}

    result = {
        **jsonable_encoder(result[0]),
    }

    return HTTP_200_OK, {"message": "OK", "result": result}


def get_user_id(user_id):
    result = exec_fetch_query(query.SELECT_USER + ";", {"user_id": user_id})

    if result == []:
        return HTTP_200_OK, {"message": "success", "result": "0"}

    return HTTP_409_CONFLICT, {"message": "duplicate", "result": "1"}

    # if not result:
    #     return HTTP_200_OK

    # return HTTP_409_CONFLICT, {"code": "DUPLICATE", "message": "duplicate"}


def post_user(user_info):
    try:
        exec_query(query.INSERT_USER, user_info)

    except errors.Error as e:
        raise USERDBRequestFailException(e)

    return HTTP_200_OK


# 로그인
def post_user_login(login_info):
    """
    로그인
    """

    print(login_info)
    print(login_info["user_id"])
    print("벡엔드 controller까지 옴")

    query_result = exec_fetch_query(
        query.SELECT_USER_LOGIN_ID_PW,
        {
            "user_id": login_info["user_id"],
            "user_pw": login_info["user_pw"],
        },
    )

    if not query_result:
        return HTTP_403_FORBIDDEN, {
            "code": "FAILED",
            "message": "FAILED",
        }

    query_result = jsonable_encoder(query_result)

    # JWT 발행 시각
    issued_timestamp = datetime.utcnow()

    # JWT 만료 시각
    expiration_timestamp = datetime.utcnow() + timedelta(days=1)

    token = jwt.encode(
        {
            "identity": query_result[0].get("USER_ID"),
            "iat": issued_timestamp,
            "exp": expiration_timestamp,
            "type": "access",
        },
        "rjsanfwn",
    )

    # print(token)

    return HTTP_200_OK, {"code": "OK", "message": "OK", "token": f"Bearer {token}"}
