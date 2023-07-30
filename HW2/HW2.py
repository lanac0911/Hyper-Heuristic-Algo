#HW2 One-Max Problem with HillClimbling
import random, math
import matplotlib.pyplot as plt
import varibles, functions
import numpy as np

rl_best_sol = 0
rand_best_sol = 0
rl_temp_history = rand_temp_history= []
history = [[],[]]
RL_list = []
Rand_list = []


def Hill_Climbling():
    global RL_list, Rand_list, rl_best_sol, rand_best_sol
    # ------ 往左或往右 ------
    direction = random.randint(0, 1) # 0:left; 1:right
    rl_temp_list = RL_list.copy()
    if direction: #+1
        temp_dec = functions.BinaryList_to_Dec(rl_temp_list) + 1
    else: #-1
        temp_dec = functions.BinaryList_to_Dec(rl_temp_list) - 1
    #計算並取代
    rl_temp_list = functions.Dec_to_BinaryList(temp_dec)
    rl_temp_sol = functions.Count_Sol(rl_temp_list)
    if rl_temp_sol > rl_best_sol:
        RL_list = rl_temp_list #取代成新list
        rl_best_sol = rl_temp_sol #取代新成解

    # ------ 隨機翻轉 ------
    rand_temp_list = Rand_list.copy()
    position = random.randint(0, varibles.BIT_LEN - 1) #隨機更改的位置
    rand_temp_list[position] = int(not rand_temp_list[position]) #翻轉位元
    #計算解
    rand_temp_sol = functions.Count_Sol(rand_temp_list)
    if rand_temp_sol > rand_best_sol:
        Rand_list = rand_temp_list #取代成新list
        rand_best_sol = rand_temp_sol #取代新成解

    return [rl_best_sol, rand_best_sol]

def HW2_main(draw):
    global RL_list, Rand_list, rl_best_sol, rand_best_sol, history
    global rl_temp_history, rand_temp_history
    rl_total_best = 0 ; rand_total_best = 0 ; rl_best_run = 0 ; rand_best_run = 0
    rl_sum_list = rand_sum_list = [0] * varibles.ITER
    
    for i in range(varibles.RUNS):    
        rl_temp_history = [] ; rand_temp_history = [] #清空
        rand_best_run = 0; rl_best_sol = 0
        # ------ random一組解 ------
        init_obj = functions.Random_Sol(varibles.BIT_LEN) # [one_nums, zero_nums, random_list]
        rl_best_sol = init_obj['one_nums'] ; rand_best_sol = init_obj['one_nums']
        RL_list = init_obj['random_list'] ; Rand_list = RL_list.copy()

        j = 0
        while j < varibles.ITER:
            temp_best = Hill_Climbling()
            rl_temp_history.append(temp_best[0])
            rand_temp_history.append(temp_best[1])
            j += 1

        # ------ 取代＆做平均計算用 ------
        rl_sum_list = np.array(rl_sum_list) + np.array(rl_temp_history)
        rand_sum_list = np.array(rand_sum_list) + np.array(rand_temp_history)
        if temp_best[0] > rl_total_best:
            rl_total_best = temp_best[0]
            history[0] = rl_temp_history
            rl_best_run = i
        if temp_best[1] > rand_total_best:
            rand_total_best = temp_best[1]
            history[1] = rl_temp_history
            rand_best_run = i
    rl_sum_list = np.divide(rl_sum_list, varibles.RUNS)
    rand_sum_list = np.divide(rand_sum_list, varibles.RUNS)

    if(draw):
        print_content = [ 
            "【 往左/右走 】\n在第" + str(rl_best_run)  + "回有最佳解:"  + str(rl_total_best)  +  "，平均最佳解：" + str(math.floor(rl_sum_list[len(rl_sum_list)-1] * 100) / 100.0),
            "【 隨機左右移 】\n在第" + str(rand_best_run) + "回有最佳解:" + str(rand_total_best) + "，平均最佳解：" + str(math.floor(rand_sum_list[len(rand_sum_list)-1] * 100) / 100.0)
        ]
        speciallist = [rl_best_run, rl_total_best, rl_sum_list, rand_best_run, rand_total_best, rand_sum_list,]
        functions.Draw(print_content,varibles.ALGO, 1, [], speciallist)        
    else:
        return rand_sum_list
 