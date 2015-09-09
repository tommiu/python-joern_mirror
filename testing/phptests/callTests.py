from PythonJoernTests import *
from py2neo import Node

class CallTests(PythonJoernTests):

    def testCallToArguments(self):
        """Searches all call expressions in test-repos/agavi/src/core/AgaviContext.class.php
        and retrieves their arguments"""
        query = """g.V("type","File").has("name","AgaviContext.class.php").out(FILE_EDGE).match{ isCallExpression(it) }
                   .callToArguments()"""
        result = self.j.runGremlinQuery(query)
        expect = [Node(childnum=0,index=20443,lineno=326,type="AST_ARRAY"),
                  Node(childnum=1,index=20200,lineno=204,type="AST_DIM"),
                  Node(childnum=0,index=20198,lineno=204,type="AST_VAR"),
                  Node(childnum=1,index=20063,lineno=120,type="AST_CONST"),
                  Node(childnum=0,code="Cloning an AgaviContext instance is not allowed.",index=20062,lineno=120,type="string"),
                  Node(childnum=0,index=20504,lineno=361,type="AST_VAR"),
                  Node(childnum=0,index=20161,lineno=198,type="AST_VAR"),
                  Node(childnum=0,index=20806,lineno=428,type="AST_ARRAY"),
                  Node(childnum=0,code="AgaviISingletonModel",index=20685,lineno=403,type="string"),
                  Node(childnum=2,index=20516,lineno=362,type="AST_VAR"),
                  Node(childnum=1,code="_",index=20515,lineno=362,type="string"),
                  Node(childnum=0,code="/",index=20514,lineno=362,type="string"),
                  Node(childnum=1,flags=["TYPE_ARRAY"],index=20822,lineno=430,type="AST_CAST"),
                  Node(childnum=0,index=20820,lineno=430,type="AST_VAR"),
                  Node(childnum=0,index=20654,lineno=394,type="AST_VAR"),
                  Node(childnum=0,index=20641,lineno=390,type="AST_VAR"),
                  Node(childnum=1,index=20419,lineno=321,type="AST_PROP"),
                  Node(childnum=0,flags=["BINARY_CONCAT"],index=20411,lineno=321,type="AST_BINARY_OP"),
                  Node(childnum=0,index=20315,lineno=284,type="AST_VAR"),
                  Node(childnum=1,index=20436,lineno=323,type="AST_VAR"),
                  Node(childnum=0,index=20434,lineno=323,type="AST_VAR"),
                  Node(childnum=0,index=20385,lineno=292,type="AST_VAR"),
                  Node(childnum=0,index=20578,lineno=375,type="AST_VAR"),
                  Node(childnum=0,index=20248,lineno=242,type="AST_VAR"),
                  Node(childnum=1,index=20667,lineno=396,type="AST_VAR"),
                  Node(childnum=0,code="Couldn't find class for Model %s",index=20666,lineno=396,type="string"),
                  Node(childnum=0,index=20604,lineno=384,type="AST_VAR"),
                  Node(childnum=0,index=20547,lineno=369,type="AST_VAR"),
                  Node(childnum=0,code="core.config_dir",index=20417,lineno=321,type="string"),
                  Node(childnum=1,index=20338,lineno=286,type="AST_CALL"),
                  Node(childnum=0,code="core.context_implementation",index=20337,lineno=286,type="string"),
                  Node(childnum=0,code="core.default_context",index=20292,lineno=279,type="string"),
                  Node(childnum=1,index=20182,lineno=200,type="AST_VAR"),
                  Node(childnum=0,code="No factory info for \"%s\"",index=20181,lineno=200,type="string"),
                  Node(childnum=0,index=20798,lineno=424,type="AST_VAR"),
                  Node(childnum=0,index=20746,lineno=413,type="AST_VAR"),
                  Node(childnum=0,code="core.model_dir",index=20561,lineno=371,type="string"),
                  Node(childnum=0,code="core.module_dir",index=20620,lineno=386,type="string")
              ]
        self.assertEquals(result, expect)

    def testIthArguments(self):
        """Searches all call expressions in
        test-repos/agavi/src/core/AgaviContext.class.php and retrieves
        their third argument."""
        query = """g.V("type","File").has("name","AgaviContext.class.php").out(FILE_EDGE).match{ isCallExpression(it) }
                   .ithArguments(2)"""
        result = self.j.runGremlinQuery(query)
        expect = [Node(childnum=2,index=20516,lineno=362,type="AST_VAR")]
        self.assertEquals(result, expect)

    def testArgToCall(self):
        """Searches all call expressions in
        test-repos/agavi/src/core/AgaviContext.class.php, retrieves
        their arguments, traverses back to the call expressions and
        deduplicates. The result is the set of all call expressions
        that have at least one argument."""
        query = """g.V("type","File").has("name","AgaviContext.class.php").out(FILE_EDGE).match{ isCallExpression(it) }.callToArguments()
                   .argToCall().dedup()"""
        result = self.j.runGremlinQuery(query)
        expect = [Node(childnum=1,index=20439,lineno=326,type="AST_CALL"),
                  Node(childnum=3,index=20193,lineno=204,type="AST_METHOD_CALL"),
                  Node(childnum=0,index=20058,lineno=120,type="AST_CALL"),
                  Node(childnum=1,index=20499,lineno=361,type="AST_STATIC_CALL"),
                  Node(childnum=1,index=20156,lineno=198,type="AST_METHOD_CALL"),
                  Node(childnum=0,index=20802,lineno=428,type="AST_CALL"),
                  Node(childnum=0,index=20680,lineno=403,type="AST_METHOD_CALL"),
                  Node(childnum=0,index=20510,lineno=362,type="AST_CALL"),
                  Node(childnum=0,index=20815,lineno=430,type="AST_METHOD_CALL"),
                  Node(childnum=0,index=20650,lineno=394,type="AST_CALL"),
                  Node(childnum=1,index=20637,lineno=390,type="AST_CALL"),
                  Node(childnum=0,index=20406,lineno=321,type="AST_STATIC_CALL"),
                  Node(childnum=1,index=20311,lineno=284,type="AST_CALL"),
                  Node(childnum=0,index=20429,lineno=323,type="AST_STATIC_CALL"),
                  Node(childnum=0,index=20380,lineno=292,type="AST_STATIC_CALL"),
                  Node(childnum=0,index=20571,lineno=375,type="AST_METHOD_CALL"),
                  Node(childnum=0,index=20241,lineno=242,type="AST_METHOD_CALL"),
                  Node(childnum=0,index=20662,lineno=396,type="AST_CALL"),
                  Node(childnum=0,index=20600,lineno=384,type="AST_CALL"),
                  Node(childnum=0,index=20543,lineno=369,type="AST_CALL"),
                  Node(childnum=0,index=20412,lineno=321,type="AST_STATIC_CALL"),
                  Node(childnum=1,index=20332,lineno=286,type="AST_STATIC_CALL"),
                  Node(childnum=1,index=20287,lineno=279,type="AST_STATIC_CALL"),
                  Node(childnum=0,index=20177,lineno=200,type="AST_CALL"),
                  Node(childnum=1,index=20793,lineno=424,type="AST_METHOD_CALL"),
                  Node(childnum=1,index=20741,lineno=413,type="AST_METHOD_CALL"),
                  Node(childnum=0,index=20556,lineno=371,type="AST_STATIC_CALL"),
                  Node(childnum=0,index=20615,lineno=386,type="AST_STATIC_CALL")
              ]
        self.assertEquals(result, expect)

    def testCallToAssigns(self):
        """Searches all call expressions in
        test-repos/agavi/src/core/AgaviContext.class.php and retrieves
        their enclosing assign statements (if they are enclosed in
        assign statements.)"""
        query = """g.V("type","File").has("name","AgaviContext.class.php").out(FILE_EDGE).match{ isCallExpression(it) }
                   .callToAssigns()"""
        result = self.j.runGremlinQuery(query)
        expect = [Node(childnum=1,index=20496,lineno=361,type="AST_ASSIGN"),
                  Node(childnum=0,index=20153,lineno=198,type="AST_ASSIGN"),
                  Node(childnum=2,index=20506,lineno=362,type="AST_ASSIGN"),
                  Node(childnum=1,index=20308,lineno=284,type="AST_ASSIGN"),
                  Node(childnum=0,index=20329,lineno=286,type="AST_ASSIGN"),
                  Node(childnum=0,index=20284,lineno=279,type="AST_ASSIGN"),
                  Node(childnum=0,index=20790,lineno=424,type="AST_ASSIGN"),
                  Node(childnum=0,index=20329,lineno=286,type="AST_ASSIGN"),
                  Node(childnum=0,index=20733,lineno=413,type="AST_ASSIGN"),
                  Node(childnum=0,index=20550,lineno=371,type="AST_ASSIGN"),
                  Node(childnum=0,index=20607,lineno=386,type="AST_ASSIGN")
              ]
        self.assertEquals(result, expect)
