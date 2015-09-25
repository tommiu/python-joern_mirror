/*
  Model possibly dangerous include / require statements.
 */

def warning( id, type, filename, lineno) {
  "findinclude: In file " + filename + ": line " + lineno + " potentially dangerous (node id " + id + ", type " + type + ")"
}

g.V()
// find all include or require expressions
.filter{ it.type == TYPE_INCLUDE_OR_EVAL && !it.flags.contains(FLAG_EXEC_EVAL) }
// traverse to child
.ithChildren(0)
// is the expression a string?
.ifThenElse{ it.type == TYPE_STRING } {
  // if yes, warn if it's an external URL (yep, that's possible in PHP)
  it.filter{ it.code.toLowerCase().startsWith("http") }
  .transform{ warning(it.id, it.type, it.toFile().fileToPath().next(), it.lineno) }
 }
 // otherwise, output a warning
 {
   it.transform{ warning(it.id, it.type, it.toFile().fileToPath().next(), it.lineno) }
 }
