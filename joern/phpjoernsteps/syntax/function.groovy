/**
   (Optimized) Match-traversals for function declarations.
*/

/**
   Traverse to function/method declarations enclosing supplied AST
   nodes. This may be the node itself.
*/
Gremlin.defineStep('functions', [Vertex, Pipe], {
  _().ifThenElse{ isFunction(it) }
  { it }
  { it.parents().loop(1){ !isFunction(it.object) } }
});

// checks whether a given node represents a function/method declaration
Object.metaClass.isFunction = { it ->
  it.type == TYPE_FUNC_DECL ||
  it.type == TYPE_METHOD
  // TODO what about closures?
}
