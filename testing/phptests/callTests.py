from PythonJoernTests import *
from py2neo import Node

class CallTests(PythonJoernTests):

    def testCallToArguments(self):
        """Searches all call expressions in test-repos/agavi/src/core/AgaviContext.class.php
        and retrieves their arguments"""
        query = """g.V().getAstOfFile("AgaviContext.class.php").match{ isCallExpression(it) }
                   .callToArguments()"""
        result = self.j.runGremlinQuery(query)
        expect = [Node(childnum=0,funcid=20399,id=20443,lineno=326,type="AST_ARRAY"),
                  Node(childnum=1,funcid=20145,id=20200,lineno=204,type="AST_DIM"),
                  Node(childnum=0,funcid=20145,id=20198,lineno=204,type="AST_VAR"),
                  Node(childnum=1,funcid=20054,id=20063,lineno=120,type="AST_CONST"),
                  Node(childnum=0,code="Cloning an AgaviContext instance is not allowed.",funcid=20054,id=20062,lineno=120,type="string"),
                  Node(childnum=0,funcid=20471,id=20504,lineno=361,type="AST_VAR"),
                  Node(childnum=0,funcid=20145,id=20161,lineno=198,type="AST_VAR"),
                  Node(childnum=0,funcid=20471,id=20806,lineno=428,type="AST_ARRAY"),
                  Node(childnum=0,code="AgaviISingletonModel",funcid=20471,id=20685,lineno=403,type="string"),
                  Node(childnum=2,funcid=20471,id=20516,lineno=362,type="AST_VAR"),
                  Node(childnum=1,code="_",funcid=20471,id=20515,lineno=362,type="string"),
                  Node(childnum=0,code="/",funcid=20471,id=20514,lineno=362,type="string"),
                  Node(childnum=1,flags=["TYPE_ARRAY"],funcid=20471,id=20822,lineno=430,type="AST_CAST"),
                  Node(childnum=0,funcid=20471,id=20820,lineno=430,type="AST_VAR"),
                  Node(childnum=0,funcid=20471,id=20654,lineno=394,type="AST_VAR"),
                  Node(childnum=0,funcid=20471,id=20641,lineno=390,type="AST_VAR"),
                  Node(childnum=1,funcid=20399,id=20419,lineno=321,type="AST_PROP"),
                  Node(childnum=0,flags=["BINARY_CONCAT"],funcid=20399,id=20411,lineno=321,type="AST_BINARY_OP"),
                  Node(childnum=0,funcid=20263,id=20315,lineno=284,type="AST_VAR"),
                  Node(childnum=1,funcid=20399,id=20436,lineno=323,type="AST_VAR"),
                  Node(childnum=0,funcid=20399,id=20434,lineno=323,type="AST_VAR"),
                  Node(childnum=0,funcid=20263,id=20385,lineno=292,type="AST_VAR"),
                  Node(childnum=0,funcid=20471,id=20578,lineno=375,type="AST_VAR"),
                  Node(childnum=0,funcid=20218,id=20248,lineno=242,type="AST_VAR"),
                  Node(childnum=1,funcid=20471,id=20667,lineno=396,type="AST_VAR"),
                  Node(childnum=0,code="Couldn't find class for Model %s",funcid=20471,id=20666,lineno=396,type="string"),
                  Node(childnum=0,funcid=20471,id=20604,lineno=384,type="AST_VAR"),
                  Node(childnum=0,funcid=20471,id=20547,lineno=369,type="AST_VAR"),
                  Node(childnum=0,code="core.config_dir",funcid=20399,id=20417,lineno=321,type="string"),
                  Node(childnum=1,funcid=20263,id=20338,lineno=286,type="AST_CALL"),
                  Node(childnum=0,code="core.context_implementation",funcid=20263,id=20337,lineno=286,type="string"),
                  Node(childnum=0,code="core.default_context",funcid=20263,id=20292,lineno=279,type="string"),
                  Node(childnum=1,funcid=20145,id=20182,lineno=200,type="AST_VAR"),
                  Node(childnum=0,code="No factory info for \"%s\"",funcid=20145,id=20181,lineno=200,type="string"),
                  Node(childnum=0,funcid=20471,id=20798,lineno=424,type="AST_VAR"),
                  Node(childnum=0,funcid=20471,id=20746,lineno=413,type="AST_VAR"),
                  Node(childnum=0,code="core.model_dir",funcid=20471,id=20561,lineno=371,type="string"),
                  Node(childnum=0,code="core.module_dir",funcid=20471,id=20620,lineno=386,type="string")
        ]
        self.assertEquals(result, expect)

    def testIthArguments(self):
        """Searches all call expressions in
        test-repos/agavi/src/core/AgaviContext.class.php and retrieves
        their third argument."""
        query = """g.V().getAstOfFile("AgaviContext.class.php").match{ isCallExpression(it) }
                   .ithArguments(2)"""
        result = self.j.runGremlinQuery(query)
        expect = [Node(childnum=2,funcid=20471,id=20516,lineno=362,type="AST_VAR")]
        self.assertEquals(result, expect)

    def testArgToCall(self):
        """Searches all call expressions in
        test-repos/agavi/src/core/AgaviContext.class.php, retrieves
        their arguments, traverses back to the call expressions and
        deduplicates. The result is the set of all call expressions
        that have at least one argument."""
        query = """g.V().getAstOfFile("AgaviContext.class.php").match{ isCallExpression(it) }.callToArguments()
                   .argToCall().dedup()"""
        result = self.j.runGremlinQuery(query)
        expect = [Node(childnum=1,funcid=20399,id=20439,lineno=326,type="AST_CALL"),
                  Node(childnum=3,funcid=20145,id=20193,lineno=204,type="AST_METHOD_CALL"),
                  Node(childnum=0,funcid=20054,id=20058,lineno=120,type="AST_CALL"),
                  Node(childnum=1,funcid=20471,id=20499,lineno=361,type="AST_STATIC_CALL"),
                  Node(childnum=1,funcid=20145,id=20156,lineno=198,type="AST_METHOD_CALL"),
                  Node(childnum=0,funcid=20471,id=20802,lineno=428,type="AST_CALL"),
                  Node(childnum=0,funcid=20471,id=20680,lineno=403,type="AST_METHOD_CALL"),
                  Node(childnum=0,funcid=20471,id=20510,lineno=362,type="AST_CALL"),
                  Node(childnum=0,funcid=20471,id=20815,lineno=430,type="AST_METHOD_CALL"),
                  Node(childnum=0,funcid=20471,id=20650,lineno=394,type="AST_CALL"),
                  Node(childnum=1,funcid=20471,id=20637,lineno=390,type="AST_CALL"),
                  Node(childnum=0,funcid=20399,id=20406,lineno=321,type="AST_STATIC_CALL"),
                  Node(childnum=1,funcid=20263,id=20311,lineno=284,type="AST_CALL"),
                  Node(childnum=0,funcid=20399,id=20429,lineno=323,type="AST_STATIC_CALL"),
                  Node(childnum=0,funcid=20263,id=20380,lineno=292,type="AST_STATIC_CALL"),
                  Node(childnum=0,funcid=20471,id=20571,lineno=375,type="AST_METHOD_CALL"),
                  Node(childnum=0,funcid=20218,id=20241,lineno=242,type="AST_METHOD_CALL"),
                  Node(childnum=0,funcid=20471,id=20662,lineno=396,type="AST_CALL"),
                  Node(childnum=0,funcid=20471,id=20600,lineno=384,type="AST_CALL"),
                  Node(childnum=0,funcid=20471,id=20543,lineno=369,type="AST_CALL"),
                  Node(childnum=0,funcid=20399,id=20412,lineno=321,type="AST_STATIC_CALL"),
                  Node(childnum=1,funcid=20263,id=20332,lineno=286,type="AST_STATIC_CALL"),
                  Node(childnum=1,funcid=20263,id=20287,lineno=279,type="AST_STATIC_CALL"),
                  Node(childnum=0,funcid=20145,id=20177,lineno=200,type="AST_CALL"),
                  Node(childnum=1,funcid=20471,id=20793,lineno=424,type="AST_METHOD_CALL"),
                  Node(childnum=1,funcid=20471,id=20741,lineno=413,type="AST_METHOD_CALL"),
                  Node(childnum=0,funcid=20471,id=20556,lineno=371,type="AST_STATIC_CALL"),
                  Node(childnum=0,funcid=20471,id=20615,lineno=386,type="AST_STATIC_CALL")
        ]
        self.assertEquals(result, expect)

    def testCallToAssigns(self):
        """Searches all call expressions in
        test-repos/agavi/src/core/AgaviContext.class.php and retrieves
        their enclosing assign statements (if they are enclosed in
        assign statements.)"""
        query = """g.V().getAstOfFile("AgaviContext.class.php").match{ isCallExpression(it) }
                   .callToAssigns()"""
        result = self.j.runGremlinQuery(query)
        expect = [Node(childnum=1,funcid=20471,id=20496,lineno=361,type="AST_ASSIGN"),
                  Node(childnum=0,funcid=20145,id=20153,lineno=198,type="AST_ASSIGN"),
                  Node(childnum=2,funcid=20471,id=20506,lineno=362,type="AST_ASSIGN"),
                  Node(childnum=1,funcid=20263,id=20308,lineno=284,type="AST_ASSIGN"),
                  Node(childnum=0,funcid=20263,id=20329,lineno=286,type="AST_ASSIGN"),
                  Node(childnum=0,funcid=20263,id=20284,lineno=279,type="AST_ASSIGN"),
                  Node(childnum=0,funcid=20471,id=20790,lineno=424,type="AST_ASSIGN"),
                  Node(childnum=0,funcid=20263,id=20329,lineno=286,type="AST_ASSIGN"),
                  Node(childnum=0,funcid=20471,id=20733,lineno=413,type="AST_ASSIGN"),
                  Node(childnum=0,funcid=20471,id=20550,lineno=371,type="AST_ASSIGN"),
                  Node(childnum=0,funcid=20471,id=20607,lineno=386,type="AST_ASSIGN")
        ]
        self.assertEquals(result, expect)
