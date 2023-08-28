
#HW6 Ackley Function with Particle Swarm Optimiaztion 
import random, math
import varibles, functions
import numpy as np
from scipy.spatial import distance
import matplotlib.pyplot as plt


PARTICLE_NUMS = 50
DIMENSION = 3
SPACE_MAX = 30
SPEED_MAX = 1
C1 = 2
C2 = 2
Omega = 0.5

def Update_Optaimal(list, pos, sol, iter):
    list["sol"] = sol
    list["list"] = pos
    list['iter'] = iter

def Ackley_Func(coords, a = 20, b = 0.2, c = 2 * np.pi):
    x, y, z = coords
    term1 = -a * np.exp(-b * np.sqrt((x**2 + y**2 + z**2) / 3))
    term2 = -np.exp((np.cos(c*x) + np.cos(c*y) + np.cos(c*z)) / 3)
    return term1 + term2 + a + np.exp(1)

def If_Better(current_best, now_val):
    if now_val < current_best: return True
    else: return False


def  Particle_Swarm_Optimiaztion():
    sum_list = np.zeros(varibles.ITER)
    global_best = {'sol': None, 'list': [], 'iter':0}
    for _ in range(varibles.RUNS):
        # ------- Initialize -------
        # 初始化
        p_positions = np.random.uniform(-SPACE_MAX, SPACE_MAX, (PARTICLE_NUMS, DIMENSION)) # 每個(粒子)的位置 [粒子數＊維度]
        p_solutions = list(map(Ackley_Func, p_positions)) # 每一組(粒子)的解 [粒子數]
        p_speeds = np.random.uniform(-SPEED_MAX, SPEED_MAX, (PARTICLE_NUMS, DIMENSION)) # 初始化每一組(粒子)的速度  [粒子數＊維度]
        # personal
        pb_positions = p_positions.copy() # 設定為最初的最佳解(位置) [粒子數＊維度]
        pb_solutions = p_solutions.copy() # 設定為最初的最佳解 [粒子數]
        # global
        gb_solution = min(p_solutions) # 目前的最佳解
        gb_position = p_positions[np.argmin(p_solutions)] # 目前最佳解的位置
        #
        one_iter_sol = []
        # ------- Calulate & Updat ------- 
        for iter in range(varibles.ITER):
            # 1. 計算每個粒子的fitness
            for i in range(PARTICLE_NUMS):
                # calulate/update speed
                r1 = random.random(); r2 = random.random()
                p_speeds[i] = Omega * p_speeds[i] +\
                            C1 * r1 * (pb_positions[i]- p_positions[i]) +\
                            C2 * r2 * (gb_position - p_positions[i])
                # 2. update position
                p_positions[i] = p_positions[i] + p_speeds[i]
                # 3. update fitness
                fitness = Ackley_Func(p_positions[i])
                # 4. compare
                if If_Better(pb_solutions[i], fitness): # personal (pb)
                    pb_positions[i] = p_positions[i] # 更新位置
                    pb_solutions[i] = fitness # 更新位置解
                    if If_Better(gb_solution, fitness):  # global (gb)
                        gb_position = p_positions[i]
                        gb_solution = fitness
                        Update_Optaimal(global_best, gb_position, gb_solution, iter)

            one_iter_sol.append(gb_solution)
        sum_list =  np.array(sum_list) + np.array(one_iter_sol)
    sum_list = np.divide(sum_list, varibles.RUNS)
    return(sum_list, global_best)
    


def HW7_main(draw):
    result = []
    (result, global_best) =  Particle_Swarm_Optimiaztion()
    if(draw):
        print_content = [ "在第" + str(global_best['iter']) + " 次遞迴時有最佳解:" + 
                         str(global_best['sol']) + "，\n內容為："+ 
                         str(global_best['list'])
                        ]
        functions.Draw(print_content,varibles.ALGO, 1, result, [PARTICLE_NUMS])
        #
    else: return result
    


