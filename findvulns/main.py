import os
from joern.all import JoernSteps

j = JoernSteps()
j.connectToDatabase()

#command = file(os.path.join(os.path.dirname(__file__), "findsqlinj.groovy")).read() + "\n"
#command = file(os.path.join(os.path.dirname(__file__), "findeval.groovy")).read() + "\n"
#command = file(os.path.join(os.path.dirname(__file__), "findinclude.groovy")).read() + "\n"
#command = file(os.path.join(os.path.dirname(__file__), "findeval_improved.groovy")).read() + "\n"
#command = file(os.path.join(os.path.dirname(__file__), "findsqlinj_improved.groovy")).read() + "\n"
command = file(os.path.join(os.path.dirname(__file__), "findsqlinjnew_indirect.groovy")).read() + "\n"
#command = file(os.path.join(os.path.dirname(__file__), "findsqlinjnew_direct.groovy")).read() + "\n"

res = j.runGremlinQuery( command)

#print res

for r in res: print r

