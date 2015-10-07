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


/**
   For a given variable varname, find all variables that "taint" that
   variable in the current subtree, i.e., all variables that occur in
   assignments whose left side is v.

   @param varname A *closure* that returns the name of the variable
                  (instead of simply a *string* that contains the name
                  of the variable)

   Note: for some weird reason I do not fully understand yet, we
   cannot pass varname as a string, but we have to pass it as a
   closure that returns a string. This is because if I use
   .tainters(varname) below where varname is a string that was
   assigned in an earlier .sideEffect, Gremlin throws an exception and
   says it does not know varname. The workaround is to put varname
   inside a closure, and call .tainters as .tainters({varname}). Then,
   Gremlin knows what varname is. Therefore, we have to use the syntax
   varname() below instead of simply varname (i.e., we have postfix
   varname with parentheses). TODO design minimal example and write to
   the Gremlin mailing list to ask about this.
*/

/* TODO maybe now that the below works, isolate the relevant steps
Gremlin.defineStep('tainters', [Vertex,Pipe], { varname ->
  _().match{ isAssignment(it) && it.lval().varToName().next() == varname()}
  .rval().match{ it.type == TYPE_VAR }
});
*/


x = []

g.V()
// find all call expressions where the called function is called "mysql_query" / "pg_query" / "sqlite_query"
.filter{ sql_query_funcs.contains(it.code) && isCallExpression(it.nameToCall().next()) }.callexpressions()
// traverse to arguments; note that we do not know whether to traverse
// to the first or second argument, so just collect them all (1)
.callToArguments()
// match variables (argument could be a variable itself, or contain
// variables within a string concatenation or an encapsulated list)
.match{ it.type == TYPE_VAR }
// label here for looping
.as('x')
// save the variable node
.sideEffect{ var = it }
// traverse to enclosing function or file statements node
.fileOrFunctionStmts()
// match assignments whose left side is the saved variable name...
.match{ isAssignment(it) && it.lval().varToName().next() == var.varToName().next() }
// ...find the variables that occur on the right-hand side...
.rval().match{ it.type == TYPE_VAR }
// loop until nothing new is emitted, and emit all objects in each iteration
.loop('x'){ it.object != null }{ true }
// filter only the nodes contained in the attacker sources
.filter{ attacker_sources.contains(it.varToName().next()) }
// finally, when we get here, go back to the matched variable and emit a warning
.back('x')
.transform{ warning(it.id, it.type, it.toFile().fileToPath().next(), it.lineno) }


//.sideEffect{ var = it; varname = var.varToName().next(); }
//.fileOrFunctionStmts()
//.tainters{varname}
//.varToName()


/*
// OLD #3: Pretty much like OLD #2, but we use a loop with an explicit
// number of steps (i.e., we manually specify the recursion depth) The
// main problem here is that when the recursion depth is too high,
// there are no results any more. It appears that aggregating null
// objects has some unexpected side effects...

x = []

g.V()
// find all call expressions where the called function is called "mysql_query" / "pg_query" / "sqlite_query"
.filter{ sql_query_funcs.contains(it.code) && isCallExpression(it.nameToCall().next()) }.callexpressions()
// traverse to arguments; note that we do not know whether to traverse
// to the first or second argument, so just collect them all (1)
.callToArguments()
// match variables (argument could be a variable itself, or contain
// variables within a string concatenation or an encapsulated list)
.match{ it.type == TYPE_VAR }
// label here for looping
.as('x')
// save the variable node
.sideEffect{ var = it }
// traverse to enclosing function or file statements node
.fileOrFunctionStmts()
// match assignments whose left side is the saved variable name...
.match{ isAssignment(it) && it.lval().varToName().next() == var.varToName().next() }
// ...find the variables that occur on the right-hand side...
.rval().match{ it.type == TYPE_VAR }
// ...and store them in the array x
.aggregate(x)
// loop this for a fixed recursion depth of, e.g., 3
.loop('x'){ it.loops < 4 }
// scatter the array x and output the variables
.transform{ x }
.scatter()
.varToName()
 */


/*
// OLD #2: Manually repeating aggregate steps
// Here, we have to use .aggregate because otherwise something
// extremely weird happens: Without .aggregate, upon the second
// .sideEffect, some seemingly random nodes are output. I do not quite
// understand why what happens.

x = []

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
.sideEffect{ var = it }
// traverse to enclosing function or file statements node
.fileOrFunctionStmts()
// match assignments whose left side is the saved variable name...
.match{ isAssignment(it) && it.lval().varToName().next() == var.varToName().next() }
// ...find the variables that occur on the right-hand side...
.rval().match{ it.type == TYPE_VAR }
// ...and store them in the array x
.aggregate(x)

// repeat
// Note (see above): if we did not use .aggregate and simply try to
// repeat the traversal beginning with .sideEffect, the results look
// random:
.sideEffect{ var = it }
.fileOrFunctionStmts()
.match{ isAssignment(it) && it.lval().varToName().next() == var.varToName().next() }
.rval().match{ it.type == TYPE_VAR }
.aggregate(x)

// repeat
.sideEffect{ var = it }
.fileOrFunctionStmts()
.match{ isAssignment(it) && it.lval().varToName().next() == var.varToName().next() }
.rval().match{ it.type == TYPE_VAR }
.aggregate(x)

// repeat
.sideEffect{ var = it }
.fileOrFunctionStmts()
.match{ isAssignment(it) && it.lval().varToName().next() == var.varToName().next() }
.rval().match{ it.type == TYPE_VAR }
.aggregate(x)

// ...scatter the array and output everything
.transform{ x }
.scatter()
.varToName()
*/


/*
// OLD #1: Without indirections
// (i.e., $a = $_POST['foo']; mysql_query($a); will be found,
// but NOT $a = $_POST['foo']; $b = $a; mysql_query($b);)

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
*/
