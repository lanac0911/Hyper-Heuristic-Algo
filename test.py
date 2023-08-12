# list1 = [0,1,0,1,0,1,0]
# list2 = [0,1,0,1,0,1,0]
# list3 = [1,1,1,0,0,1,0]
import numpy as np
# t = [[0,1,0,1,0,1,0], [0,1,0,1,0,1,0], [1,1,1,0,0,1,0]]
# print(len(t))

# for item in t:
#    print("item=", item) 
#    print(list1 == item)
# print("------   ")
# print(list1 == t[0])
# print(list1 == t[1])
# print(list1 == t[2])




# list = [[1,2,3,4,5,6,7],[0,0,0,0,0,0]]
# print(len(list))
             
#               # 是否符合免禁原則 which is “dequene 最舊紀錄後，如果不在名單裡即赦免"
#                 # 被赦免 => 正式dequene、更新global optimal、再enquene
                # 扔在名單中 => 不更新，略過
            # 若不在禁忌名單裡
              # 是否優於當前最佳解
                # 是 => 更新global optimal，並enquene
                # 否 => 不更新，略過
# params = { 0:'HC' , 1: 51, 2: 100, 3: 100 }
# for i in range(4):
#     print(params[i])

# ß

# li = [{'one_nums': 5, 'zero_nums': 5, 'random_list': [1, 1, 1, 0, 0, 0, 1, 1, 0, 0]}, {'one_nums': 2, 'zero_nums': 8, 'random_list': [0, 0, 0, 0, 1, 0, 0, 0, 0, 1]}, {'one_nums': 2, 'zero_nums': 8, 'random_list': [0, 0, 0, 1, 0, 0, 1, 0, 0, 0]}, {'one_nums': 0, 'zero_nums': 10, 'random_list': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}, {'one_nums': 3, 'zero_nums': 7, 'random_list': [1, 0, 1, 0, 1, 0, 0, 0, 0, 0]}, {'one_nums': 10, 'zero_nums': 0, 'random_list': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]}]
# print(li)
# print("====")
# print(li['random_list'])
# for   


l = [{'sol': 4, 'list': [1, 1, 0, 1, 0, 0]}, 
     {'sol': 5, 'list': [1, 0, 0, 1, 0, 0]}]
print(l[1]['list'][3])