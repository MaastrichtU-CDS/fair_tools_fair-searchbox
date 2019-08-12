class RepositoryManager:
    rdflib = __import__('rdflib')

    def __init__(self, rdfFileList):
        self.graph = self.rdflib.Graph()

        for rdfFile in rdfFileList:
            self.graph.parse(rdfFile)
    
    def searchForText(self, text):
        queryResult = self.graph.query("""
            PREFIX vektis: <https://www.vektis.nl/intelligence/open-data/ontologie/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>

            SELECT DISTINCT ?class ?classLabel ?classComment ?classLocation
            WHERE {
                ?class rdfs:label ?classLabel.

                {
                    ?class rdfs:label ?searchText.
                } UNION {
                    ?class rdfs:comment ?searchText.
                } UNION {
                    ?class vektis:Open_Data_Locatie ?searchText.
                }

                OPTIONAL {?class rdfs:comment ?classComment}.
                OPTIONAL {?class vektis:Open_Data_Locatie ?classLocation}.

                FILTER(REGEX(?searchText, ".*%s.*", "i")).
            } ORDER BY DESC(?classLocation)
        """ % text)
        return queryResult