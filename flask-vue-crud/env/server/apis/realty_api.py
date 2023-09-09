from flask import Flask, jsonify, request
from flask_cors import CORS
import json, requests, re
from time import localtime, strftime

response = requests.get('https://www.zillow.com/webservice/GetSearchResults.htm?zws-id=X1-ZWz17aldo1dzbf_61q4u&address=2114+Bigelow+Ave&citystatezip=Seattle%2C+WA')
print(response.text)