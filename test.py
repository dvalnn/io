import pulp

#PARAMETERS
P = [1,8,10,23,5] #Profit per unit of the products
C = [100,50,80] #Capacity of the factories

#Hours of production of the products in each factory
H = [[2,7,5],
    [9,4,7],
    [6,3,4],
    [2,9,3],
    [5,1,7]]

#SETS
Prod = range(0,len(P)) #set of products
Fact = range(0,len(C)) #set of factories

#DECISION VARIABLES
x = pulp.LpVariable.dicts('x',[(i,j) for i in Prod for j in Fact],cat=pulp.LpInteger,lowBound=0)
y = pulp.LpVariable.dicts('y',Fact,cat=pulp.LpBinary)

#CREATE MODEL
model = pulp.LpProblem('production', pulp.LpMaximize)

#OBJECTIVE FUNCTION
model += sum(P[i]*x[(i,j)] for i in Prod for j in Fact)

#CONSTRAINTS
model += sum(H[i][j]*x[(i,j)] for i in Prod for j in Fact) <= 200, 'TotalLimit'

for j in Fact:
    model += sum(H[i][j]*x[(i,j)] for i in Prod) <= C[j]*y[j],'CapacityLimit_{}'.format(j)

model += sum(y[j] for j in Fact) <= 2, 'MaxFactories'

# SOLVE
status=model.solve()

if status==pulp.LpStatusOptimal:
    print (model.objective.value()) #prints optimal OF value
    for i in Prod:
        for j in Fact:
            print(x[(i,j)],x[(i,j)].varValue) #prints the name of variable x and its optimal value
    for j in Fact:
        print(y[j],y[j].varValue) #prints the name of variable x and its optimal value

    model.writeLP('testlp') #creates LP file for the model
