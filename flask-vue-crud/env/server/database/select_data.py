from database import config
import psycopg2

def retrieve_stock_list():
    conn = None
    try:
        params = config.config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("SELECT * FROM userstocklist")
        #print("The number of parts: ", cur.rowcount)
        row = cur.fetchone()

        #while row is not None:
            #row = cur.fetchone()
        #print(row)

        cur.close()
        return row
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def retrieve_account_info(username):
    conn = None
    try:
        params = config.config()
        user_name = username.lower()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        select_sql = """SELECT * FROM users WHERE user_name = %s"""
        cur.execute(select_sql, (user_name,))
        user_data = cur.fetchone()
        return user_data
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return str(error)
    finally:
        if conn is not None:
            conn.close()
