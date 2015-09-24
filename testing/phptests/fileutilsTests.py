from PythonJoernTests import *
from py2neo import Node

class FileutilsTests(PythonJoernTests):

    def testGetAstOfFile(self):
        """Searches for a file named AgaviArrayPathDefinition.class.php"""
        query = """g.V()
                   .getAstOfFile("AgaviArrayPathDefinition.class.php")"""
        result = self.j.runGremlinQuery(query)
        expect = [Node(childnum=0,id=12883,lineno=1,type="AST_STMT_LIST")]
        self.assertEquals(result, expect)

    def testToFile(self):
        """For some AST node in the file AgaviArrayPathDefinition.class.php,
        traverses back to the file node corresponding to this file."""
        query = """g.V().getAstOfFile("AgaviArrayPathDefinition.class.php").astNodes().next()
                   .toFile()"""
        result = self.j.runGremlinQuery(query)
        expect = [Node(id=12882,name="AgaviArrayPathDefinition.class.php",type="File")]
        self.assertEquals(result, expect)

    def testFileToPath(self):
        """For the file node of AgaviArrayPathDefinition.class.php, obtain the
        complete path."""
        query = """g.V().getAstOfFile("AgaviArrayPathDefinition.class.php").toFile()
                   .fileToPath()"""
        result = self.j.runGremlinQuery(query)
        expect = ["agavi/src/util/AgaviArrayPathDefinition.class.php"]
        self.assertEquals(result, expect)

