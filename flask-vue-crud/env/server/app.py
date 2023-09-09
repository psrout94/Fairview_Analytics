from flask import Flask, jsonify, request, session, url_for
from flask_cors import CORS, cross_origin
import json, requests, re
import yfinance as yf
import pandas as pd
import psycopg2
from apis import alpha_apis, news_api, fred_api, export_api
from database import config, crud_db, select_data
from user import create_user, edit_user

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)    #This is what allows hot-swaps

# enable CORS
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.secret_key = b'\xc4\xeb\xbf1qH\x1e\x8f=8\xdc\x92;o\x84\x81'
#cors = CORS(app)
#app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/alpha', methods=['GET', 'POST'])
def alpha_vantage():
    if request.method == 'POST':
        post_data = request.get_json()
        print(post_data)
        if 'function' in post_data:
            if post_data['function'] == 'Sector':
                alpha_request = alpha_apis.process_sector_performance(post_data)
            elif post_data['function'] != 'Sector':
                if post_data['function'] == 'Currency Exchange Rate' or post_data['function'] == 'Monthly' or post_data['function'] == 'Daily' or post_data['function'] == 'Intraday' or post_data['function'] == 'Weekly':
                    alpha_request = alpha_apis.process_forex(post_data)
                elif post_data['function'] == 'Crypto Daily' or post_data['function'] == 'Crypto Monthly' or post_data['function'] == 'Crypto Weekly':
                    alpha_request = alpha_apis.process_crypto(post_data)
                else:
                    alpha_request = alpha_apis.process_tech_indicators(post_data)
        elif 'dataoption' in post_data:
            alpha_request = alpha_apis.process_time_series(post_data)
        if alpha_request != 'Error Message':
            parsed = json.loads(alpha_request.text)
        else:
            parsed = 'Error Message'
        if 'Error Message' in parsed:
            return 'Error'
        for key in parsed:
            new_key = re.sub('\ |\?|\.|\!|\-|\/|\;|\:', '', key)
            #print(new_key)
            new_key = re.sub('[(){}<>]', '', new_key)
            parsed[new_key] = parsed.pop(key)
        return json.dumps(parsed, indent=4, sort_keys=True)

@app.route('/yahoo', methods=['GET', 'POST'])
def ticker_function():
    try:
        post_data = request.get_json()
        if post_data == None:
            selected_tickers = 'wmt pg xom vz dis jnj mmm csco pfe rtx msft cat mrk intc trv nke hd mcd ko unh v ibm aapl cvx wba gs jpm dow axp ba'
        else:
            selected_tickers = post_data['stocklist'].replace(",", " ")
            username = post_data['username']
            print(username)
            print(selected_tickers)
            create_user.stock_list(username, selected_tickers)
        tickers = yf.Tickers(selected_tickers) #DJIA components
        history = tickers.history(period="1m")
        day_open = tickers.history(period="2d")
        day = day_open[['Close']]
        day = day.rename(columns={"Close": "a"})
        history = history[['Close']]
        day.reset_index(drop=True, inplace=True)
        history.reset_index(drop=True, inplace=True)
        response = pd.concat([history, day])    #Concat the two dataframes to combine to a single response object
        response = response.to_json(orient='split')
    except:
        response = 'Error'
        print('Error')
    return response

@app.route('/news', methods=['GET', 'POST'])
def news_api_function():
    if request.method == 'POST':
        post_data = request.get_json()
        print(post_data)
        if post_data['method'] == 'top-headlines':
            news_request = news_api.get_headlines()
        elif post_data['keyword'] == None:
            news_request = news_api.get_headlines()
        else:
            news_request = news_api.get_everything(post_data)
    else:
        news_request = news_api.get_headlines()
    return news_request

@app.route('/fred', methods=['GET', 'POST'])
def fred_api_function():
    if request.method == 'POST':
        post_data = request.get_json()
        fred_request = fred_api.series_data(post_data['data'])
    return fred_request.text

@app.route('/sec', methods=['GET', 'POST'])
def sec_api_function():
    if request.method == 'POST':
        post_data = request.get_json()
        print(post_data)
        return post_data
    else:
        return 0

@app.route('/agriculture', methods=['GET', 'POST'])
def quick_stats():
    if request.method == 'GET':
        return "You have reached the agriculture page"

@app.route('/economic', methods=['GET', 'POST'])
def economic_data():
    print('We up in here')

@app.route('/', methods=['GET'])
def home():
    return 200

@app.route('/export', methods=['GET', 'POST'])
def write_to_csv():
    if request.method == 'POST':
        request_data = request.get_json()
        return_value = export_api.to_csv(request_data)
        return return_value

@app.route('/userstockdata', methods=['GET', 'POST'])
def get_stock_data():
    stock_list = select_data.retrieve_stock_list()
    print(stock_list)
    return_object = json.dumps(stock_list)
    print(type(stock_list))
    return return_object

@app.route('/usercreation', methods=['GET', 'POST'])
def create_new_user():
    if request.method == 'POST':
        request_data = request.get_json()
        created_user = create_user.user_creation(request_data)
        return created_user

@app.route('/usersignin', methods=['GET', 'POST'])
def returning_user():
    if request.method == 'POST':
        request_data = request.get_json()
        stock_list = create_user.user_signin(request_data)
        return stock_list

@app.route('/getaccount', methods=['GET', 'POST'])
def get_account_data():
    if request.method == 'POST':
        request_data = request.get_json()
        user_name = request_data['username']
        acct_data = select_data.retrieve_account_info(user_name)
        response = list(acct_data)
        #response = json.dumps(acct_data)
        print(str(response[3]))
    return str(response)

@app.route('/changepassword', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        request_data = request.get_json()
        user_name = request_data['username']
        old_password = request_data['old']
        new_password = request_data['new']
        changes = edit_user.chg_password(user_name, old_password, new_password)
    return changes

@app.route('/changestocks', methods=['GET', 'POST'])
def change_stocks():
    if request.method == 'POST':
        request_data = request.get_json()
        user_name = request_data['username']
        stocks = request_data['stocklist']
        changes = edit_user.stock_list(user_name, stocks)
        return changes


"""@app.route('/setcookie', methods=['GET', 'POST'])
def setcookie():
    if request.method == 'POST':
        request_data = request.get_json()
        usernames = request_data['username']
        passwords = request_data['password']
        session['username'] = usernames
        #session['password'] = passwords
        response.set_cookie('YourSessionCookie', user.id)
    return jsonify(session) """

if __name__ == '__main__':
    #connect()
    app.run()