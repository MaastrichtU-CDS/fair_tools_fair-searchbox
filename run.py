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

@app.route("/reload")
def reload():
    # Init configuration file
    configFile = open("config.json")
    config = json.load(configFile)
    configFile.close()

    app = Flask('FAIR Searchbox')
    repoManager = RepositoryManager(config["rdfDataFiles"])

@app.route('/<path:path>')
def catch_all(path):
    accept = "application/turtle"
    uri = config["baseUri"] + path

    if "Accept" in request.headers:
        accept = str(request.headers["Accept"])
    
    if accept == "text/html" or accept == "application/xhtml+xml":
        return showUriHtml(uri)
    
    return showUriTurtle(uri)

@app.route('/')
def index():
    if "uri" in request.args:
        return showUriHtml(request.args.get("uri"))
    
    return render_template("index.html")

@app.route('/', methods=["POST"])
def searchResult():
    data = request.form
    results = repoManager.searchForText(data["searchField"])

    myResults = [ ]
    for result in results:
        myResult = {
            "class": result["class"],
            "matchedText": result["searchText"],
            "distance": distance.get_jaro_distance(data["searchField"], result["searchText"], winkler=True)
        }
        myResults.append(myResult)
    
    myResults.sort(key=calculateResultScore, reverse=True)

    return render_template("searchBox.html", searchTerm=data["searchField"], termList=myResults)

def calculateResultScore(myResult):
    return myResult["distance"]

def showUriHtml(uri):
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

def showUriTurtle(uri):
    uriContentsResult = repoManager.getPropertiesForUri(uri)
    outputString = ""
    for uriResult in uriContentsResult:
        if uriResult["outObjectIRI"]=="true":
            outputString += ("<%s> <%s> <%s>." % (uri, uriResult["outPredicate"], uriResult["outObject"]))
        else:
            outputString += ("<%s> <%s> \"%s\"." % (uri, uriResult["outPredicate"], uriResult["outObject"]))
        outputString += "\n"
    return Response(outputString, mimetype="application/turtle")

app.run(debug=True, host='0.0.0.0', port=5050)
