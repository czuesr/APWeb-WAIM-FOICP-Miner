import utils
import time
start=time.time()
sum_list = utils.load_data_set(r"data2.xlsx")
ET, CNT, SN, S = utils.gen_star_neighbor(sum_list)
utils.S = S
P = ET
k = 2

Prevenlence_P = {}
while (len(P) > 0):
    candidate_list = utils.gen_candidate_co_location(P, k)  # k阶候选co-location模式
    Ck = utils.get_star_instances(candidate_list, SN, k)
    P = utils.select_prevalent_co_locations(Ck, CNT)
    Prevenlence_P[k] = P
    k += 1
end=time.time()
print('Running time: %s Seconds'%(end-start))
print(CNT)
n = open('frequentData1.data','a+')
for key,value in Prevenlence_P.items():
    if len(value)!=0:
        print(key,'阶频繁模式：',value,'数量：',len(value))
        for i in value:
            n.write(str(i)+'\n')
n.close()


