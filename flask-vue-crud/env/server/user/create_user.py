from database import config
import psycopg2
import hashlib

def user_creation(user_data):
    full_name = user_data['fullname'].lower()
    user_name = user_data['username'].lower()
    user_password = user_data['password']
    user_email = user_data['email'].lower()
    user_stocks = ' '.join(user_data['stocks'])
    if user_stocks == '':
        user_stocks = 'aapl goog amzn fb msft'
        print('WE ADDED STOCKS!!!!')
        print(user_stocks)
    user_password = user_password.encode()
    user_password = hashlib.sha256(user_password).hexdigest()
    select_sql = """SELECT user_stock_list FROM users WHERE user_name = %s"""
    sql = """INSERT INTO users(fullname, user_name, user_password, user_email, user_stock_list)
            VALUES(%s, %s, %s, %s, %s)"""
    #print(user_data)
    try:
        # read database configuration
        params = config.config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # make sure user name and email aren't duplicates
        cur.execute("SELECT user_name, user_email, user_stock_list FROM users") 
        row = cur.fetchall()
        iterator = 0
        while row is not None:
            (username, email, stocklist) = row[iterator]
            if username == user_name:
                raise Exception('Username is already registered')
            elif email == user_email:
                raise Exception('Email is already registered')
            iterator += 1
        #print(full_name, user_name, user_password, user_email, user_stocks)
        #Add the data into the database
        cur.execute(sql,(full_name, user_name, user_password, user_email, user_stocks))
        # commit the changes to the database
        conn.commit()
        cur.execute(select_sql, (user_name,))
        stocklist = cur.fetchone()
        # close communication with the database
        cur.close()
        stocklist = ''.join(stocklist)
        #return the stocklist to the client
        return stocklist
        # execute the INSERT statement
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return str(error)
    finally:
        if conn is not None:
            conn.close()

def user_signin(user_data):
    username = user_data['username'].lower()
    user_password = user_data['password']
    user_password = user_password.encode()
    user_password = hashlib.sha256(user_password).hexdigest()
    #conn = None
    sql = """SELECT * FROM users WHERE user_name = %s"""
    try:
        params = config.config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql, (username,))
        #print("The number of parts: ", cur.rowcount)
        row = cur.fetchone()
        print(row)
        if row == None:
            raise Exception('Bad Username')
        (_, _, _, pwd, _, stocks) = row #Deconstruct the tuple
        if pwd == user_password:
            print('ACCESS GRANTED!')
            cur.close()
            return stocks
        else:
            print('Bad Password')
            raise Exception('Bad Password')
        #while row is not None:
            #row = cur.fetchone()
        #print(row)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return str(error)
    finally:
        if conn is not None:
            conn.close()

def stock_list(user_name, stock_list):
    sql = """UPDATE users
                SET user_stock_list = %s
                WHERE user_name = %s;"""
    conn = None
    #user_id = None
    try:
        # read database configuration
        params = config.config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the UPDATE statement
        user_name = user_name.lower()
        cur.execute(sql, (stock_list, user_name))
        # get the generated id back
        #user_id = cur.fetchone()
        print(user_name)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()