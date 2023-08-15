#HW5 One-Max Problem with Genetic Algorithm
import random
import varibles, functions
import numpy as np

# 其他用參數
best_sol = 0
global_best_t = {'sol':0, 'list':[], 'run':0}
global_best_w = {'sol':0, 'list':[], 'run':0}
POPULATION_SIZE = 20
CROSSOVER_RATE = 0.7
MUTATION_RATE = 0.1
GENERATION_LIST = []

def Update_Optaimal(type,sol, list, run):
    global global_best_t, global_best_w
    if type == 't':
        global_best_t["sol"] = sol
        global_best_t["list"] = list
        global_best_t['iter'] = run
    elif type == 'w':
        global_best_w["sol"] = sol
        global_best_w["list"] = list
        global_best_w['iter'] = run


def Crossover(objects): #[{'sol': 4, 'list': [1, 1, 0, 1, 0, 0]}, ...]
    obj1 = objects[0].copy(); obj2 = objects[1].copy()
    offspring1 = []; offspring2 =[]
    cross_r = random.random()
    if cross_r < CROSSOVER_RATE: # 小於則進行交換
        cross_index_cut = random.randint(0, varibles.BIT_LEN-1) # 單點交換：random要交配的切斷點index
        offspring1 = obj1['list'][:cross_index_cut] + obj2['list'][cross_index_cut:]
        offspring2 = obj2['list'][:cross_index_cut] + obj1['list'][cross_index_cut:]
    else: offspring1 = obj1['list']; offspring2 = obj2['list']
    d1 = functions.Update_Optaimal(offspring1)
    d2 = functions.Update_Optaimal(offspring2)
    return (d1, d2)


def Mutation(objects):#[{'sol': 4, 'list': [1, 1, 0, 1, 0, 0]}, ...]
    objs = objects.copy()
    for idx in range(2): #4 # 每個交配完的結果單獨決定要不要突變
        mutation_r = random.random()
        if mutation_r < MUTATION_RATE:
            mutation_index = random.randint(0, varibles.BIT_LEN - 1) # 單點交換：random要突變的位置
            objs[idx]['list'][mutation_index] = int(not objs[idx]['list'][mutation_index])
    return (objs[0], objs[1])

def Selection_Tournament(list):
    parent_candiate = []
    for _ in range(2): #生成候選人
        candiates = random.sample(list, 2) 
        parent_candiate.append(functions.biggest(candiates))
    return (parent_candiate[0], parent_candiate[1])


def Selection_Wheel(popu_l, cdf_l): 
    selected_list = []
    for i in range(2): #ex. 總共選
        r = random.random()
        picked_idx = -1 #index of list
        if r <= cdf_l[0]: picked_idx = 0
        else: #當qk-1 < r < qk，則選擇第 k 個染色體 vk
            for i in range(1, len(cdf_l)): #1~10 (1 2 3 4 5 6 7 8 9)
                if r > cdf_l[i-1] and r <= cdf_l[i]: picked_idx =  i; break
            if picked_idx == -1: picked_idx = len(list) - 1 #last one
        #每組找完
        selected_list.append(popu_l[picked_idx])
    return ([selected_list[0], selected_list[1]])



def Genetic_Algorithm(n, type):
    sumlist_t = [0] * varibles.ITER; sumlist_w = [0] * varibles.ITER
    global best_sol, global_best_t, global_best_w, GENERATION_LIST
    for run in range(varibles.RUNS):
        iter = 0; one_iter_sol_list_t = []; one_iter_sol_list_w = []
        init_popu = functions.Generate_init(POPULATION_SIZE,n) # 先產生一組初始群體 （大小：POPULATION_SIZE）
        population_list_t = init_popu.copy() #for tourment
        population_list_w = init_popu.copy() #for wheel
        while iter < varibles.ITER:
            probability_list = functions.cal_proba(population_list_w) # [0.0185185, 0.1296296, ...]
            cdf_list = functions.proba_to_cumulative(probability_list) # [0.114, 0.11428, ...]
            # 從population中取兩個最大的 -> operate -> 產生兩offsprings 
            mutate_list_t = [] #for tourment
            mutate_list_w = [] #for wheel
            for _ in range(int(POPULATION_SIZE / 2)):  # repeat到總共獲得POPULATION_SIZE個offsprings 
                # ------ Selection_Tournament (by CDF) -----------------
                parent1, parent2 = Selection_Tournament(population_list_t) # tou
                parent3, parent4 = Selection_Wheel(population_list_w, cdf_list) # wheel
                # ------ Crossover ------
                crossoverd1, crossoverd2 = Crossover([parent1, parent2])
                crossoverd3, crossoverd4 = Crossover([parent3, parent4])
                # ------ Mutation ------
                (mutated1, mutated2) = Mutation([crossoverd1, crossoverd2])
                (mutated3, mutated4) = Mutation([crossoverd3, crossoverd4])
                mutate_list_t.append(mutated1); mutate_list_t.append(mutated2)
                mutate_list_w.append(mutated3); mutate_list_w.append(mutated4)
            
            #------ find the local/global best sol of this iteration ------
            local_best_t = 0; local_best_w = 0; 
            local_best_t = (max(mutate_list_t, key=lambda d: d['sol']))['sol']
            local_best_w = (max(mutate_list_w, key=lambda d: d['sol']))['sol']
            for idx in range(0, POPULATION_SIZE):
                if mutate_list_t[idx]['sol'] > global_best_t['sol']: # for global
                    Update_Optaimal('t',mutate_list_t[idx]['sol'], mutate_list_t[idx]['list'], run)
                if mutate_list_w[idx]['sol'] > global_best_w['sol']: # for global
                    Update_Optaimal('w',mutate_list_w[idx]['sol'], mutate_list_w[idx]['list'], run)
            one_iter_sol_list_t.append(local_best_t) 
            one_iter_sol_list_w.append(local_best_w) 

            # get numbers of list whiich is contain POPULATION_SIZE offspraings
            population_list_t = mutate_list_t
            population_list_w = mutate_list_w

            iter += 1
        sumlist_t = np.array(sumlist_t) + np.array(one_iter_sol_list_t)
        sumlist_w = np.array(sumlist_w) + np.array(one_iter_sol_list_w)
    sumlist_t = np.divide(sumlist_t, varibles.RUNS)
    sumlist_w = np.divide(sumlist_w, varibles.RUNS)
    return (sumlist_t, sumlist_w, global_best_t, global_best_w) 



def HW5_main(draw):
    global best_sol
    type = 'One Max Problem'
    n = varibles.BIT_LEN
    print_content = []; result = []
    (result_t, result_w, global_best_t, global_best_w) =  Genetic_Algorithm(n, type)
    if(draw):
        print_content_t = [ "(Tournament) 在第" + str(global_best_t['iter']) + "回時有最佳解:" + str(global_best_t['sol']) + "，\n 內容為："+ str(global_best_t['list'])]
        print_content_w = [ "(Roulette Wheel) 在第" + str(global_best_w['iter']) + "回時有最佳解:" + str(global_best_w['sol']) + "，\n 內容為："+ str(global_best_w['list'])]
        print_content.append(print_content_t);print_content.append(print_content_w)
        result.append(result_t); result.append(result_w)
        functions.Draw(print_content,varibles.ALGO, 1, result, [])
    else: return result