from PythonJoernTests import *
from py2neo import Node

class ParamTests(PythonJoernTests):

    def testParamsToNames(self):
        """Searches for all parameters in the file
        AgaviContext.class.php and returns their names."""
        query = """g.V().getAstOfFile("AgaviContext.class.php").match{ it.type == TYPE_PARAM }
                   .paramsToNames()"""
        result = self.j.runGremlinQuery(query)
        expect = [Node(childnum=1,code="parameters",funcid=20471,id=20485,lineno=358,type="string"),
                  Node(childnum=1,code="moduleName",funcid=20471,id=20479,lineno=358,type="string"),
                  Node(childnum=1,code="modelName",funcid=20471,id=20475,lineno=358,type="string"),
                  Node(childnum=1,code="profile",funcid=20263,id=20267,lineno=275,type="string"),
                  Node(childnum=1,code="name",funcid=20218,id=20222,lineno=239,type="string"),
                  Node(childnum=1,code="for",funcid=20145,id=20149,lineno=196,type="string"),
                  Node(childnum=1,code="info",funcid=20122,id=20130,lineno=179,type="string"),
                  Node(childnum=1,code="for",funcid=20122,id=20126,lineno=179,type="string"),
                  Node(childnum=1,code="for",funcid=20094,id=20098,lineno=163,type="string"),
                  Node(childnum=1,code="name",funcid=20067,id=20071,lineno=133,type="string")
        ]
        self.assertEquals(result, expect)

    def testParamsToTypes(self):
        """Searches for all parameters in the file
        AgaviContext.class.php and returns their types."""
        query = """g.V().getAstOfFile("AgaviContext.class.php").match{ it.type == TYPE_PARAM }
                   .paramsToTypes()"""
        result = self.j.runGremlinQuery(query)
        expect = [Node(childnum=0,flags=["TYPE_ARRAY"],funcid=20471,id=20484,lineno=358,type="AST_TYPE"),
                  Node(childnum=0,funcid=20471,id=20478,lineno=358,type="NULL"),
                  Node(childnum=0,funcid=20471,id=20474,lineno=358,type="NULL"),
                  Node(childnum=0,funcid=20263,id=20266,lineno=275,type="NULL"),
                  Node(childnum=0,funcid=20218,id=20221,lineno=239,type="NULL"),
                  Node(childnum=0,funcid=20145,id=20148,lineno=196,type="NULL"),
                  Node(childnum=0,flags=["TYPE_ARRAY"],funcid=20122,id=20129,lineno=179,type="AST_TYPE"),
                  Node(childnum=0,funcid=20122,id=20125,lineno=179,type="NULL"),
                  Node(childnum=0,funcid=20094,id=20097,lineno=163,type="NULL"),
                  Node(childnum=0,funcid=20067,id=20070,lineno=133,type="NULL")
        ]
        self.assertEquals(result, expect)

    def testParamsToDefaults(self):
        """Searches for all parameters in the file
        AgaviContext.class.php and returns their default values."""
        query = """g.V().getAstOfFile("AgaviContext.class.php").match{ it.type == TYPE_PARAM }
                   .paramsToDefaults()"""
        result = self.j.runGremlinQuery(query)
        expect = [Node(childnum=2,funcid=20471,id=20486,lineno=358,type="AST_CONST"),
                  Node(childnum=2,funcid=20471,id=20480,lineno=358,type="AST_CONST"),
                  Node(childnum=2,funcid=20471,id=20476,lineno=358,type="NULL"),
                  Node(childnum=2,funcid=20263,id=20268,lineno=275,type="AST_CONST"),
                  Node(childnum=2,funcid=20218,id=20223,lineno=239,type="AST_CONST"),
                  Node(childnum=2,funcid=20145,id=20150,lineno=196,type="NULL"),
                  Node(childnum=2,funcid=20122,id=20131,lineno=179,type="NULL"),
                  Node(childnum=2,funcid=20122,id=20127,lineno=179,type="NULL"),
                  Node(childnum=2,funcid=20094,id=20099,lineno=163,type="NULL"),
                  Node(childnum=2,funcid=20067,id=20072,lineno=133,type="NULL")
        ]
        self.assertEquals(result, expect)

