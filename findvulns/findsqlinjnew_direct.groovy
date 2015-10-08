/*
  First attempt to model possible SQL injections at a purely
  syntactical level, when one of PHP's classic SQL *_query() functions
  is used to perform the query.
 */

attacker_sources = ["_GET", "_POST", "_COOKIE", "_REQUEST", "_ENV", "HTTP_ENV_VARS"]

sql_query_funcs = ["mysql_query", "pg_query", "sqlite_query"]

def warning( id, type, filename, lineno) {
  "findsqlinjnew_direct: In file " + filename + ": line " + lineno + " potentially dangerous (node id " + id + ", type " + type + ")"
}

def unexpected( id, type, filename, lineno) {
  "findsqlinjnew_direct: Unexpected first argument to SQL query call in " + filename + ", line " + lineno + " (node id " + id + ", type " + type + ")"
}

// Note: This is only for *direct* vulnerabilities such as
// mysql_query("...".$_POST['foo']) but, e.g., will not find things
// such as $a = $_POST['foo']; mysql_query($a); see
// findsqlnew_indirect.groovy for that

g.V()
// find all call expressions where the called function is called "mysql_query" / "pg_query" / "sqlite_query"
.filter{ sql_query_funcs.contains(it.code) && isCallExpression(it.nameToCall().next()) }.callexpressions()
// traverse to arguments; note that we do not know whether to traverse
// to the first or second argument, so just collect them all (1)
.callToArguments()
// match variables (argument could be a variable itself, or contain
// variables within a string concatenation or an encapsulated list)
.match{ it.type == TYPE_VAR }
// filter variables that are among the attacker sources
.filter{ attacker_sources.contains(it.varToName().next()) }
// and output a warning for those
.transform{ warning(it.id, it.type, it.toFile().fileToPath().next(), it.lineno) }
