#HW4 One-Max Problem with Tabu Search
import matplotlib.pyplot as plt
import varibles, functions
import numpy as np

# 其他用參數
best_sol = 0
global_best = {'sol':0, 'list':[], 'iter':0}
TABU_LIST = []
TABU_MAX = 7

def If_in_TABU(TabuL, lst):
    exist = False
    for item in TabuL:
        if lst == item:
            exist = True
            break
    return exist

def Aspiration_Criteria(lst): #是否符合免禁原則 
    temp_tabu = TABU_LIST.copy()
    temp_tabu.pop(0)
    remit = If_in_TABU(temp_tabu, lst) #exist為T時，不赦免
    return (not remit)

def Quene_Oper(type, lst):
    global TABU_LIST
    space = len(TABU_LIST)
    if type == 'en':
        if space == 7:
            Quene_Oper('de',[])
        TABU_LIST.append(lst)
    elif type == 'de':
        if space > 0:
            TABU_LIST.pop(0)

def Update_Optaimal(new_best, new_best_list, runs):
    global best_sol, global_best
    #for sol
    Quene_Oper('de', []) #正式dequene
    best_sol = new_best #更新global optimal
    #for all
    global_best["sol"] = new_best
    global_best["list"] = new_best_list
    global_best['iter'] = runs


def TABU_Search(n, type):
    sumlist = [0] * varibles.ITER
    global best_sol, global_best, TABU_LIST
    for i in range(varibles.RUNS):
        one_iter_sol_list = []
        # ------- Initialization 生成一組初始解 -------
        init_obj = functions.Random_Sol(n) #隨機產生一組初始解
        init_sol = init_obj['one_nums'] #計算當前解
        best_sol = init_sol; temp_list = init_obj['random_list']
        j = 0
        # 迭代
        while j < varibles.ITER:
            # ------- Transition 生成鄰居解 -------
            new_obj = functions.Transition_by_Random(temp_list, n, type)
            # ----- 免禁原則 ------
            exist = If_in_TABU(TABU_LIST, new_obj['list'])
            # 若在禁忌名單裡
            if exist:
                remit = Aspiration_Criteria(new_obj['list']) # 是否符合免禁原則 which is “dequene 最舊紀錄後，如果不在名單裡即赦免"
                if remit:    # 被赦免 => 正式dequene、更新global optimal、再C
                    Quene_Oper('de', []) #正式dequene
                    Update_Optaimal(new_obj['sol'], new_obj['list'], i) #更新global optimal
                    temp_list = new_obj['list']
                    Quene_Oper('en', new_obj['list']) #enquene
                #扔在名單中 => 不更新，略過
            # 若不在禁忌名單裡 => check是否優於當前最佳解
            else: 
                if new_obj['sol'] > best_sol: # 是 => 更新global optimal，並enquene
                    Update_Optaimal(new_obj['sol'], new_obj['list'], i) #更新global optimal
                    temp_list = new_obj['list']
                    Quene_Oper('en', new_obj['list']) #enquene
                #否 => 不更新，略過
            # temp_list = new_obj['list']
            print("!!!!!!!,be",best_sol)
            one_iter_sol_list.append(best_sol) 
            j+=1
        print("one_iter_sol_list=",one_iter_sol_list)
        sumlist = np.array(sumlist) + np.array(one_iter_sol_list) #算平均用
        print("sumlist=",sumlist)
    sumlist = np.divide(sumlist, varibles.RUNS)
    print("after sumlist=",sumlist)
    return (sumlist, global_best) 


def HW4_main(draw):
    global best_sol
    if draw:
        while(1):
            print("=============================================")
            print("for【One Max Problem】enter 1 \nfor【Deceptive Problem】enter 2 ")
            print("=============================================")
            problem = int(input('please input: '))  
            if problem == 1 or problem == 2 : 
                break

    if problem == 1: #One Max Problem
        n = varibles.BIT_LEN
        type = 'One Max Problem'
    else: #Deceptive Problem 
        n = int(input('please input n : '))  
        type = 'Deceptive Problem'

    (result, global_best) = TABU_Search(n, type)
    if(draw):
        print_content = [ "在第" + str(global_best['iter']) + "回時有最佳解:" + str(global_best['sol']) + "，\n內容為："+ str(global_best['list'])]
        functions.Draw(print_content,varibles.ALGO, problem, result, [])
    else: return result