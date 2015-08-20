Object.metaClass.NODE_INDEX = 'index'

// Node Keys

Object.metaClass.NODE_TYPE = 'type'
Object.metaClass.NODE_FLAGS = 'flags'
Object.metaClass.NODE_LINENO = 'lineno'
Object.metaClass.NODE_CODE = 'code'
Object.metaClass.NODE_ENDLINENO = 'endlineno'
Object.metaClass.NODE_NAME = 'name'
Object.metaClass.NODE_DOCCOMMENT = 'doccomment'

// Node Values

Object.metaClass.TYPE_STMT_LIST = 'AST_STMT_LIST' // ...; ...; ...;
Object.metaClass.TYPE_CALL = 'AST_CALL' // foo()
Object.metaClass.TYPE_STATIC_CALL = 'AST_STATIC_CALL' // bla::foo()
Object.metaClass.TYPE_METHOD_CALL = 'AST_METHOD_CALL' // $bla->foo()
Object.metaClass.TYPE_FUNC_DECL = 'AST_FUNC_DECL' // function foo() {}
Object.metaClass.TYPE_METHOD = 'AST_METHOD' // class bla { ... function foo() {} ... }
Object.metaClass.TYPE_ARG_LIST = 'AST_ARG_LIST' // foo( a1, a2, a3)
Object.metaClass.TYPE_PARAM_LIST = 'AST_PARAM_LIST' // function foo( p1, p2, p3) {}
Object.metaClass.TYPE_ASSIGN = 'AST_ASSIGN' // $buzz = true
// TODO and many more...

Object.metaClass.TYPE_DIRECTORY = 'Directory'
Object.metaClass.TYPE_FILE = 'File'

// Edge types

Object.metaClass.DIRECTORY_EDGE = 'DIRECTORY_OF'
Object.metaClass.FILE_EDGE = 'FILE_OF'
Object.metaClass.AST_EDGE = 'PARENT_OF'

