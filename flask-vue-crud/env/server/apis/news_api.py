from flask import Flask, jsonify, request
from flask_cors import CORS
import json, requests, re
from time import localtime, strftime

def get_headlines():
    url = ('http://newsapi.org/v2/top-headlines?country=us&apiKey=cc2e08b8963244de91ddae8dcdb6fa0b')
    response = requests.get(url)
    return response.text

def get_everything(post_data):
    method = post_data['keyword']
    current_date = strftime("%Y-%m-%d", localtime())
    url = ('http://newsapi.org/v2/everything?q='+ method + '&from=' + current_date + '&sortBy=popularity&apiKey=cc2e08b8963244de91ddae8dcdb6fa0b')
    response = requests.get(url)
    return response.text