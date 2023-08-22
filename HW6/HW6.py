#HW6  One-Max Problem with Ant Colony Optimization
import random
import varibles, functions
import numpy as np
from scipy.spatial import distance

# 其他用參數
global_best = { 'distance':0, 'path':[] }
ANT_NUMS = 3
CITY_NUMS = 30
CITY_NAMES = []
alpha = 1
beta = 2
rh_rate = 0.1 #費洛蒙衰退參數



def Get_Distance_Matrix(fileName):
    res = []
    with open(fileName, 'r') as f:
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

def Selection_Wheel(cdf_l, candidates_city): 
    r = random.random()
    picked_idx = -1 #index of list
    if r <= cdf_l[0]: picked_idx = 0
    else: #當qk-1 < r < qk，則選擇第 k 個染色體 vk
        for i in range(1, len(cdf_l)): #1~10 (1 2 3 4 5 6 7 8 9)
            if r > cdf_l[i-1] and r <= cdf_l[i]: picked_idx =  i; break
        if picked_idx == -1: picked_idx = len(candidates_city) - 1 #last one
    return candidates_city[picked_idx]

def An_Ant_Trip(An_Ant_Path, Pheromone_Table, visibility, Dist_Martix):
    # print("-----------")
    # print("An_Ant_Path=",An_Ant_Path)
    # print("Pheromone_Table=",Pheromone_Table)
    # print("visibility=",visibility)
    # print("-----------")
    # 建構一個解 => "一隻"螞蟻完成所有城市的流程    
    distance = 0
    candidates_city = [len for len in range(CITY_NUMS)] # 未訪問城市
    now_city_id = random.choice(candidates_city ) # 1.隨機挑選起始城市
    An_Ant_Path[0] = now_city_id # 2.加入路徑
    candidates_city.remove(now_city_id) # 3.放問過 ＝> 移除
    
    # select/calculate 下個要訪問的city (form candidates_city)
    for i in range(1, CITY_NUMS-1):
        # 計算
        fitness_list = []
        for city_idx in candidates_city:
            fitness = pow(Pheromone_Table[now_city_id][city_idx], alpha) *\
                      pow(visibility[now_city_id][city_idx], beta)
            fitness_list.append(fitness)
        # 用輪盤法找下一個
        cdf_list = functions.proba_to_cumulative(fitness_list) # [0.114, 0.11428, ...]
        picked_city_idx = Selection_Wheel(cdf_list, candidates_city) # wheel
        candidates_city.remove(picked_city_idx)
        An_Ant_Path[i] = picked_city_idx
        # 計算距離
        distance += Dist_Martix[now_city_id][picked_city_idx]

        now_city_id = picked_city_idx
    # 會剩最後一個
    distance += Dist_Martix[now_city_id][candidates_city[0]]
    An_Ant_Path[-1] = candidates_city.pop()
    return (An_Ant_Path, distance)

def Update_Optaimal(Distances, Solutions):
    global global_best
    temp_dis = 2000; temp_path = []
    for i in range(len(Distances)):
        if Distances[i] < temp_dis: 
            temp_dis = Distances[i]
            temp_path = Solutions[i]
    global_best['distance'] = temp_dis
    global_best['path'] = temp_path






def Ant_Colony_Optimization():
    iter = 0; global global_best
    All_Solutions = []; All_Distances = []; total_distance = 0
    Dist_Martix = Get_Distance_Matrix('t2.txt') # 初始距離矩陣
    Pheromone_Table = np.ones((CITY_NUMS, CITY_NUMS)) #費洛蒙表
    print("!!", (Pheromone_Table))
    An_Ant_Path = np.zeros(CITY_NUMS) # 一隻螞蟻的路徑
    Best_Path = np.zeros((ANT_NUMS, CITY_NUMS)) #某隻螞蟻的最佳路經
    visibility = np.divide(1.0,Dist_Martix) # 距離的倒數
  # -------- 建所有解 --------
    for _ in range(ANT_NUMS):
        (a_solution, a_distance) = An_Ant_Trip(An_Ant_Path, Pheromone_Table, visibility, Dist_Martix)
        All_Solutions.append(a_solution)
        All_Distances.append(a_distance)
        total_distance += a_distance
    print("All_Solutions =",All_Solutions)
    print("All_Distances =",All_Distances)
    print("===========================")
  # -------- 更新費洛蒙 --------
    # τ(i,j) = ρ * τ(i,j) +  Δτ(i,j) = (原本這條路的費洛蒙)*揮發速度 + Δτ(i,j)
    temp_Pheromen = np.zeros((CITY_NUMS, CITY_NUMS))
    for i in range(ANT_NUMS): # 計算每個螞蟻的
        print("i---------------------------------------",i)
        for j in range(CITY_NUMS - 1):  # 計算每個螞蟻的 每個城市
            city1 = int(All_Solutions[i][j]); city2 = int(All_Solutions[i][j+1])
            temp_Pheromen[city1][city2] += 1 / All_Distances[i]
        city1 = int(All_Solutions[i][j+1]); city2 = int(All_Solutions[i][0])
        temp_Pheromen[city1][city2] += 1 / All_Distances[i]
    Pheromone_Table = rh_rate*Pheromone_Table + temp_Pheromen # 揮發
  # -------- 更新路徑 --------
    Update_Optaimal(All_Distances, All_Solutions)
        
    while iter < 1:

        iter+=1

        #
            



def HW6_main(draw):
    Ant_Colony_Optimization()
    
    
