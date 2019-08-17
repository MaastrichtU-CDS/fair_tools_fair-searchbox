from flask import Flask, Response, request, render_template
import json
from RepositoryManager import RepositoryManager
from pyjarowinkler import distance

# Init configuration file
configFile = open("config.json")
config = json.load(configFile)
configFile.close()

app = Flask('FAIR Searchbox')
repoManager = RepositoryManager(config["rdfDataFiles"])

@app.route('/')
def index():
    if "uri" in request.args:
        return showUri(request.args.get("uri"))
    
    return render_template("index.html")

@app.route('/', methods=["POST"])
def searchResult():
    data = request.form
    results = repoManager.searchForText(data["searchField"])

    myResults = [ ]
    for result in results:
        myResult = {
            "class": result["class"],
            "classLabel": result["classLabel"],
            "classComment": result["classComment"],
            "classLocation": result["classLocation"],
            "distance": distance.get_jaro_distance(data["searchField"], result["classLabel"], winkler=True)
        }
        myResults.append(myResult)
    
    myResults.sort(key=calculateResultScore, reverse=True)

    return render_template("searchBox.html", searchTerm=data["searchField"], termList=myResults)

def calculateResultScore(myResult):
    number = 0
    if myResult["classLocation"] is not None:
        number = 1
    return number + myResult["distance"]

def showUri(uri):
    uriResults = repoManager.searchForUri(uri)
    propertiesResults = repoManager.getPropertiesForUri(uri)
    referencingResults = repoManager.getReferencingObjects(uri)

    returnObj = { }
    for uriResult in uriResults:
        returnObj["object"] = uriResult.object
        returnObj["objectLabel"] = uriResult.objectLabel
        returnObj["objectType"] = uriResult.objectType
        returnObj["objectTypeLabel"] = uriResult.objectTypeLabel
        break
    
    return render_template("uriShow.html", uriInfo=returnObj, propertyList=propertiesResults, propertyListIn=referencingResults)

app.run(debug=True, host='0.0.0.0', port=5000)