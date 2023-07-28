import sys
import varibles
from HW1 import HW1
from HW2 import HW2
from HW3 import HW3
from HW4 import HW4

def load_para(algo, runs, iter, bits):
    varibles.ALGO = algo
    varibles.RUNS = int(runs)
    varibles.ITER = int(iter)
    varibles.BIT_LEN = int(bits)
    print("===============================================================")
    print("Alogorithm:",varibles.ALGO, 
          " ⎮ Runs:", varibles.RUNS, 
          " ⎮ Iterations:", varibles.ITER, 
          " ⎮ Bit_Lengths:", varibles.BIT_LEN)
    print("===============================================================")

def which_algo(type):
    if(type == 'ES'):    
        HW1.HW1_main()
    elif(type == 'HC'):    
        HW2.HW2_main(draw=True)
    elif(type == 'SA'):
        HW3.HW3_main()
    elif(type == 'TABU'):
        HW4.HW4_main()


if __name__ == '__main__':
    # 沒有輸入初始參數
    if(len(sys.argv) <= 2):
        default_RUNS = 51   
        default_ITER = 1000
        default_BIT_LEN = 100
    else:
        default_RUNS = sys.argv[2]
        default_ITER = sys.argv[3]
        default_BIT_LEN = sys.argv[4]
    # 沒有輸入演算法
    select = None
    if(len(sys.argv) == 1):
        while(not select):
            print("Please Chose a Algorithm，Selections：'HC'、'SA'")
            select = input("please input:")
    else:
        select = sys.argv[1]
    
    # 載入參數
    load_para(select,default_RUNS, default_ITER, default_BIT_LEN)
    varibles.initialize()
    which_algo(select)

