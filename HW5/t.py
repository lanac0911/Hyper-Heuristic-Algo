#HW5 One-Max Problem with Genetic Algorithm
import matplotlib.pyplot as plt
import random, math
import varibles, functions
import numpy as np

# 其他用參數
best_sol = 0
global_best = {'sol':0, 'list':[], 'run':0}
SELECTION_SIZE = 4
POPULATION_SIZE = 10
CROSSOVER_RATE = 0.8
MUTATION_RATE = 0.1
GENERATION_LIST = []

def cal_proba(list_group):
    dict = list_group.copy()
    proba_list = [] #[{'sol': 10, 'list': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]}, ....}
    sum = 0
    for one_member in dict:
        sum += one_member['sol']  
    for one_member in dict:
        proba_list.append(one_member['sol'] / sum)
    return proba_list

def proba_to_cumulative(p_list): # [0.0185, 0.1296, ...]
    cdf_list = []
    for i in range(len(p_list)):
        sum = 0
        for j in range(i+1):
            sum += p_list[j]
        cdf_list.insert(i, sum)
    return cdf_list #累積機率

def Selection(nums, cdf_l, popu_l): 
#nums = 4, cdf_l = [0.018, 0.129, ...], popu_l = [{'sol': 10, 'list': [1, 1, 1, 1, 1]}, ....}
    selected_list = []
    for i in range(nums): #ex. 總共選4個
        r = random.random()
        picked_idx = -1 #index of list
        if r <= cdf_l[0]: picked_idx = 0
        else: #當qk-1 < r < qk，則選擇第 k 個染色體 vk
            for i in range(1, len(cdf_l)): #1~10 (1 2 3 4 5 6 7 8 9)
                if r > cdf_l[i-1] and r <= cdf_l[i]: picked_idx =  i; break
            if picked_idx == -1: picked_idx = len(list) - 1 #last one
        #每組找完
        # print("########   #####picke idx=",picked_idx)
        selected_list.append(popu_l[picked_idx])
    return selected_list

def Selection2(nums, popu_l): 
#nums = 4, cdf_l = [0.018, 0.129, ...], popu_l = [{'sol': 10, 'list': [1, 1, 1, 1, 1]}, ....}
    selected_list = []
    tmep_obj = popu_l.copy()
    sort_list = sorted(tmep_obj, key=lambda d: d['sol']) 
    biggest = sort_list[0]['sol']
    for j in range(len(sort_list)):
        if sort_list[j]['sol'] < biggest:
            end_point = j; break
    print("sprt",sort_list)
    for i in range(nums-1, -1): #ex. 總共選4個
        if len(popu_l) >= nums:
            print("sort_List[",i,"]" , sort_list[i])
            selected_list.append(sort_list[i])
        else: 
            r = random.randint(0,end_point)
            selected_list.append(sort_list[r])
            

    print("over")
    return selected_list


def Crossover(list_group): #[{'sol': 4, 'list': [1, 1, 0, 1, 0, 0]}, ...]
    obj_list = list_group.copy()
    crossovered_list = []
    cross_index_cut = random.randint(0, varibles.BIT_LEN) # 單點交換：random要交配的切斷點index
    for idx in range(0, SELECTION_SIZE): #4-> 0 1 2 3 # 兩兩做交配
        result_list = obj_list[idx]['list'].copy()
        cross_r = random.random()
        if cross_r < CROSSOVER_RATE: # 小於則進行交換
            for j in range(cross_index_cut, varibles.BIT_LEN): # A[cross_index_cut]~A[last_index]
                    # print("可換 idx=", idx, "j=",j)
                    if idx%2 == 0: # 第一個0（偶數）list 與 第二個1（奇數）list 交換 
                        # print("偶數", idx,temp_list[idx][j],"與",  temp_list[idx+1][j],"交換")
                        # print("前", temp_list)
                        # obj_list[idx][j] = obj_list[idx+1][j]
                        result_list[j] =  obj_list[idx+1]['list'][j]
                        # print("後", temp_list)  
                    else: # 第二個list 跟 第一個list （偶數）交換 
                        # print("奇數", idx,temp_list[idx][j],"與",  temp_list[idx-1][j],"交換")
                        # print("前", temp_list)
                        # obj_list[idx][j] = obj_list[idx-1][j]
                        result_list[j] =  obj_list[idx-1]['list'][j]
                        # print("後", temp_list)  
        # print("結果", result_list)
        d = dict()
        d['sol'] = functions.Count_Sol(result_list)
        d['list'] = result_list
        crossovered_list.append(d)
    return crossovered_list



def Mutation(list_group):
    obj_list = list_group.copy() #[{'sol': 4, 'list': [1, 1, 0, 1, 0, 0]}, ...]
    mutation_list = [] # 兩兩交配吼額所有list
    for idx in range(0, SELECTION_SIZE ): #4 # 每個交配完的結果單獨決定要不要突變
        mutation_r = random.random()
        target_list = obj_list[idx]['list'].copy()
        if mutation_r < MUTATION_RATE:
            mutation_index = random.randint(0, varibles.BIT_LEN - 1) # 單點交換：random要突變的位置
            # print("交換 idx=",idx,"mutation_index=",mutation_index)
            target_list[mutation_index] = int(not target_list[mutation_index])
            # print("結果", target_list)
        d = dict()
        d['sol'] = functions.Count_Sol(target_list)
        d['list'] = target_list
        mutation_list.append(d)
    return mutation_list

