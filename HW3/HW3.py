#HW3 One-Max Problem with Simulated Annealing
import random, math
import matplotlib.pyplot as plt
import varibles, functions
import numpy as np
from HW2 import HW2

# 退火用參數
T0 = 1 #初始退火溫度 (影響解的搜索範圍)
RATIO = 0.95 #收斂速度 (過快較可能找不到最佳解)

# 其他用參數
best_sol = 0
global_best = {'sol':0, 'list':[], 'iter':0}
content = '⎨ Deceptive Function Def. ⎬\n   ( n = 4 for example) \n---------------------------\n'
funct = '  f(0000) = 5   * optimal\n  f(0001) = 1\n  f(0010) = 1\n  f(0011) = 2\n.\n.\n.\n  f(1100) = 2\n  f(1101) = 3\n  f(1110) = 3\n  f(1111) = 4\n'


def Update_Best_Sol(newV):
    global best_sol
    best_sol = newV

def Transition_by_Random(list, n, type):
    # ------ 隨機翻轉 ------
    new_list = list.copy()
    position = random.randint(0, n - 1) #隨機更改的位置
    new_list[position] = int(not new_list[position]) #翻轉位元
    if type == 'Deceptive Problem':
        new_sol = functions.Trap_Func(new_list) # 計算新解
    else:
        new_sol = functions.Count_Sol(new_list) # 計算新解

    # ------ 往左或往右 ------
    # direction = random.randint(0, 1) # 0:left; 1:right
    # new_list = list.copy()
    # if direction: #+1
    #     temp_dec = functions.BinaryList_to_Dec(new_list) + 1
    # else: #-1
    #     temp_dec = functions.BinaryList_to_Dec(new_list) - 1
    # #計算並取代
    # new_list = functions.Dec_to_BinaryList(temp_dec)
    # new_sol = functions.Count_Sol(new_list)

    d = dict()
    d['sol'] = new_sol
    d['list'] = new_list
    return d


def Simulated_Annealing(n, type):
    global best_sol, global_best, global_best_list
    sumlist = [0] * varibles.ITER
    for i in range(varibles.RUNS):
        t = T0
        one_iter_sol_list = []
        # ------- Initialization 生成一組初始解 -------
        init_obj = functions.Random_Sol(n) #隨機產生一組初始解
        init_sol = functions.Count_Sol(init_obj['random_list']) #計算當前解
        best_sol = init_sol; temp_sol = best_sol
        temp_list = init_obj['random_list']
        j = 0
        # 迭代
        while j < varibles.ITER:
            # ------- Transition 生成鄰居解 -------
            new_obj = Transition_by_Random(temp_list, n, type)
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

def Draw(problem, result, global_best):

    # ------ 印出結果 ------
    print("⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯")
    print("在第", global_best['iter'], "回時有最佳解:",global_best['sol'], "，\n內容為：", global_best['list'])
    print("⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯")


    title = 'Deceptive Problem'
    if problem == 1: #oneMax
        HC_result = HW2.HW2_main(draw=False)
        plt.plot(HC_result, color='g', label="HC avg")
        title = 'One Max Problem'
    if problem == 2: #deceptive
        y_top = result[len(result)-1]; y_bottom = result[0]
        distance = ((y_top - y_bottom) / 5) 
        y = y_bottom + distance
        plt.annotate(
            (content+funct),
            xy=(int(varibles.ITER / 2),y ),
            bbox={
                'boxstyle':'round',
                'facecolor':'#d9d2d9',
                'edgecolor':'#4d494d',
                'linewidth':2
            }
        )
    # ------ 畫圖用 ------
    #plt1
    plt.plot(result, color='b', label="SA avg")
    plt.xlabel('Iterations', fontsize="10") 
    plt.ylabel('Fitness', fontsize="10") 
    plt.title(title, fontsize="18") 
    plt.legend()
    plt.show()


def HW3_main():
    while(1):
        print("===============================================================")
        print("for【One Max Problem】enter 1 \nfor【Deceptive Problem】enter 2 ")
        print("===============================================================")
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
  
    Draw(problem, result, global_best)

