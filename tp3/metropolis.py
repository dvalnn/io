from os import stat
import pulp

# dados
C = [
    [0, 1, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 1],
    [0, 1, 0, 0, 0, 1, 1],
    [0, 1, 1, 0, 1, 1, 0],
    [1, 0, 1, 0, 1, 0, 0],
    [1, 0, 0, 1, 0, 1, 0],
    [1, 0, 0, 0, 0, 0, 1],
    [0, 0, 1, 1, 1, 0, 0],
    [1, 0, 0, 0, 1, 0, 0],
]
loc = range(1, len(C[0]) + 1)
zones = range(len(C))

# var de decisão
l = pulp.LpVariable.dicts("l", [i for i in loc], cat=pulp.LpBinary)

# modelo
model = pulp.LpProblem("Escolha_de_locais", pulp.LpMinimize)

# objective func
model += sum(l[i] for i in loc)

# restrain
for zone in zones:
    model += sum(C[zone][i - 1] * l[i] for i in loc) >= 1

status = model.solve()

if status == pulp.LpStatusOptimal:
    print(model.objective.value())
    for i in loc:
        print(l[i], l[i].varValue)
    model.writeLP("metropolisLP")
