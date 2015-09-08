from PythonJoernTests import *
from py2neo import Node

class SyntaxTests(PythonJoernTests):

    def testAstNodes(self):
        """Searches all AST nodes from the first statement in agavi's
        version.php"""
        query = """g.v(3)
                   .astNodes()"""
        result = self.j.runGremlinQuery(query)
        expect = [Node(childnum=2,index=7,lineno=30,type="AST_ARG_LIST"),
                  Node(childnum=1,code="set",index=6,lineno=30,type="string"),
                  Node(childnum=0,flags=["NAME_NOT_FQ"],index=4,lineno=30,type="AST_NAME"),
                  Node(childnum=1,code="Agavi",index=9,lineno=30,type="string"),
                  Node(childnum=0,code="agavi.name",index=8,lineno=30,type="string"),
                  Node(childnum=0,code="AgaviConfig",index=5,lineno=30,type="string"),
                  Node(childnum=0,index=3,lineno=30,type="AST_STATIC_CALL")
              ]
        self.assertEquals(result, expect)
        
    def testParents(self):
        """Searches for all parent nodes of function declarations."""
        query = """g.V(NODE_TYPE,TYPE_FUNC_DECL)
                   .parents()"""
        result = self.j.runGremlinQuery(query)
        expect = [Node(childnum=0,index=68677,lineno=1,type="AST_STMT_LIST"),
                  Node(childnum=0,index=68677,lineno=1,type="AST_STMT_LIST"),
                  Node(childnum=0,index=68677,lineno=1,type="AST_STMT_LIST"),
                  Node(childnum=0,index=68677,lineno=1,type="AST_STMT_LIST"),
                  Node(childnum=0,index=68677,lineno=1,type="AST_STMT_LIST"),
                  Node(childnum=0,index=68677,lineno=1,type="AST_STMT_LIST"),
                  Node(childnum=0,index=68677,lineno=1,type="AST_STMT_LIST"),
                  Node(childnum=0,index=68677,lineno=1,type="AST_STMT_LIST"),
                  Node(childnum=0,index=68677,lineno=1,type="AST_STMT_LIST"),
                  Node(childnum=0,index=486806,lineno=1,type="AST_STMT_LIST")
              ]
        self.assertEquals(result, expect)

    def testChildren(self):
        """Searches for all children nodes of the root node of agavi's version.php"""
        query = """g.V(NODE_TYPE,TYPE_FILE).has(NODE_NAME,"version.php").out(FILE_EDGE)
                   .children()"""
        result = self.j.runGremlinQuery(query)
        expect = [Node(childnum=10,index=143,lineno=1,type="NULL"),
                  Node(childnum=9,index=120,lineno=54,type="AST_STATIC_CALL"),
                  Node(childnum=8,index=113,lineno=52,type="AST_STATIC_CALL"),
                  Node(childnum=7,index=92,lineno=47,type="AST_STATIC_CALL"),
                  Node(childnum=6,index=45,lineno=38,type="AST_STATIC_CALL"),
                  Node(childnum=5,index=38,lineno=36,type="AST_STATIC_CALL"),
                  Node(childnum=4,index=31,lineno=35,type="AST_STATIC_CALL"),
                  Node(childnum=3,index=24,lineno=34,type="AST_STATIC_CALL"),
                  Node(childnum=2,index=17,lineno=33,type="AST_STATIC_CALL"),
                  Node(childnum=1,index=10,lineno=32,type="AST_STATIC_CALL"),
                  Node(childnum=0,index=3,lineno=30,type="AST_STATIC_CALL")
              ]
        self.assertEquals(result, expect)

    def testIthChildren(self):
        """Searches for all third children of all function nodes. The third
        children are the statement lists."""
        query = """g.V(NODE_TYPE,TYPE_FUNC_DECL)
                   .ithChildren(2)"""
        result = self.j.runGremlinQuery(query)
        expect = [Node(childnum=2,index=68936,lineno=76,type="AST_STMT_LIST"),
                  Node(childnum=2,index=69092,lineno=90,type="AST_STMT_LIST"),
                  Node(childnum=2,index=69120,lineno=96,type="AST_STMT_LIST"),
                  Node(childnum=2,index=69172,lineno=103,type="AST_STMT_LIST"),
                  Node(childnum=2,index=69202,lineno=108,type="AST_STMT_LIST"),
                  Node(childnum=2,index=69248,lineno=116,type="AST_STMT_LIST"),
                  Node(childnum=2,index=69278,lineno=121,type="AST_STMT_LIST"),
                  Node(childnum=2,index=69341,lineno=129,type="AST_STMT_LIST"),
                  Node(childnum=2,index=69413,lineno=137,type="AST_STMT_LIST"),
                  Node(childnum=2,index=487518,lineno=174,type="AST_STMT_LIST")
              ]
        self.assertEquals(result, expect)

    def testStatements(self):
        """For all AST nodes from the first statement in agavi's version.php,
        searches the enclosing statement, which should thus be the
        first statement again in all cases."""
        query = """g.v(3).astNodes()
                   .statements()"""
        result = self.j.runGremlinQuery(query)
        expect = [Node(childnum=0,index=3,lineno=30,type="AST_STATIC_CALL"),
                  Node(childnum=0,index=3,lineno=30,type="AST_STATIC_CALL"),
                  Node(childnum=0,index=3,lineno=30,type="AST_STATIC_CALL"),
                  Node(childnum=0,index=3,lineno=30,type="AST_STATIC_CALL"),
                  Node(childnum=0,index=3,lineno=30,type="AST_STATIC_CALL"),
                  Node(childnum=0,index=3,lineno=30,type="AST_STATIC_CALL"),
                  Node(childnum=0,index=3,lineno=30,type="AST_STATIC_CALL")
              ]
        self.assertEquals(result, expect)

    def testNumChildren(self):
        """Queries the number of children of the first statement in agavi's
        version.php"""
        query = """g.v(3)
                   .numChildren()"""
        result = self.j.runGremlinQuery(query)
        expect = [3]
        self.assertEquals(result, expect)

