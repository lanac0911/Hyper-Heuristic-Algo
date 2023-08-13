import sys
import varibles
from HW1 import HW1
from HW2 import HW2
from HW3 import HW3
from HW4 import HW4
from HW5 import new2

def load_para(algo, runs, iter, bits):
    varibles.ALGO = algo
    varibles.RUNS = int(runs)
    varibles.ITER = int(iter)
    varibles.BIT_LEN = int(bits)
    if(algo != 'ES'):
        print(" "*4, "+=============================+")
        print(" "*6,"|   # Alogorithm:",varibles.ALGO, "\t|", 
            "\n", " "*5, "|   # Runs:", varibles.RUNS,  "\t\t|",
            "\n", " "*5, "|   # Iterations:", varibles.ITER,  "\t|",
            "\n", " "*5, "|   # Bit_Lengths:", varibles.BIT_LEN, "\t|"
        )
        print(" "*4,"+=============================+")
 


def which_algo(type):
    if(type == 'ES'):    
        HW1.HW1_main()
    elif(type == 'HC'):    
        HW2.HW2_main(draw=True)
    elif(type == 'SA'):
        HW3.HW3_main(draw=True)
    elif(type == 'TS'):
        HW4.HW4_main(draw=True)
    elif(type == 'GA'):
        new2.HW5_main(draw=True)

params = { 0:'HC' , 1: 51, 2: 1000, 3: 100 } #algo, runs, iters, bits
# params = { 0:'HC' , 1: 51, 2: 1000, 3: 100 } #algo, runs, iters, bits
if __name__ == '__main__':
    for i in range(2,6):
        if len(sys.argv) == i: 
            for j in range(i-1): 
                params[j] = sys.argv[j+1]
    
    # 載入參數
    load_para(params[0], params[1], params[2], params[3])
    varibles.initialize()
    which_algo(params[0])

