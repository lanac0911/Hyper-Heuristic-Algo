import random
import functions, varibles
import matplotlib.pyplot as plt
from HW2 import HW2
from HW3 import HW3
from HW4 import HW4
import numpy as np

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

def Random_Sol_Simple(n):
    one_nums = random.randint(0, n) #random “1” 的數量
    zero_nums = n - one_nums # 計算出 "0" 的數量
    list = [0] * zero_nums + [1] * one_nums # 組成list
    random_list = random.sample(list, len(list)) # 打亂list
    d = dict()
    d['sol'] = one_nums
    d['list'] = random_list
    return d

# 生成鄰居解
def Transition_by_Random(list, n, type):
    # ------ 隨機翻轉 ------
    new_list = list.copy()
    position = random.randint(0, n - 1) #隨機更改的位置
    new_list[position] = int(not new_list[position]) #翻轉位元
    if type == 'Deceptive Problem':
        new_sol = functions.Trap_Func(new_list) # 計算新解
    else:
        new_sol = functions.Count_Sol(new_list) # 計算新解

    d = dict()
    d['sol'] = new_sol
    d['list'] = new_list
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

# ------- HW5 -------
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

def biggest(obj):
    sort_list = sorted(obj, key=lambda d: d['sol'], reverse=True) 
    return sort_list[0]

def Update_Optaimal(list):
    d = dict()
    d['sol'] = functions.Count_Sol(list)
    d['list'] = list
    return d

def generate_popu(size,len):
    popu_list = []
    for _ in range(size):
        chrom_list = []
        chrom_list = np.random.randint(0,2,len)
        chrom_sol = functions.Count_Sol(chrom_list)
        d = dict(); d['list'] = chrom_list.tolist(); d['sol'] = chrom_sol
        popu_list.append(d)
    return popu_list

#######################
content = '⎨ Deceptive Function Def. ⎬\n   ( n = 4 for example) \n---------------------------\n'
funct = '  f(0000) = 5   * optimal\n  f(0001) = 1\n  f(0010) = 1\n  f(0011) = 2\n.\n.\n.\n  f(1100) = 2\n  f(1101) = 3\n  f(1110) = 3\n  f(1111) = 4\n'


# ------ 印出結果 ------
def Print_Info(content):
    if(len(content) == 1):
        print("⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯")
        for i in range(len(content)):
            print(content[i])
        print("⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯")
    else:
        print("⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯")
        for i in range(len(content)):
            print("⎯⎯⎯⎯⎯⎯")
            print(' '.join(content[i]))
            print("⎯⎯⎯⎯⎯⎯")
        print("⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯")

# ------- 畫圖 -------
def Draw(print_content, algo, problem, result, special_result):
    Print_Info(print_content)
    if algo == 'HC':
        #plt1
        plt.subplot(2, 2, 1)
        plt.plot(special_result[2], color='g')
        plt.title("Right or Left")
        #plt2
        plt.subplot(2,2,2)
        plt.plot(special_result[5], color='b')
        plt.title("Random")

        plt.xlabel('iterations')
        plt.suptitle("Hill Climbling")    
        #plt3
        ax1 = plt.subplot(2, 1, 2)
        ax1.plot(special_result[2], c='g')
        ax1.set_xlabel("Iteration")
        ax1.set_ylabel("Right or Left", color='g')
        plt.setp(ax1.get_yticklabels(), color='g') 

        ax2 = ax1.twinx()
        ax2.plot(special_result[5], color='b' )
        ax2.set_ylabel("Random", color='b')
        ax2.tick_params('y', color='b')
        plt.setp(ax2.get_yticklabels(), color='b')         
    else:    
        title = 'One Max Problem'
        if problem == 1: #oneMax
            HC_result = HW2.HW2_main(draw=False)
            if algo == 'SA': #畫HC+SA(本身)
                plt.plot(HC_result, 'b:', label="HC avg")
            elif algo == 'TS': #畫HC+SA+TB(本身)
                SA_result =  HW3.HW3_main(draw=False)
                plt.plot(HC_result, 'b:', label="HC avg")
                plt.plot(SA_result, 'g--', label='SA avg')
            elif algo == 'GA': #畫HC+SA+TB+GA(本身)
                TS_result_t = result[0]
                TS_result_w = result[1]
                plt.plot(TS_result_t, 'b:', label='GA - Tournament avg')
                plt.plot(TS_result_w, 'g--', label='GA - Roulette Wheel avg')
        if problem == 2: #deceptive
            title = 'Deceptive Problem'
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
        if algo != 'GA':
            plt.plot(result, color='r', label='{0} avg'.format(varibles.ALGO)) #(本身)
            plt.xlabel('Iterations', fontsize="10") 
    plt.ylabel('Fitness', fontsize="10") 
    plt.title(title, fontsize="18") 
    plt.legend()
    plt.show()