def Genetic_Algorithm(n, type):
    sumlist = [0] * varibles.ITER
    global best_sol, global_best, GENERATION_LIST
    for run in range(varibles.RUNS):
        iter = 0; one_iter_sol_list = []
        # print("================第",run,"RUN================")
        init_popu = [] #[ {'sol': x, 'list':[] }, ...... ]
        # 先產生一組初始群體 （大小：POPULATION_SIZE）
        for i in range(POPULATION_SIZE):
            init_popu.append(functions.Random_Sol_Simple(n))
        print("init_popu=",init_popu)  #[{'sol': 10, 'list': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]}, ....}
        # print("init_popu=",init_popu)  #[{'sol': 10, 'list': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]}, ....}
        print("-")
        probability_list = cal_proba(init_popu) # [0.0185185, 0.1296296, ...]
        cdf_list = proba_to_cumulative(probability_list) # [0.114, 0.11428, ...]
        selected_list = Selection2(SELECTION_SIZE, init_popu) #[{'sol': 4, 'list': [1, 1, 0, 1, 0, 0]}, ...]
        # print("最初", selected_list)
        # print("最初", cdf_list)
        while iter < varibles.ITER:
            # print("[[[[[[[[[[[[ 回圈",iter,"]]]]]]]]]]]]")
            # ------ Crossover（選出的selected_list兩兩交配） ------
            crossovered_list = Crossover(selected_list) #[{'sol': 4, 'list': [1, 1, 0, 1, 0, 0]}, ...]
            # print("crossovered_list=",crossovered_list)
            # print("-")
            # ------ Mutation ------
            mutation_list = Mutation(crossovered_list) #[{'sol': 4, 'list': [1, 1, 0, 1, 0, 0]}, ...]
            # print("mutation_list=",mutation_list)
            # print("-")

            # ------ find the local/global best sol of this iteration ------
            local_best = 0; local_sum = 0
            for idx in range(0, SELECTION_SIZE):
                local_sum += mutation_list[idx]['sol']
                if mutation_list[idx]['sol'] > local_best: 
                    local_best =  mutation_list[idx]['sol'] #for local
                if mutation_list[idx]['sol'] > global_best['sol']: # for global
                    global_best['sol'] = mutation_list[idx]['sol']
                    global_best['list'] = mutation_list[idx]['list']
                    global_best['iter'] = run
            one_iter_sol_list.append(local_sum / SELECTION_SIZE) 
            # one_iter_sol_list.append(local_best) 
            # print("此one_iter_sol_list", one_iter_sol_list)
            # print("!!!!!!!!!!!!!!!!!!!!!!!\n\n")


            # ------ New population ------
            new_popu = mutation_list.copy()
            #  對現有population進行fitness評估 
            probability_list = cal_proba(new_popu) # [0.0185185, 0.1296296, ...]
            # print("probability_list=",probability_list)
            # print("-")
            cdf_list = proba_to_cumulative(probability_list) # [0.114, 0.11428, ...]
            # print("cdf_list=",cdf_list)
            # print("-")
            # 產生 POPULATION_SIZE 的族群
            # new_popu = Selection(POPULATION_SIZE, cdf_list, new_popu) #[{'sol': 4, 'list': [1, 1, 0, 1, 0, 0]}, ...]
            new_popu = Selection2(POPULATION_SIZE, new_popu) #[{'sol': 4, 'list': [1, 1, 0, 1, 0, 0]}, ...]
            # print("new_popu-",new_popu)                
            # print("-")
            probability_list = cal_proba(new_popu) # [0.0185185, 0.1296296, ...]
            cdf_list = proba_to_cumulative(probability_list) # [0.114, 0.11428, ...]
            # ------ Selection (by CDF) -----------------
            selected_list = Selection2(SELECTION_SIZE, new_popu) #[{'sol': 4, 'list': [1, 1, 0, 1, 0, 0]}, ...]
            # selected_list = Selection(SELECTION_SIZE, cdf_list, new_popu) #[{'sol': 4, 'list': [1, 1, 0, 1, 0, 0]}, ...]
            # print("selected_list=",selected_list)
            # print("-")            
            iter += 1
        sumlist = np.array(sumlist) + np.array(one_iter_sol_list)
    sumlist = np.divide(sumlist, varibles.RUNS)
    print("sumlist=",sumlist)
    return (sumlist, global_best) 





def HW5_main(draw):
    global best_sol
    type = 'One Max Problem'
    n = varibles.BIT_LEN
    (result, global_best) =  Genetic_Algorithm(n, type)
    if(draw):
        print_content = [ "在第" + str(global_best['iter']) + "回時有最佳解:" + str(global_best['sol']) + "，\n內容為："+ str(global_best['list'])]
        functions.Draw(print_content,varibles.ALGO, 1, result, [])
    else: return result