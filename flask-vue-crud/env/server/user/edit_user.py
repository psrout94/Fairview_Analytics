from database import config
import psycopg2
import hashlib

def chg_password(user_name, old_password, new_password):
    conn = None
    params = config.config()
    conn = psycopg2.connect(**params)
    username = user_name.lower()
    username = username.strip()
    print(username)
    select_sql = """SELECT user_password FROM users WHERE user_name = %s"""
    change_sql = """UPDATE users
                SET user_password = %s
                WHERE user_name = %s;"""
    try:
        cur = conn.cursor()
        cur.execute(select_sql, (username,))
        retrieved_password = cur.fetchone()
        retrieved_password = ''.join(retrieved_password)
        print(retrieved_password)
        old_password = old_password.encode()
        old_password = hashlib.sha256(old_password).hexdigest()
        print('Old Password: ' + old_password)
        if retrieved_password == old_password:
            new_password = new_password.encode()
            new_password = hashlib.sha256(new_password).hexdigest()
            cur.execute(change_sql, (new_password, username))
            conn.commit()
            cur.close()
            return 'Password Changed Successfully!'
        else:
            raise Exception('Bad Password')

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return ('Bad Password')
    finally:
        if conn is not None:
            conn.close()

def stock_list(user_name, stock_list):
    """ Edit the User's stock list """
    sql = """UPDATE users
                SET user_stock_list = %s
                WHERE user_name = %s;"""
    conn = None
    params = config.config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    try:
        # execute the UPDATE statement
        user_name = user_name.lower()
        user_name = user_name.strip()
        print(user_name)
        cur.execute(sql, (stock_list, user_name))
        conn.commit()
        # get the generated id back
        
        # commit the changes to the database
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return 'There is an error!'
    finally:
        if conn is not None:
            conn.close()
    return 'Success!'