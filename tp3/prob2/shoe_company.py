import pulp
import header

# SPENCER SHOE COMPANY

# DADOS
cdist = header.readMatrixFromFile("cdist.txt")
proc = header.readArrayFromFile("proc.txt")
cap = header.readArrayFromFile("cap.txt")
cprod = header.readArrayFromFile("cprod.txt")
cfix = header.readArrayFromFile("cfix.txt")

# CONJUNTOS
Fab = range(len(cap))  # fabricas
Cent = range(len(proc))  # centros distribuicao

# VARIAVEIS DE DECISAO
x = pulp.LpVariable.dicts("x", [(i, j) for i in Fab for j in Cent], cat=pulp.LpContinuous, lowBound=0)
y = pulp.LpVariable.dicts("y", Fab, cat=pulp.LpBinary)

# CRIAR MODELO
modelo = pulp.LpProblem("Spencer", pulp.LpMinimize)

# FUNCAO OBJETIVO
modelo += (
    sum(cprod[i] * x[(i, j)] for i in Fab for j in Cent)
    + sum(cdist[i][j] * x[(i, j)] for i in Fab for j in Cent)
    + sum(cfix[i] * y[i] for i in Fab)
)

# RESTRICOES
for i in Fab:
    modelo += sum(x[(i, j)] for j in Cent) <= cap[i] * y[i], "Capacidade_{}".format(i)

for j in Cent:
    modelo += sum(x[(i, j)] for i in Fab) >= proc[j], "Procura_{}".format(j)

modelo += y[0] == 1, "Pontiac"  # para a alinea 2, retirar esta restricao

# RESOLVER
status = modelo.solve()

if status == pulp.LpStatusOptimal:

    for i in Fab:
        print(y[i], y[i].varValue)
        for j in Cent:
            print(x[(i, j)], x[(i, j)].varValue)

    print("Valor otimo:", modelo.objective.value())
