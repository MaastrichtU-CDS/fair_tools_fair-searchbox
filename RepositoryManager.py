class RepositoryManager:
    rdflib = __import__('rdflib')

    def __init__(self, rdfFileList):
        self.graph = self.rdflib.Graph()

        for rdfFile in rdfFileList:
            try:
                self.graph.parse(rdfFile)
            except:
                print("Could not load %s - is the file reachable? Ignoring for now." % rdfFile)
    
    def searchForText(self, text):
        queryResult = self.graph.query("""
            PREFIX vektis: <https://www.vektis.nl/intelligence/open-data/ontologie/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>

            SELECT DISTINCT ?class ?classLabel ?classComment ?classLocation
            WHERE {
                ?class rdfs:label ?classLabel.

                ?class ?predicate ?searchText.

                OPTIONAL {?class rdfs:comment ?classComment}.
                OPTIONAL {?class vektis:Open_Data_Locatie ?classLocation}.

                FILTER(REGEX(?searchText, ".*%s.*", "i")).
            } ORDER BY DESC(?classLocation)
        """ % text)
        return queryResult

    def searchForUri(self, uri):
        queryResult = self.graph.query("""
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>

            SELECT DISTINCT ?object ?objectLabel ?objectType ?objectTypeLabel
            WHERE {
                BIND (<%s> AS ?object).
                ?object rdf:type ?objectType.
                OPTIONAL { ?object rdfs:label ?objectLabel. }.
                OPTIONAL { ?objectType rdfs:label ?objectTypeLabel. }.
            }
        """ % uri)
        return queryResult
    def getPropertiesForUri(self, uri):
        queryResult = self.graph.query("""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>

        SELECT DISTINCT ?outPredicate ?outPredicateLabel ?outObject ?outObjectLabel ?outObjectLiteral
        WHERE {
            BIND (<%s> AS ?object).
            ?object ?outPredicate ?outObject.
            OPTIONAL{ ?outPredicate rdfs:label ?outPredicateLabel. }.
            OPTIONAL{ ?outObject rdfs:label ?outObjectLabel. }.
            BIND (isIRI(?outObject) AS ?outObjectIRI).
        } ORDER BY ?outPredicate
        """ % uri)
        return queryResult
    def getReferencingObjects(self, uri):
        queryResult = self.graph.query("""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>

        SELECT DISTINCT ?inPredicate ?inPredicateLabel ?inObject ?inObjectLabel ?inObjectIRI
        WHERE {
            BIND (<%s> AS ?object).
            ?inObject ?inPredicate ?object.
            OPTIONAL{ ?inPredicate rdfs:label ?inPredicateLabel. }.
            OPTIONAL{ ?inObject rdfs:label ?inObjectLabel. }.
            BIND (isIRI(?inObject) AS ?inObjectIRI).
        } ORDER BY ?inPredicate
        """ % uri)
        return queryResult