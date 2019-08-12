from flask import Flask, Response, request
import json
import rdflib

app = Flask('FAIR Searchbox')

# Init configuration file
configFile = open("config.json")
config = json.load(configFile)
configFile.close()

@app.route('/')
def index():
    return "Hello, World"

app.run(debug=True, host='0.0.0.0', port=5000)