/**
   Helper traversals for finding files and directory nodes.
 */

/**
   Given a file name, filter from the current set of vertices the
   vertices that are file nodes and have the given name, and traverse
   the corresponding root of the AST.

   This traversal is meant as a starting point when analysing a
   particular file, to be used as, e.g.,

   g.V().getAstOfFile("index.php")

   Note: If several files nodes have the same name, this may return
   more than one node.
 */
Gremlin.defineStep('getAstOfFile', [Vertex, Pipe], { filename ->
  _().has(NODE_TYPE,TYPE_FILE).has(NODE_NAME,filename).out(FILE_EDGE)
})


/**
   Given a set of vertices, traverse to the enclosing file nodes.
 */
Gremlin.defineStep('toFile', [Vertex, Pipe], {
  _().in.loop(1){ it.object.type != TYPE_FILE }
})


/**
   Given a set of file nodes, return their paths.
 */
Gremlin.defineStep('fileToPath', [Vertex, Pipe], {
  _().filter{ it.type == TYPE_FILE }.sideEffect{ path = it.name }
  .in(DIRECTORY_EDGE).sideEffect{ path = it.name + "/" + path }.loop(2){it.object.index != 0}
  .transform{ path }
})

