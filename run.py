from flask import Flask, Response, request
import json
from RepositoryManager import RepositoryManager

# Init configuration file
configFile = open("config.json")
config = json.load(configFile)
configFile.close()

app = Flask('FAIR Searchbox')
repoManager = RepositoryManager(config["rdfDataFiles"])

@app.route('/')
def index():
    return "Hello, World"

app.run(debug=True, host='0.0.0.0', port=5000)