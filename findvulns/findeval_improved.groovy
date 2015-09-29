/*
  Improved attempt to model possibly dangerous eval statements. Only
  consider $_POST, $_GET, $_COOKIE and $_REQUEST sources.
 */

attacker_sources = ["_GET", "_POST", "_COOKIE", "_REQUEST"]

def warning( id, type, filename, lineno) {
  "findeval: In file " + filename + ": line " + lineno + " potentially dangerous (node id " + id + ", type " + type + ")"
}

g.V()
// find all eval expressions... or include, why not
//.filter{ it.type == TYPE_INCLUDE_OR_EVAL && it.flags.contains(FLAG_EXEC_EVAL) }
.filter{ it.type == TYPE_INCLUDE_OR_EVAL }
// traverse to child
.ithChildren(0)
// match variables (argument could be a variable itself, or contain
// variables within a string concatenation or an encapsulated list)
.match{ it.type == TYPE_VAR }
// save the variable node
.sideEffect{ var = it }
// is one of these variables already among the attacker sources?
.ifThenElse{ attacker_sources.contains(var.varToName().next()) }{
   // if yes, warning
   it.transform{ warning(it.id, it.type, it.toFile().fileToPath().next(), it.lineno) }
 }
 {
   // if not, traverse to enclosing function or file statements node...
   it.fileOrFunctionStmts()
   // ..and find assignments whose left side is the saved variable name...
   .match{ it.type == TYPE_ASSIGN && it.lval().varToName().next() == var.varToName().next() }
   // ...and whose right side contains one of the attacker sources
   .rval().match{ it.type == TYPE_VAR && attacker_sources.contains(it.varToName().next()) }
   // for the results, output a warning
   .transform{ warning(var.id, var.type, var.toFile().fileToPath().next(), var.lineno) }
 }
