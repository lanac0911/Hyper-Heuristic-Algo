#HW5 One-Max Problem with Genetic Algorithm
import matplotlib.pyplot as plt
import random, math
import varibles, functions
import numpy as np

# 其他用參數
best_sol = 0
global_best = {'sol':0, 'list':[], 'iter':0}
SELECTION_SIZE = 4
POPULATION_SIZE = 10
CROSSOVER_RATE = 0.6
MUTATION_RATE = 0.6
GENERATION_LIST = []

def cal_p(list, type):
    sum = 0
    p_list = []
    p_sum_list = []
    if type == 1:
        for item in list:
            sum += item['one_nums']
            p_list.append(item['one_nums'])
    else:
        for a_list in list:
            local_sol = 0
            for item in a_list:
                if item: local_sol += 1
                sum += item
            p_list.append(local_sol)
    p_list = np.divide(p_list,sum) #機率 
    # 機率 to 累積機率
    for i in range(len(p_list)):
        # print("i=",i)
        sum = 0
        for j in range(i+1):
            # print("j=",j)
            # print("p_list[j]=",p_list[j])
            sum += p_list[j]
        # print("!!!",i,"=",sum)
        p_sum_list.insert(i, sum)
    return p_sum_list #累積機率

# r=0.6 li=[0.3, 0.4, 0.5, 0.6, 0.7]
#            0    1    2    3    4 
def Select_By_P(r, list):
    picked = -1 #index of list
    if r <= list[0]: picked = 0
    else: #當qk-1 < r < qk，則選擇第 k 個染色體 vk
        for i in range(1, len(list)): #1~5 (1 2 3 4)
            if r > list[i-1] and r <= list[i]: picked =  i; break
        if picked == -1: picked = len(list) - 1 #last one
    return picked

def CrossOver(index, list, i):
    # print("進來的list=", index, list, i)
    temp_list = list.copy()
    for j in range(index, varibles.BIT_LEN): # A[index]~A[last_index]
        cross_r = random.random()
        # print("j=",j)
        if cross_r < CROSSOVER_RATE: # 小於則進行交換
            # print("可換")
            if i%2 == 0: # 第一個0（偶數）list 與 第二個1（奇數）list 交換 
                # print("偶數", i,temp_list[i][j],"與",  temp_list[i+1][j],"交換")
                # print("前", temp_list)
                temp_list[i][j] = temp_list[i+1][j]
                # print("後", temp_list)  
            else: # 第二個list 跟 第一個list （偶數）交換 
                # print("奇數", i,temp_list[i][j],"與",  temp_list[i-1][j],"交換")
                # print("前", temp_list)
                temp_list[i][j] = temp_list[i-1][j]
                # print("後", temp_list)  
            # print("===========")
    # print("結果", temp_list[i])
    return temp_list[i]

def Mutation(index, list):
    list[index] = int(not list[index])
    return list

def Update_Optaimal(new_best, new_best_list, runs):
    global best_sol, global_best
    best_sol = new_best #更新global optimal
    #for all
    global_best["sol"] = new_best
    global_best["list"] = new_best_list
    global_best['iter'] = runs

def cal_a_p(list):
    local_sol = 0
    for item in list:
        if item: local_sol += 1
        sum += item
    p_list.append(local_sol)
    p_list = np.divide(p_list,sum) #機率 
    # 機率 to 累積機率
    for i in range(len(p_list)):
        # print("i=",i)
        sum = 0
        for j in range(i+1):
            # print("j=",j)
            # print("p_list[j]=",p_list[j])
            sum += p_list[j]
        # print("!!!",i,"=",sum)
        p_sum_list.insert(i, sum)
    # print("ans",p_sum_list)
    return p_sum_list #累積機率

def Genetic_Algorithm(n, type):
    sumlist = [0] * varibles.ITER
    global best_sol, global_best, GENERATION_LIST
    for run in range(varibles.RUNS):
        print("================第",run,"RUN================")
        temp_list = []
        one_iter_sol_list = []
        # ------- Initialize Population 生成x組初始解 -------
        init_obj_sets = [] # [{one_nums:, zero_nums:, random_list: },{},{},......]
        iter = 0
        for k in range(POPULATION_SIZE):
            init_obj = functions.Random_Sol(n) # 隨機產生一組初始解
            
            init_obj_sets.append(init_obj)
            init_sol = init_obj['one_nums']; best_sol = init_sol
            temp_list.append(init_obj['random_list'])
        
        CD_list = cal_p(init_obj_sets, 1)
        GENERATION_LIST = temp_list
        print("GENERATION_LIST!!!!!",GENERATION_LIST)
        print("CD_list  vs",CD_list)
        while iter < varibles.ITER:
            print("==------第",iter,"iter=------=")
            # ------------ Selection ----------
            picked_list = []
            for l in range(SELECTION_SIZE):
                r = random.random()
                picked_index = (Select_By_P(r, CD_list))
                picklist = GENERATION_LIST[picked_index].copy()
                picked_list.append(picklist )
            print("被選中的",picked_list)
            # ------------ Crossover ----------
            crossovered_list = [] # 兩兩交配後的所有list
            cross_index = random.randint(0, varibles.BIT_LEN - 1) # 單點交換：random要交配的切斷點index
            temp = picked_list.copy()
            for idx in range(0, SELECTION_SIZE): #4 # 兩兩做交配
                # cross_r = random.random()
                # if cross_r < CROSSOVER_RATE: # 小於則進行交換
                crossovered_list.append(CrossOver(cross_index, temp, idx))
            print("交配完後",crossovered_list)
            # ------------ Mutation ----------
            mutation_list = [] # 兩兩交配吼額所有list
            for idx2 in range(0, SELECTION_SIZE): #4 # 每個交配完的結果單獨決定要不要突變
                mutation_r = random.random()
                result = crossovered_list[idx2]
                if mutation_r < MUTATION_RATE:
                    mutation_index = random.randint(0, varibles.BIT_LEN - 1) # 單點交換：random要突變的位置
                    result = Mutation(mutation_index, crossovered_list[idx2])
                mutation_list.append(result)
            print("突變完後",mutation_list)
            # 計算適應值(Fitness Value) 一次iteration會有 SELECTION_SIZE 組解
            best_sol = 0
            for i in range(SELECTION_SIZE):
                temp_sol = functions.Count_Sol(mutation_list[i])
                if temp_sol >= best_sol:
                    Update_Optaimal(temp_sol, mutation_list[i], run)
                # else: temp_sol = 0
                print("sol-",i,"=",temp_sol)
            print("最好",best_sol)
            one_iter_sol_list.append(temp_sol) 
            GENERATION_LIST = mutation_list
            CD_list = cal_p(mutation_list,2)
            print("子代 ＬＩ",GENERATION_LIST)
            print("子代 ＣＤ",CD_list)
            iter += 1
        print("此地會結果",one_iter_sol_list)
        sumlist = np.array(sumlist) + np.array(one_iter_sol_list) #算平均用
        print("sumlist=",sumlist)
    sumlist = np.divide(sumlist, varibles.RUNS)
    print("after sumlist=",sumlist)
    return (sumlist, global_best) 
        


def HW5_main():
    global best_sol
    type = 'One Max Problem'
    n = varibles.BIT_LEN
    Genetic_Algorithm(n, type)
    # (result, global_best) = Genetic_Algorithm(n, type)
    # print_content = [ "在第" + str(global_best['iter']) + "回時有最佳解:" + str(global_best['sol']) + "，\n內容為："+ str(global_best['list'])]
    # functions.Draw(print_content,varibles.ALGO, problem, result, [])

