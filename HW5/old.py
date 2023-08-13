import random
import matplotlib.pyplot as plt

# 定義問題設定
target_length = 10  # 二進位字串長度
population_size = 50  # 個體群體大小
mutation_rate = 0.1  # 變異率
generations = 10  # 迭代代數

# 創建初始個體
def create_individual():
    return [random.choice([0, 1]) for _ in range(target_length)]

# 計算適應度
def fitness(individual):
    return sum(individual)

# 交叉操作
def crossover(parent1, parent2):
    crossover_point = random.randint(1, target_length - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

# 變異操作
def mutate(individual):
    gene_index = random.randint(0, target_length - 1)
    if random.random() < mutation_rate:
        individual[gene_index] = 1 - individual[gene_index]

# 選擇過程（使用競賽法）
def select(population, num_parents):
    selected_parents = []
    for _ in range(num_parents):
        competitors = random.sample(population, 2)  # 隨機選取兩個競爭者
        winner = max(competitors, key=fitness)  # 選擇適應度較高者作為父代
        selected_parents.append(winner)
    return selected_parents

# 初始化列表來儲存每代的最佳適應度
best_fitnesses_per_run = []

# 執行多次遺傳演算法並收集執行結果
num_runs = 51

for run in range(num_runs):
    print("==========================第",run,"RUN===========================")
    population = [create_individual() for _ in range(population_size)]
    print("population=",population)
    best_fitnesses = []
    # 主要迭代過程
    for generation in range(generations):
        print("========第",generation,"iter========")
        population = sorted(population, key=fitness, reverse=True)  # 根據適應度排序
        print("pop sort",population)
        new_population = []

        for i in range(0, population_size, 2):
            print("!!!!第",i,"i!!!!!!!")
            parent1, parent2 = select(population, 2)  # 選擇parent
            print("selse 2", parent1, parent2)
            child1, child2 = crossover(parent1, parent2)
            print("cross 2", child1, child2)
            mutate(child1)
            mutate(child2)
            new_population.extend([child1, child2])

        population = new_population
        # 找到每代的最佳適應度並儲存
        best_fitnesses.append(fitness(max(population, key=fitness)))
    best_fitnesses_per_run.append(best_fitnesses)

# 計算每代的平均適應度
average_best_fitnesses = [sum(fitnesses) / num_runs for fitnesses in zip(*best_fitnesses_per_run)]

# 繪製平均適應度隨迭代次數變化的折線圖
plt.plot(range(generations), average_best_fitnesses)
plt.xlabel('Generation')
plt.ylabel('Average Best Fitness')
plt.title('Average Fitness Convergence over 51 Runs')
plt.savefig('Average Fitness Convergence over 51 Runs.png')
plt.show()
