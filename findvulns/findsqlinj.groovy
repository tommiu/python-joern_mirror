/*
  First attempt to model possible SQL injections at a purely
  syntactical level, when one of PHP's classic SQL *_query() functions
  is used to perform the query.
 */

sql_query_funcs = ["mysql_query", "pg_query", "sqlite_query"]

g.V().getAllASTRoots()
// find all call expressions where the called function is called "mysql_query" / "pg_query" / "sqlite_query"
.match{ sql_query_funcs.contains(it.code) && isCallExpression(it.nameToCall().next()) }.callexpressions()
// save the variable names of the first arguments to these call expressions for later
.sideEffect{ queryvar = it.ithArguments(0).varToName().next() }
// traverse to enclosing function declarations
.functions()
// find all assignments within the function bodies whose left side is the saved variable name
// and which are either concatenation assignments or whose right side is either
// a string concatenation or a string containing variables... for details see (1) below
.match{
  isAssignment(it) &&
  it.lval().varToName().next() == queryvar &&
  ((it.type == TYPE_ASSIGN_OP && it.flags.contains(FLAG_ASSIGN_CONCAT)) ||
   (it.rval().next().type == TYPE_BINARY_OP && it.rval().next().flags.contains(FLAG_BINARY_CONCAT)) ||
   (it.rval().next().type == TYPE_ENCAPS_LIST)
  )
 }
// save the line numbers for inspection
.sideEffect{ lineno = it.lineno }
// traverse back to the potentially vulnerable functions
.functions()//.dedup()
// finally, give a nice human-readable output
.transform{ "In file " + it.toFile().fileToPath().next() + ", function " + it.name + "(): line " + lineno + " potentially dangerous"}


/*

(1) There are different possibilities how a string concatenation can happen:

o $query = 'SELECT ... ' . $userinput . ' ORDER BY ...';
=> assignment of type AST_ASSIGN where left side is the saved variable and right side is of type AST_BINARY_OP (flag = BINARY_CONCAT)

o $query .= $userinput;
=> assignment of type AST_ASSIGN_OP (flag = ASSIGN_CONCAT) where left side is the saved variable

o $query .= 'SELECT ... ' . $userinput . ' ORDER BY ...';
=> same same, just to illustrate right side could be different things

o $query = "SELECT ... {$userinput} ORDER BY ...";
=> assignment of type AST_ASSIGN where left side is the saved variable and right side is of type AST_ENCAPS_LIST

Summing up, we want to look for:
 Assignments where left side is saved variable and
 o of type AST_ASSIGN and right side either AST_BINARY_OP or AST_ENCAPS_LIST; or
 o of type AST_ASSIGN_OP and right side is whatever


TODO:
=====
- what other ways to do SQL queries?
-> have a look at mysqli...
-> think of more ways
- what about a call where a concatenation happens within the argument, e.g.,
  mysql_query("SELECT ...".$userinput."...");

 */


