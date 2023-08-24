
#HW6  Travelling Salesman Problem with Ant Colony Optimization
import random, math
import varibles, functions
import numpy as np
from scipy.spatial import distance
import matplotlib.pyplot as plt

# 其他用參數
global_best = {'sol':1000, 'list':[], 'run':0}
ANT_NUMS = 10
CITY_NUMS = 51
CITY_NAMES = []
alpha = 1
beta = 3
Q = 10
RH_RATE = 0.7 #費洛蒙衰退參數
Pheromone_Table = []



def Get_Distance_Matrix(fileName):
    res = []
    with open(fileName, 'r') as f:
        print(f)
        res = []; start = False
        for line in f.readlines():
            split_item = line.split()
            if(split_item[0] == 'EOF'): break
            if(split_item[0] == '1'): start = True
            if(start):
                item = []
                CITY_NAMES.append(split_item[0])
                item.append(int(split_item[1])); item.append(int(split_item[2]))
                res.append(item)
    martrix = distance.cdist(res, res, 'euclidean')
    #更改對角線
    row, col = np.diag_indices_from(martrix)
    martrix[row, col] = 1000
    return martrix

def Selection_Wheel(fitness_list, candidates_city): 
    sum_fitness = sum(fitness_list)
    prob_list = np.divide(fitness_list, sum_fitness)
    cdf_l = functions.proba_to_cumulative(prob_list) # 累積機率
    r = random.random()
    picked_idx = -1 #index of list
    if r <= cdf_l[0]: picked_idx = 0
    else: #當qk-1 < r < qk，則選擇第 k 個染色體 vk
        for i in range(1, len(cdf_l)): #1~10 (1 2 3 4 5 6 7 8 9)
            if r > cdf_l[i-1] and r <= cdf_l[i]: picked_idx =  i; break
        if picked_idx == -1: picked_idx = len(candidates_city) - 1 #last one
    return candidates_city[picked_idx]


def Ant_Colony_Optimization():
    # 讀取TSP資料
    Dist_Martix = Get_Distance_Matrix('eil51.tsp') # 距離矩陣
    Visibility = np.divide(1, Dist_Martix) # 能見度(距離的倒數)
    sum_solutions = np.zeros(varibles.ITER)
    for run in range(varibles.RUNS):
        print(f"執行第{run}RUN...")
        # 資訊初始化
        Pheromone = np.ones((CITY_NUMS, CITY_NUMS)) # 費洛蒙
        all_solutions = []

        for _ in range(varibles.ITER):
            # ------- 遍歷each ant ------- 
            all_ants_path = []; 
            for _ in range(ANT_NUMS):
                # 變數s
                an_ant_path = [] # 其中一隻ant的路程(解)
                unvisit = [city for city in range(CITY_NUMS)] # 未訪問city(初始化)
                # 決定起始city
                current_city_id = random.choice(unvisit)
                # 加入path & 修改未訪問city list
                an_ant_path.append(current_city_id); unvisit.remove(current_city_id)
                #  ------- 遍歷each unvisit cities -------
                an_ant_length = 0; 
                while (unvisit):
                    fitness_list = []
                    # 計算剩下的city的機率 (pheromone^alpha) * (visibility^beta)
                    for city_idx in unvisit:
                        fitness = pow(Pheromone[current_city_id][city_idx], alpha) *\
                                pow(Visibility[current_city_id][city_idx], beta)
                        fitness_list.append(fitness)
                    # 用［輪盤法］決定下一個city
                    picked_city_id = Selection_Wheel(fitness_list, unvisit)
                    # 加入path & 修改未訪問city list
                    an_ant_path.append(picked_city_id); unvisit.remove(picked_city_id)
                    #
                    an_ant_length += Dist_Martix[current_city_id][picked_city_id]
                    current_city_id = picked_city_id
                # print(f"{ant}號ant的路線", an_ant_length, an_ant_path)
                all_ants_path.append({'length': an_ant_length, 'path': an_ant_path})
            # print("all=",(all_ants_path))
            
            # ------- 更新費洛蒙 -------
            # 先蒸發濃度
            Pheromone *= RH_RATE
            # 更新走過的路線
            for a_sol in all_ants_path:
                a_path = a_sol['path']
                delta =  Q / a_sol['length']
                for idx in range(len(a_path) - 1): 
                    Pheromone[a_path[idx]][a_path[idx+1]] += delta
                # 終點->起點的另外算
                Pheromone[a_path[idx+1]][a_path[0]] += delta

            # ------- 更新最佳解/路徑 -------
            best_sol = min(all_ants_path,  key=lambda x: x['length']) 
            all_solutions.append(best_sol) # each iter's ant's best sol
            length_values = [entry['length'] for entry in all_solutions]

        # ------- 更新最佳解/路徑 -------
        best = min(length_values)
        min_obj = min(all_solutions, key=lambda x: x['length'])
        best = min_obj['length']
        if best < global_best['sol']:
            global_best['sol'] = best
            global_best['list'] = min_obj['path']
            global_best['run'] = run

        sum_solutions = np.array(sum_solutions) + np.array(length_values)
    sum_solutions = np.divide(sum_solutions, varibles.RUNS)
    return (sum_solutions, global_best)


        


def HW6_main(draw):
    global best_sol
    type = 'Travel Salesman Problem'
    result = []
    (result, global_best) = Ant_Colony_Optimization()
    if(draw):
        print_content = [ "在第" + str(global_best['run']) + "回時有最佳解:" + 
                         str(global_best['sol']) + "，\n內容為："+ 
                         str(global_best['list'])
                        ]
        functions.Draw(print_content,varibles.ALGO, 1, result, [])
        #
    else: return result
    


