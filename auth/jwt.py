from db_connection import exec_fetch_query
from exception import *
from fastapi import Header
from query import user as query

import jwt


secret_key = "rjsanfwn"
algorithm = ["HS256"]


# JWT로부터 LOADIT 'USER_ID'와 'ADMIN_USER_ID' 얻기
def get_user_id_from_jwt(token_header: str) -> str:
    try:
        print("토큰 진입 전")
        if not token_header:
            raise AuthHeaderNotIncludedException

        token = token_header[7:]
        print("토큰 생성 : ", token)
        # print(token_header)
        decoded_token = jwt.decode(token, secret_key, algorithms=algorithm)

        return decoded_token.get("identity")

    except (IndexError, jwt.PyJWTError):
        raise InvalidUserIdException
