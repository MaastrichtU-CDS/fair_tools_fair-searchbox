class RepositoryManager:
    rdflib = __import__('rdflib')
    def __init__(self, rdfFileList):
        self.graph = self.rdflib.Graph()
        for rdfFile in rdfFileList:
            self.graph.parse(rdfFile)