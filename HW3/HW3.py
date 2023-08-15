#HW3 One-Max Problem with Simulated Annealing
import random, math
import varibles, functions
import numpy as np

# 退火用參數
T0 = 1 #初始退火溫度 (影響解的搜索範圍)
RATIO = 0.95 #收斂速度 (過快較可能找不到最佳解)

# 其他用參數
best_sol = 0
global_best = {'sol':0, 'list':[], 'iter':0}


def Update_Best_Sol(newV):
    global best_sol
    best_sol = newV


def Simulated_Annealing(n, type):
    global best_sol, global_best
    sumlist = [0] * varibles.ITER
    for i in range(varibles.RUNS):
        t = T0; one_iter_sol_list = []; j = 0
        # ------- Initialization 生成一組初始解 -------
        init_obj = functions.Generate_init(1, n) #隨機產生一組初始解
        init_sol = init_obj[0]['sol'] #計算當前解
        best_sol = init_sol; temp_sol = best_sol
        temp_list = init_obj[0]['list']
        # 迭代
        while j < varibles.ITER:
            # ------- Transition 生成鄰居解 -------
            new_obj = functions.Transition_by_Random(temp_list, n, type)
            # ------- Evaluation 評估 -------
            new_sol = new_obj['sol']
            if(new_sol > temp_sol): # 若優於先前解 → 則直接更新
                Update_Best_Sol(new_sol)
                temp_list = new_obj['list']
            # ------- Determination --- ----
            else: # 否 → 則進行退火
                Pa = math.exp( (new_sol - temp_sol) / t ) #由差值機算出的允許機率
                r = random.random() #一隨機機率
                if r < Pa: #if 隨機機率 < 允許機率 → 則取代
                    Update_Best_Sol(new_sol)
                    temp_list = new_obj['list']
                t *= RATIO #進行降溫
            # find 全域最佳解
            if best_sol > global_best['sol']:
                global_best["sol"] = best_sol
                global_best["list"] = temp_list
                global_best['iter'] = i

            one_iter_sol_list.append(best_sol) 
            temp_sol = best_sol
            j += 1
        sumlist = np.array(sumlist) + np.array(one_iter_sol_list) #算平均用
    sumlist = np.divide(sumlist, varibles.RUNS)

    return (sumlist, global_best) 


def HW3_main(draw):
    problem = 1
    if draw:
        while(1):
            print("=====================================================")
            print("for【One Max Problem】enter 1 \nfor【Deceptive Problem】enter 2 ")
            print("=====================================================")
            problem = int(input('please input: '))  
            if problem == 1 or problem == 2 : 
                break
    if problem == 1: #One Max Problem
        n = varibles.BIT_LEN
        type = 'One Max Problem'
    else: #Deceptive Problem 
        n = int(input('please input n : '))  
        type = 'Deceptive Problem'

    (result, global_best) = Simulated_Annealing(n, type)
    
    if(draw):
        print_content = [ "在第" + str(global_best['iter']) + "回時有最佳解:" + str(global_best['sol']) + "，\n內容為：" + str(global_best['list'])]

        functions.Draw(print_content,varibles.ALGO, problem, result, [])
    else: return result
