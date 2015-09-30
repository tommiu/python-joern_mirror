/*
  First attempt to model possible SQL injections at a purely
  syntactical level, when one of PHP's classic SQL *_query() functions
  is used to perform the query.
 */

attacker_sources = ["_GET", "_POST", "_COOKIE", "_REQUEST", "_ENV", "HTTP_ENV_VARS"]

sql_query_funcs = ["mysql_query", "pg_query", "sqlite_query"]

def warning( id, type, filename, lineno) {
  "findsqlinj_improved: In file " + filename + ": line " + lineno + " potentially dangerous (node id " + id + ", type " + type + ")"
}

def unexpected( id, type, filename, lineno) {
  "findsqlinj_improved: Unexpected first argument to SQL query call in " + filename + ", line " + lineno + " (node id " + id + ", type " + type + ")"
}

g.V()
// find all call expressions where the called function is called "mysql_query" / "pg_query" / "sqlite_query"
.filter{ sql_query_funcs.contains(it.code) && isCallExpression(it.nameToCall().next()) }.callexpressions()
// traverse to arguments; note that we do not know whether to traverse
// to the first or second argument, so just collect them all (1)
.callToArguments()
// match variables (argument could be a variable itself, or contain
// variables within a string concatenation or an encapsulated list)
.match{ it.type == TYPE_VAR }
// save the variable node
.sideEffect{ var = it; varname = var.varToName().next(); }
// is one of these variables already among the attacker sources?
.ifThenElse{ attacker_sources.contains(varname) }{
   // if yes, warning
   it.transform{ warning(it.id, it.type, it.toFile().fileToPath().next(), it.lineno) }
 }
 {
   // if not, traverse to enclosing function or file statements node...
   it.fileOrFunctionStmts()
   // ..and find assignments whose left side is the saved variable name...
   .match{ isAssignment(it) && it.lval().varToName().next() == varname }
   // ...and whose right side contains one of the attacker sources
   .rval().match{ it.type == TYPE_VAR && attacker_sources.contains(it.varToName().next()) }
   // for the results, output a warning
   .transform{ warning(var.id, var.type, var.toFile().fileToPath().next(), var.lineno) }
 }
