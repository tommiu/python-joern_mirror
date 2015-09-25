/*
  First attempt to model possible SQL injections at a purely
  syntactical level, when one of PHP's classic SQL *_query() functions
  is used to perform the query.
 */

sql_query_funcs = ["mysql_query", "pg_query", "sqlite_query"]

// do not consider arguments to SQL query functions of the following types:
// (fixed) strings, as well as AST_CALL, AST_METHOD_CALL, and AST_PROP for now
argument_type_filter = [TYPE_STRING, TYPE_CALL, TYPE_METHOD_CALL, TYPE_PROP]

def warning( id, type, filename, lineno) {
  "findsqlinj: In file " + filename + ": line " + lineno + " potentially dangerous (node id " + id + ", type " + type + ")"
}

def unexpected( id, type, filename, lineno) {
  "findsqlinj: Unexpected first argument to SQL query call in " + filename + ", line " + lineno + " (node id " + id + ", type " + type + ")"
}

g.V()
// find all call expressions where the called function is called "mysql_query" / "pg_query" / "sqlite_query"
.filter{ sql_query_funcs.contains(it.code) && isCallExpression(it.nameToCall().next()) }.callexpressions()
// traverse to arguments; note that we do not know whether to traverse
// to the first or second argument, so just collect them all (1)
.callToArguments()
// filter all argument types that we do not want to consider
.filter{ !argument_type_filter.contains(it.type) }
// is the argument itself already a string concatenation or a string that contains variables?
.ifThenElse{ (it.type == TYPE_BINARY_OP && it.flags.contains(FLAG_BINARY_CONCAT)) || it.type == TYPE_ENCAPS_LIST } {
  // if yes, output a warning, no questions asked
  it.transform{ warning(it.id, it.type, it.toFile().fileToPath().next(), it.lineno) }
 }
 // otherwise, is it a variable?
 {
   it.ifThenElse{ it.type == TYPE_VAR } {
     // if yes, save the argument and the variable name for later
     it.as('arg')
     .sideEffect{ queryvar = it.varToName().next() }
     // traverse to enclosing function or file statements node
     .fileOrFunctionStmts()
     // find all assignments within the function/file body whose left side is the saved variable name
     // and which is either a concatenation assignment or whose right side is either
     // a string concatenation or a string containing variables... for details see (2) below
     .match{
       isAssignment(it) &&
       it.lval().varToName().next() == queryvar &&
       ((it.type == TYPE_ASSIGN_OP && it.flags.contains(FLAG_ASSIGN_CONCAT)) ||
	(it.rval().next().type == TYPE_BINARY_OP && it.rval().next().flags.contains(FLAG_BINARY_CONCAT)) ||
	(it.rval().next().type == TYPE_ENCAPS_LIST)
       )
     }
     // finally, give a nice human-readable output
     .back('arg')
     .transform{ warning(it.id, it.type, it.toFile().fileToPath().next(), it.lineno) }
   }
   // otherwise, we encountered a first argument of a type we did not expect --
   // have a closer look!
   {
     it.transform{ unexpected(it.id, it.type, it.toFile().fileToPath().next(), it.lineno) }
   }
 }

/*

(1) PHP being super-awesome, there is no consistency whatsoever
concerning the order of the argument to the *_query() calls. The
synopses are:

* mysql_query ( string $query [, resource $link_identifier = NULL ] )

* pg_query ([ resource $connection ], string $query )

* sqlite_query ( resource $dbhandle , string $query [, int $result_type = SQLITE_BOTH [, string &$error_msg ]] )

* sqlite_query ( string $query , resource $dbhandle [, int $result_type = SQLITE_BOTH [, string &$error_msg ]] )

So, basically, we do not always know for sure whether to traverse to
the first or the second argument. In particular since types are only
known at runtime. Thus, the easiest solution is to simply traverse to
all arguments...


(2) There are different possibilities how a string concatenation can happen:

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
-> the PDO abstraction thing...
-> think of more ways

- there's probably a rather small bug in the above script that may
lead to some false positives.  this is due to the fact that PHP has
top-level code, and SQL queries can also be executed within top-level
code instead of functions (in fact, in practice this appears to happen
rather often.) However, using .astNodes (implicitly, by using .match)
on top-level code will also match code inside functions declared
within that top-level code. For instance, consider:

function foo() {
  $query = "select ".$input."...";
  $result = mysql_query($query);
}
$query = "secure, fixed string query";
$result = mysql_query($query);

The query within foo() is vulnerable, but the query on the top-level
is not. However, our traversal will consider the top-level query
dangerous also, as it will see that a variable is used which
presumably was the result of an earlier string concatenation; it
actually wasn't, of course, but the traversal will not see that, as it
does not know about local scopes and simply notices (using .match)
that the variable $query used in the mysql_query call on the top-level
was once the result of a string concatenation.

It's probably not that big a deal. There will always be some false
negatives. But it's interesting to realize this.


- .functions() verbessern! Es filtert nodes, die nicht innerhalb einer
Funktion sind. Vielleicht in .functions() alternativ nach it.type ==
File gucken oder wohl viel viel besser: Funktionen schreiben, die
feststellen koennen, ob Code top-level oder innerhalb einer Funktion
ist und dann entsprechend reagieren. functions() muss insofern nicht
verbessert werden, es sollte aber nur dann benutzt werden, wenn sich
Code innerhalb einer Funktion befindet.

ODER vielleicht ist es auch besser, den AST leicht umzubauen: schon
beim generieren der CSV-Dateien koennten wir beim anlegen einer file
node direkt darunter eine kuenstliche AST_FUNC_DECL node anlegen, die
z.B. ___MAIN___ heisst. dann haette man in den traversals nicht das
problem, zwischen top-level und function code unterscheiden zu
muessen... am Montag mal Fabian fragen; er muss sich mit der Thematik
ja beschaeftigt haben, wenn er CFG edges "pro Funktion" anlegt...


 */


