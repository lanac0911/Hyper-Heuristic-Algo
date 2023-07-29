import random

# ------- SHARE -------
# 初始一組解(one max problem)
def Random_Sol(n):
    one_nums = random.randint(0, n) #random “1” 的數量
    zero_nums = n - one_nums # 計算出 "0" 的數量
    list = [0] * zero_nums + [1] * one_nums # 組成list
    random_list = random.sample(list, len(list)) # 打亂list
    d = dict()
    d['one_nums'] = one_nums
    d['zero_nums'] = zero_nums
    d['random_list'] = random_list

    return d

# ------- HW2 -------
def Dec_to_BinaryList(num):
    return [i for i in bin(num)[2:]]

def BinaryList_to_Dec(list):
    temp_str = ''.join(map(str,list))
    return int(temp_str,2)

def Count_Sol(list):
    cnt = 0
    for bit in iter(list): #計算和
        if bit == 1 : cnt += 1
    return cnt

# ------- HW3 -------
def Trap_Func(list):
    cnt = 0
    for bit in iter(list): #計算和
        if bit == 1 : cnt += 1
    if cnt == 0:
        cnt = len(list) + 1
    return cnt
