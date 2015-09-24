from PythonJoernTests import *
from py2neo import Node

class MatchTests(PythonJoernTests):

    def testMatch(self):
        """Searches all nodes of type AST_STATIC_CALL in agavi/src/version.php"""
        query = """g.V().getAstOfFile("version.php")
                   .match{ it.type == TYPE_STATIC_CALL }"""
        result = self.j.runGremlinQuery(query)
        expect = [Node(childnum=9,id=120,lineno=54,type="AST_STATIC_CALL"),
                  Node(childnum=8,id=113,lineno=52,type="AST_STATIC_CALL"),
                  Node(childnum=7,id=92,lineno=47,type="AST_STATIC_CALL"),
                  Node(childnum=6,id=45,lineno=38,type="AST_STATIC_CALL"),
                  Node(childnum=5,id=38,lineno=36,type="AST_STATIC_CALL"),
                  Node(childnum=4,id=31,lineno=35,type="AST_STATIC_CALL"),
                  Node(childnum=3,id=24,lineno=34,type="AST_STATIC_CALL"),
                  Node(childnum=2,id=17,lineno=33,type="AST_STATIC_CALL"),
                  Node(childnum=1,id=10,lineno=32,type="AST_STATIC_CALL"),
                  Node(childnum=0,id=3,lineno=30,type="AST_STATIC_CALL"),
                  Node(childnum=1,id=107,lineno=49,type="AST_STATIC_CALL"),
                  Node(childnum=1,id=136,lineno=56,type="AST_STATIC_CALL"),
                  Node(childnum=0,id=100,lineno=48,type="AST_STATIC_CALL"),
                  Node(childnum=0,id=77,lineno=42,type="AST_STATIC_CALL"),
                  Node(childnum=1,id=70,lineno=41,type="AST_STATIC_CALL"),
                  Node(childnum=0,id=129,lineno=55,type="AST_STATIC_CALL"),
                  Node(childnum=1,id=85,lineno=43,type="AST_STATIC_CALL"),
                  Node(childnum=1,id=63,lineno=40,type="AST_STATIC_CALL"),
                  Node(childnum=0,id=56,lineno=39,type="AST_STATIC_CALL")
        ]
        self.assertEquals(result, expect)

    def testMatchParents(self):
        """Searches all parent nodes of those nodes that correspond to the
        string 'agavi.major_version' in agavi's version.php, then
        looks for parent nodes that correspond to static calls, and
        returns these. (The string 'agavi.major_version' appears
        twice; the first is within a static call, and the second is
        within *two* nested static calls, so we expect to get three
        nodes as a result here.)"""
        query = """g.V().getAstOfFile("version.php").match{ it.code == "agavi.major_version" }
                   .matchParents{ it.type == TYPE_STATIC_CALL }"""
        result = self.j.runGremlinQuery(query)
        expect = [Node(childnum=1,id=10,lineno=32,type="AST_STATIC_CALL"),
                  Node(childnum=0,id=56,lineno=39,type="AST_STATIC_CALL"),
                  Node(childnum=6,id=45,lineno=38,type="AST_STATIC_CALL")
        ]
        self.assertEquals(result, expect)

    def testArg(self):
        """Searches all call expressions in AgaviContext.class.php, filters
        those where the name of the called function starts with 'get',
        and returns all the first arguments to these calls."""
        query = """g.V().getAstOfFile("AgaviContext.class.php")
                   .arg("get",0)"""
        result = self.j.runGremlinQuery(query)
        expect = [Node(childnum=0,funcid=20145,id=20161,lineno=198,type="AST_VAR"),
                  Node(childnum=0,funcid=20218,id=20248,lineno=242,type="AST_VAR"),
                  Node(childnum=0,code="core.config_dir",funcid=20399,id=20417,lineno=321,type="string"),
                  Node(childnum=0,code="core.context_implementation",funcid=20263,id=20337,lineno=286,type="string"),
                  Node(childnum=0,code="core.default_context",funcid=20263,id=20292,lineno=279,type="string"),
                  Node(childnum=0,code="core.model_dir",funcid=20471,id=20561,lineno=371,type="string"),
                  Node(childnum=0,code="core.module_dir",funcid=20471,id=20620,lineno=386,type="string")
        ]
        self.assertEquals(result, expect)

    def testParam(self):
        """Searches for all parameter nodes in AgaviAction.class.php whose name matches /n.*/"""
        query = """g.V().getAstOfFile("AgaviAction.class.php")
                   .param("n.*")"""
        result = self.j.runGremlinQuery(query)
        expect = [Node(childnum=0,funcid=75541,id=75543,lineno=297,type="AST_PARAM"),
                  Node(childnum=0,funcid=75517,id=75519,lineno=286,type="AST_PARAM"),
                  Node(childnum=0,funcid=75493,id=75495,lineno=275,type="AST_PARAM"),
                  Node(childnum=0,funcid=75469,id=75471,lineno=264,type="AST_PARAM"),
                  Node(childnum=0,funcid=75450,id=75452,lineno=253,type="AST_PARAM"),
                  Node(childnum=0,funcid=75431,id=75433,lineno=242,type="AST_PARAM"),
                  Node(childnum=0,funcid=75375,id=75377,lineno=209,type="AST_PARAM")
        ]
        self.assertEquals(result, expect)
