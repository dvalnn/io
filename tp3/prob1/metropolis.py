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

# restrains
for zone in zones:
    model += sum(C[zone][i - 1] * l[i] for i in loc) >= 1, f"Zone_{zone+1} must be covered"

model += l[1] + l[3] + l[4] >= 2, "extra 1"
model += l[5] + l[6] + l[7] == 2, "extra 2"
model += l[3] + l[4] <= 1, "extra 3"
model += l[7] - l[2] >= 0, "extra 4"

status = model.solve()

if status == pulp.LpStatusOptimal:
    print(model.objective.value())
    for i in loc:
        print(l[i], l[i].varValue)
    model.writeLP("metropolisLP")
