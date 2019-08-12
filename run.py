from flask import Flask, Response, request, render_template
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
    return render_template("index.html")

@app.route('/', methods=["POST"])
def searchResult():
    data = request.form
    print(data)
    results = repoManager.searchForText(data["searchField"])

    return render_template("searchBox.html", searchTerm=data["searchField"], termList=results)

@app.route("/uri/<string:uri>")
def showUri(uri):
    return uri

app.run(debug=True, host='0.0.0.0', port=5000)