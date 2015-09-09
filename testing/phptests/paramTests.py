from PythonJoernTests import *
from py2neo import Node

class ParamTests(PythonJoernTests):

    def testParamsToNames(self):
        """Searches for all parameters in the file
        AgaviContext.class.php and returns their names."""
        query = """g.V().getAstOfFile("AgaviContext.class.php").match{ it.type == TYPE_PARAM }
                   .paramsToNames()"""
        result = self.j.runGremlinQuery(query)
        expect = [Node(childnum=1,code="parameters",index=20485,lineno=358,type="string"),
                  Node(childnum=1,code="moduleName",index=20479,lineno=358,type="string"),
                  Node(childnum=1,code="modelName",index=20475,lineno=358,type="string"),
                  Node(childnum=1,code="profile",index=20267,lineno=275,type="string"),
                  Node(childnum=1,code="name",index=20222,lineno=239,type="string"),
                  Node(childnum=1,code="for",index=20149,lineno=196,type="string"),
                  Node(childnum=1,code="info",index=20130,lineno=179,type="string"),
                  Node(childnum=1,code="for",index=20126,lineno=179,type="string"),
                  Node(childnum=1,code="for",index=20098,lineno=163,type="string"),
                  Node(childnum=1,code="name",index=20071,lineno=133,type="string")
              ]
        self.assertEquals(result, expect)

    def testParamsToTypes(self):
        """Searches for all parameters in the file
        AgaviContext.class.php and returns their types."""
        query = """g.V().getAstOfFile("AgaviContext.class.php").match{ it.type == TYPE_PARAM }
                   .paramsToTypes()"""
        result = self.j.runGremlinQuery(query)
        expect = [Node(childnum=0,flags=["TYPE_ARRAY"],index=20484,lineno=358,type="AST_TYPE"),
                  Node(childnum=0,index=20478,lineno=358,type="NULL"),
                  Node(childnum=0,index=20474,lineno=358,type="NULL"),
                  Node(childnum=0,index=20266,lineno=275,type="NULL"),
                  Node(childnum=0,index=20221,lineno=239,type="NULL"),
                  Node(childnum=0,index=20148,lineno=196,type="NULL"),
                  Node(childnum=0,flags=["TYPE_ARRAY"],index=20129,lineno=179,type="AST_TYPE"),
                  Node(childnum=0,index=20125,lineno=179,type="NULL"),
                  Node(childnum=0,index=20097,lineno=163,type="NULL"),
                  Node(childnum=0,index=20070,lineno=133,type="NULL")
              ]
        self.assertEquals(result, expect)

    def testParamsToDefaults(self):
        """Searches for all parameters in the file
        AgaviContext.class.php and returns their default values."""
        query = """g.V().getAstOfFile("AgaviContext.class.php").match{ it.type == TYPE_PARAM }
                   .paramsToDefaults()"""
        result = self.j.runGremlinQuery(query)
        expect = [Node(childnum=2,index=20486,lineno=358,type="AST_CONST"),
                  Node(childnum=2,index=20480,lineno=358,type="AST_CONST"),
                  Node(childnum=2,index=20476,lineno=358,type="NULL"),
                  Node(childnum=2,index=20268,lineno=275,type="AST_CONST"),
                  Node(childnum=2,index=20223,lineno=239,type="AST_CONST"),
                  Node(childnum=2,index=20150,lineno=196,type="NULL"),
                  Node(childnum=2,index=20131,lineno=179,type="NULL"),
                  Node(childnum=2,index=20127,lineno=179,type="NULL"),
                  Node(childnum=2,index=20099,lineno=163,type="NULL"),
                  Node(childnum=2,index=20072,lineno=133,type="NULL")
              ]
        self.assertEquals(result, expect)

