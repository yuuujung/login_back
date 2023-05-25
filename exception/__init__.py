from mysql.connector.errors import Error as mysqlError


class USERDBRequestFailException(Exception):
    def __init__(self, error_object):
        self.error_object = error_object

        # DB 오류시 기본 응답 코드
        self.response_code = "DB_ERROR"
        self.response_message = "USER DB 요청에 실패했습니다."

        # DB에서 일어난 에러인지 체크
        if isinstance(error_object, mysqlError):
            # duplicate key
            if error_object.errno == 1062:
                self.response_code = "DUPLICATE"
                self.response_message = "중복된 항목이 있습니다."
                self.response_content = {
                    "code": "self.response_code",
                    "message": self.response_message,
                }

            # debug for development: TODO -> logger로 변경
            print(error_object)


# 요청에 Authorization Header 포함되지 않음
class AuthHeaderNotIncludedException(Exception):
    def __init__(self):
        self.message = "인증 헤더가 포함되지 않았습니다."
        print(self.message)

        self.response_content = {"code": "NO_AUTH_HEADER", "message": self.message}


# 잘못된 LOADIT USER_ID
class InvalidUserIdException(Exception):
    def __init__(self):
        self.message = "사용자를 찾을 수 없습니다."

        self.response_content = {"code": "NOT_FOUND", "message": self.message}
