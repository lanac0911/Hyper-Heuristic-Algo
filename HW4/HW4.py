#HW3 One-Max Problem with Simulated Annealing
import random, math
import matplotlib.pyplot as plt
import varibles, functions
import numpy as np

# 退火用參數
T0 = 1 #初始退火溫度 (影響解的搜索範圍)
RATIO = 0.95 #收斂速度 (過快較可能找不到最佳解)

# 其他用參數
best_sol = 0


def HW3_main():
    global best_sol
    sumlist = [0] * varibles.ITER
    