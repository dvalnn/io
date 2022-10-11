import pulp

# Produção de Relógios para o aeroporto

M = 10e5 # valor "muito elevado" para forçar a relação entre as variáveis

# DADOS
preço_venda = [[22, 22, 28, 28, 28, 30], [35, 35, 42, 42, 42, 42], [30, 30, 40, 40, 40, 45], [26, 26, 32, 32, 32, 28]]
procura = [[10, 12, 8, 20, 15, 10], [15, 10, 5, 9, 8, 5], [8, 6, 5, 7, 4, 2], [4, 3, 7, 2, 2, 1]]
custo_fixo = [120, 100, 75, 200]
custo_var = [5, 6, 7, 9]
capacidade_max = [60, 35, 20, 15]

# CONJUNTOS
relogios = range(4)
lojas = range(6)

# VARIÁVEIS
x = pulp.LpVariable.dicts("x", [(i, j) for i in relogios for j in lojas], cat=pulp.LpContinuous, lowBound=0)
y = pulp.LpVariable.dicts("y", [(i, j) for i in relogios for j in lojas], cat=pulp.LpBinary)
w = pulp.LpVariable.dicts("w", relogios, cat=pulp.LpBinary)

# MODELO
model = pulp.LpProblem("relogios para o aeroporto", pulp.LpMaximize)

# FUNÇÃO OBJETIVO
model += (
    sum(preço_venda[i][j] * x[(i, j)] for i in relogios for j in lojas)
    - sum(custo_var[i] * x[(i, j)] for i in relogios for j in lojas)
    - sum(custo_fixo[i] * w[i] for i in relogios)
)

# RESTRIÇÕES
for i in relogios:
    model += sum(x[(i, j)] for j in lojas) / capacidade_max[i] <= 1, f"Capacidade Máxima de Produção{i}"
    model += sum(y[(i, j)] for j in range(2)) <= 1, f"Não repetir modelo {i} no terminal 1"
    model += sum(y[(i, j)] for j in range(2, 5)) <= 1, f"Não repetir modelo {i} no terminal 2"

    for j in lojas:
        model += x[(i, j)] <= procura[i][j], f"Venda max de {i} em {j}"

# RELACIONAR Y E W COM X
for i in relogios:
    for j in lojas:
        model += x[(i, j)] - y[(i, j)] * M <= 0, f"Se x{i}{j} então y{i}{j}"
        model += x[(i, j)] - w[i] * M <= 0, f"Se x{i}{j} então w{i}"

status = model.solve()

if status == pulp.LpStatusOptimal:
    for i in relogios:
        print(w[i], w[i].varValue)
        for j in lojas:
            print("-->", x[(i, j)], x[(i, j)].varValue)
            print("-->", y[(i, j)], y[(i, j)].varValue)
            print("\n")
        print("------------------")
    model.writeLP("relogiosLP")
    
