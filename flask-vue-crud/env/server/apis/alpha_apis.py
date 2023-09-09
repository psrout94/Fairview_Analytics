from flask import Flask, jsonify, request
from flask_cors import CORS
import json, requests, re

def process_forex(post_data):
    forex_function = post_data['function']
    currency_from = post_data['from_currency']
    currency_to = post_data['to_currency']
    if forex_function == "Currency Exchange Rate":
        forex_function = "currency_exchange_rate"
        external_url = 'https://www.alphavantage.co/query?function=' + forex_function + '&from_currency=' + currency_from + '&to_currency=' + currency_to + '&apikey=KKRDFLTBPYBWCFZR'
    if forex_function == "Daily":
        forex_function = "fx_daily"
        external_url = 'https://www.alphavantage.co/query?function=' + forex_function + '&from_symbol=' + currency_from + '&to_symbol=' + currency_to + '&apikey=KKRDFLTBPYBWCFZR'
    elif forex_function == "Weekly":
        forex_function = "fx_weekly"
        external_url = 'https://www.alphavantage.co/query?function=' + forex_function + '&from_symbol=' + currency_from + '&to_symbol=' + currency_to + '&apikey=KKRDFLTBPYBWCFZR'
    elif forex_function == "Monthly":
        forex_function = "fx_monthly"
        external_url = 'https://www.alphavantage.co/query?function=' + forex_function + '&from_symbol=' + currency_from + '&to_symbol=' + currency_to + '&apikey=KKRDFLTBPYBWCFZR'
    if forex_function == "Intraday":
        forex_function = 'fx_intraday'
        external_url = 'https://www.alphavantage.co/query?function=' + forex_function + '&from_symbol=' + currency_from + '&to_symbol=' + currency_to + '&interval=15min&apikey=KKRDFLTBPYBWCFZR'
    print(external_url)
    alpha_request = requests.get(external_url)
    return alpha_request

def process_time_series(post_data):
    data_option = post_data["dataoption"]
    stock_option = post_data["stockoption"]
    stock = post_data["stock"]
    if data_option == "Stock Time Series":
        data_option = "time_series_"
        external_url = 'https://www.alphavantage.co/query?function=' + data_option + stock_option + '&symbol=' + stock + '&interval=15min&apikey=KKRDFLTBPYBWCFZR'
    if stock_option == "Quote":
        data_option = "GLOBAL_QUOTE" 
        external_url = 'https://www.alphavantage.co/query?function=' + data_option + '&symbol=' + stock + '&interval=15min&apikey=KKRDFLTBPYBWCFZR'
    alpha_request = requests.get(external_url)
    print(alpha_request)
    return alpha_request

def process_crypto(post_data):
    crypto_function = post_data['function']
    currency_from = post_data['from_currency']
    currency_to = post_data['to_currency']
    if crypto_function == 'Crypto Daily':
        crypto_function = 'digital_currency_daily'
    elif crypto_function == 'Crypto Monthly':
        crypto_function = 'digital_currency_monthly'
    else:
        crypto_function = 'digital_currency_weekly'
    external_url = 'https://www.alphavantage.co/query?function=' + crypto_function + '&symbol=' + currency_from + '&market=' + currency_to + '&apikey=KKRDFLTBPYBWCFZR'
    print(external_url)
    alpha_request = requests.get(external_url)
    return alpha_request

def process_sector_performance(post_data):
    external_url = 'https://www.alphavantage.co/query?function=SECTOR&apikey=KKRDFLTBPYBWCFZR'
    alpha_request = requests.get(external_url)
    return alpha_request

def process_tech_indicators(post_data):
    try:
        tech_function = post_data['function']
        tech_symbol = post_data['symbol']
        tech_time = post_data['time_period']
        tech_series = post_data['series_type']
        if tech_function != 'vwap':
            external_url = 'https://www.alphavantage.co/query?function=' + tech_function + '&symbol=' + tech_symbol + '&interval=weekly&time_period=' + tech_time + '&series_type=' + tech_series + '&apikey=KKRDFLTBPYBWCFZR'
        else:
            external_url = 'https://www.alphavantage.co/query?function=' + tech_function + '&symbol=' + tech_symbol + '&interval=15min&apikey=KKRDFLTBPYBWCFZR'
        alpha_request = requests.get(external_url)
    except:
        alpha_request = 'Error Message'
    return alpha_request