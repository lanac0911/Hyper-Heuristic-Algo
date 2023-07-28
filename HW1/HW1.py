#HW1 One-Max Problem
import time, math
import itertools
import threading
import matplotlib.pyplot as plt


BIT_LEN = 100 #100bits
SEARCH_TIME = 30 #單位：分鐘
PRINT_TIME = 0.5 #隔多久印當前解（單位：分鐘）
end = False
best_sol = 0 #最佳解
history = [[],[]]

def cal_optimal():
    global best_sol
    global end 
    for cartesain_product in itertools.product([0,1], repeat=BIT_LEN):
        if(not end): #觀察時間未到
            temp_cnt = 0 
            for bit in cartesain_product: #計算笛卡爾積的和
                if bit != 0 : temp_cnt += 1
            if temp_cnt > best_sol: best_sol = temp_cnt#取代最佳解
        else:
            break

def print_now_optimal():
    global start
    global end 
    passt = int(math.floor(time.time() - start)) #已經過時間
    print("Time =",int(passt / 60),"分鐘\nOptimal Solution =",best_sol)
    print('---------------')
    #畫圖用
    history[0].append(int(math.floor(time.time() - start) / 60))
    history[1].append(best_sol)
    #時間到→結束
    if passt >= (SEARCH_TIME * 60) : 
        end = True
        return
    #定時執行檢查時間＆print資訊 (以thread方式)
    t1 = threading.Timer((PRINT_TIME * 60),print_now_optimal)
    t1.start()


# if __name__ == '__main__':
start = time.time() #開始算時間
def HW1_main():
    print_now_optimal() #定時執行檢查時間＆print資訊
    
    #以thread方式執行計算和（最佳解）
    t2 = threading.Timer(0,cal_optimal)
    t2.start()
    t2.join()
    
    #畫圖用
    plt.xlabel('time')
    plt.ylabel('optimal_sol')
    plt.plot(history[0], history[1])       
    plt.show()
