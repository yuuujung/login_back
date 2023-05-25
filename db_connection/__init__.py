# DB Connection Session 관리 및 CRUD METHOD
import mysql.connector
import mysql.connector.cursor
import logging


def get_DB_ACCESS_INFO():
    return {
        "host": "localhost",
        "user": "root",
        "password": "1387",
        "port": 3306,
        "database": "USER",
    }


def connect_db() -> mysql.connector.connection.MySQLConnection:
    conn = mysql.connector.connect(**get_DB_ACCESS_INFO(), autocommit=True)
    return conn


def close_db_connection(conn: mysql.connector.connection.MySQLConnection):
    conn.close()


# INSERT 문 (.SQL 파일 실행)
def exec_sql_file(sql_file, d_yyyymmdd, p_user_id):
    try:
        conn = connect_db()
        with open(sql_file, "r", encoding="UTF-8") as file:
            # sql = file.read().replace('{{ ds }}', d_yyyymmdd)
            sql_staging = file.read().replace("{{ ds }}", d_yyyymmdd)
            sql = sql_staging.replace("{{ params.user_id }}", p_user_id)
            # print(sql)
            cursor = conn.cursor()
            results = cursor.execute(sql, multi=True)
            for cur in results:
                # print('cursor:', cur)
                if cur.with_rows:
                    pass
                    # print('result:', cur.fetchall())
            conn.commit()
            close_db_connection(conn)
        return cursor.close()

    except Exception as err:
        close_db_connection(conn)
        logging.getLogger("logger").error("쿼리 실행 중 오류가 발생했습니다 :  " + repr(err))

        # pass
        raise err


global cursor


# INSERT 문 (한줄)
def exec_query(query_str, input_param="", get_insert_id=False):
    try:
        conn = connect_db()
        cursor: mysql.connector.connection.MySQLCursor = conn.cursor()
        cursor.execute(query_str, input_param)

        if get_insert_id:
            return cursor.lastrowid

        return cursor.rowcount

    except Exception as err:
        logging.getLogger("logger").error("쿼리 실행 중 오류가 발생했습니다 :  " + repr(err))
        raise err

    finally:
        cursor.close()
        close_db_connection(conn)


# SELECT 문
def exec_fetch_query(query_str, input_param="", get_insert_id=False):
    try:
        conn = connect_db()
        cursor: mysql.connector.connection.MySQLCursor = conn.cursor(dictionary=True)
        cursor.execute(query_str, input_param)
        result_list = cursor.fetchall()

        # print(cursor.statement)
        if get_insert_id:
            return cursor.lastrowid

        return result_list

    except Exception as err:
        logging.getLogger("logger").error("쿼리 실행 중 오류가 발생했습니다 :  " + repr(err))
        raise err

    finally:
        cursor.close()
        close_db_connection(conn)


# INSERT 문(여러줄)
def exec_multiple_queries(query_str, input_params=""):
    try:
        conn = connect_db()
        cursor: mysql.connector.connection.MySQLCursor = conn.cursor()
        cursor.executemany(query_str, input_params)

        # print("executed QUERY: ")
        # print(cursor.statement)

    except Exception as err:
        logging.getLogger("logger").error("쿼리 실행 중 오류가 발생했습니다 :  " + repr(err))
        raise err

    finally:
        cursor.close()
        close_db_connection(conn)


if __name__ == "__main__":
    print(get_DB_ACCESS_INFO())
    connect_db()
    print(exec_fetch_query("SELECT NOW()"))
