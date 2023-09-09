from flask import Flask, jsonify, request
from flask_cors import CORS
import requests, re, csv

def to_csv(data):
    try:
        print('Gonna try this')
        #print(os.path.basename('/Users'))
        with open("/Users/pstout/Downloads/"+data["filename"]+".csv", "w+", newline='') as csvfile:
            fieldnames = ['Date', 'Value']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for value in data['data']:
                writer.writerow({'Date': value['date'], 'Value': value['value']})
            return 'Successfully Downloaded!'
    except:
        print("File Export Failed")
        return 'Download Failed'