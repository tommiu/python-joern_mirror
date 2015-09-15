import os
from joern.all import JoernSteps

j = JoernSteps()
j.connectToDatabase()

command = file(os.path.join(os.path.dirname(__file__), "findsqlinj.groovy")).read() + "\n"

res = j.runGremlinQuery( command)

#print res

for r in res: print r

