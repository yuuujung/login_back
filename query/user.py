SELECT_USER = """
SELECT `USER_ID`
     , `USER_PW`
     , `USER_PHONE`
     , `USER_EMAIL`
  FROM USER.users
 WHERE USER_ID = %(user_id)s
"""
SELECT_USER_ID = """
SELECT USER_ID
FROM USER.users = %(user_id)s
"""
SELECT_USER_LOGIN_ID_PW = """
SELECT * 
  FROM USER.users
 WHERE USER_ID = %(user_id)s
   AND USER_PW = %(user_pw)s
;
"""
INSERT_USER = """
INSERT INTO USER.users(
  `USER_ID`,`USER_PW`, `USER_PHONE`, `USER_EMAIL`)
VALUE(
  %(user_id)s, %(user_pw)s, %(user_phone)s, %(user_email)s
);
"""
