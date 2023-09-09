from flask import Flask, jsonify, request
from flask_cors import CORS
import json, requests, re
from time import localtime, strftime

def series_data(data):
    response = requests.get('https://api.stlouisfed.org/fred/series/observations?series_id=' + data + '&api_key=a8be1c3111f016463e43297ffa623faa&file_type=json')
    return response