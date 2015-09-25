/*
  Model possibly dangerous eval statements.
 */

def warning( id, type, filename, lineno) {
  "findeval: In file " + filename + ": line " + lineno + " potentially dangerous (node id " + id + ", type " + type + ")"
}

g.V()
// find all eval expressions
.filter{ it.type == TYPE_INCLUDE_OR_EVAL && it.flags.contains(FLAG_EXEC_EVAL) }
// traverse to child
.ithChildren(0)
// filter all expressions that are not fixed strings
.filter{ it.type != TYPE_STRING }
// finally, give a nice human-readable output
.transform{ warning(it.id, it.type, it.toFile().fileToPath().next(), it.lineno) }
