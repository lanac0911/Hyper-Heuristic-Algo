#HW5 One-Max Problem with Genetic Algorithm
import matplotlib.pyplot as plt
import random, math
import varibles, functions
import numpy as np

# 其他用參數
best_sol = 0
global_best = {'sol':0, 'list':[], 'run':0}
SELECTION_SIZE = 6
POPULATION_SIZE = 10
CROSSOVER_RATE = 0.9
MUTATION_RATE = 0.1
GENERATION_LIST = []

def cal_proba(list_group):
    dict = list_group.copy()
    proba_list = [] #[{'sol': 10, 'list': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]}, ....}
    sum = 0
    for one_member in dict:
        sum += one_member['sol']  
    for one_member in dict:
        if sum == 0: proba_list.append(0)
        else:
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
            

    return selected_list

def Crossover(objects): #[{'sol': 4, 'list': [1, 1, 0, 1, 0, 0]}, ...]
    obj1 = objects[0].copy(); obj2 = objects[1].copy()
    offspring1 = []; offspring2 =[]
    cross_r = random.random()
    # print("@@@ 交換前", obj1['list'],obj2['list'])
    if cross_r < CROSSOVER_RATE: # 小於則進行交換
        cross_index_cut = random.randint(0, varibles.BIT_LEN-1) # 單點交換：random要交配的切斷點index
        # print("交換！form ",cross_index_cut)
        offspring1 = obj1['list'][:cross_index_cut] + obj2['list'][cross_index_cut:]
        offspring2 = obj2['list'][:cross_index_cut] + obj1['list'][cross_index_cut:]
    else: offspring1 = obj1['list']; offspring2 = obj2['list']
    d1 = dict(); d2 = dict()
    d1['sol'] = functions.Count_Sol(offspring1); d2['sol'] = functions.Count_Sol(offspring2)
    d1['list'] = offspring1; d2['list'] = offspring2
    # crossovered_list.append(d1); crossovered_list.append(d2)
    # print("@@@ 交換後", d1,d2)
    # print("-")
    return (d1, d2)



def Mutation(objects):#[{'sol': 4, 'list': [1, 1, 0, 1, 0, 0]}, ...]
    objs = objects.copy()
    # print("變異", objs)
    for idx in range(2): #4 # 每個交配完的結果單獨決定要不要突變
        mutation_r = random.random()
        # print("第",idx,"下 r = ",mutation_r)
        if mutation_r < MUTATION_RATE:
            mutation_index = random.randint(0, varibles.BIT_LEN - 1) # 單點交換：random要突變的位置
            # print("要突變！！！！",mutation_index )
            objs[idx]['list'][mutation_index] = int(not objs[idx]['list'][mutation_index])
    # print("後", objs)
    return (objs[0], objs[1])


def biggest(obj):
    sort_list = sorted(obj, key=lambda d: d['sol'], reverse=True) 
    return sort_list[0]

def Selection(list):
    parent_candiate = []
    for _ in range(2): #生成候選人
        candiates = random.sample(list, 2) 
        parent_candiate.append(biggest(candiates))
    return (parent_candiate[0], parent_candiate[1])

def Genetic_Algorithm(n, type):
    sumlist = [0] * varibles.ITER
    global best_sol, global_best, GENERATION_LIST
    for run in range(varibles.RUNS):
        iter = 0; one_iter_sol_list = []
        print("==========================第",run,"RUN===========================")
        init_popu = [] #[ {'sol': x, 'list':[] }, ...... ]
        # 先產生一組初始群體 （大小：POPULATION_SIZE）
        for _ in range(POPULATION_SIZE):
            init_popu.append(functions.Random_Sol_Simple(n))
        population_list = init_popu.copy()

        # print("最初", cdf_list)
        while iter < varibles.ITER:
            # print("========第",iter,"iter========")
            # ------ Fitness (by CDF) -----------------
            probability_list = cal_proba(population_list) # [0.0185185, 0.1296296, ...]
            cdf_list = proba_to_cumulative(probability_list) # [0.114, 0.11428, ...]
            # print("population_list==",population_list)
            # print("--\n")
            # ------ Selection (by CDF) -----------------
            # 從population中取兩個最大的 -> operate -> 產生兩offsprings 
            # population_list = sorted(population_list, key=lambda d: d, reverse=True)  # large -> small
            crossover_list = []; mutate_list = []
            for _ in range(int(POPULATION_SIZE / 2)):  # repeat到總共獲得POPULATION_SIZE個offsprings 
                parent1, parent2 = Selection(population_list)
                # print("選中的",parent1, parent2)
                # ------ Crossover ------
                crossoverd1, crossoverd2 = Crossover([parent1, parent2])
                crossover_list.append(crossoverd1);  crossover_list.append(crossoverd2) #get a list contaion 2 offsprings
                
                # ------ Mutation ------
                (mutated1, mutated2) = Mutation([crossoverd1, crossoverd2])
                mutate_list.append(mutated1); mutate_list.append(mutated2)
            # print("crossover_list = ",crossover_list)
            # print("--\n")
            # print("mutate_list = ",mutate_list)
            # print("--\n")
            #------ find the local/global best sol of this iteration ------
            local_best = 0; local_sum = 0
            for idx in range(0, POPULATION_SIZE):
                local_sum += mutate_list[idx]['sol']
                if mutate_list[idx]['sol'] > local_best: 
                    local_best =  mutate_list[idx]['sol'] #for local
                if mutate_list[idx]['sol'] > global_best['sol']: # for global
                    global_best['sol'] = mutate_list[idx]['sol']
                    global_best['list'] = mutate_list[idx]['list']
                    global_best['iter'] = run
            # one_iter_sol_list.append(local_sum / POPULATION_SIZE) 
            one_iter_sol_list.append(local_best) 
            # print("此one_iter_sol_list", one_iter_sol_list)
            print("!!!!!!!!!!!!!!!!!!!!!!!\n\n")

            # get numbers of list whiich is contain POPULATION_SIZE offspraings
            population_list = mutate_list



  
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