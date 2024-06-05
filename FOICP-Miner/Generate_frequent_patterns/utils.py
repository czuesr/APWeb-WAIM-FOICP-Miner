import re
import xlrd
import numpy
d_treshold = 10
min_prev = 0.1
S = []

def load_data_set(path):
    """加载数据集

    :param path: 数据集全路径
    :return: dataSet
    """
    sum_list = []
    temp_list = []
    workbook = xlrd.open_workbook(path)
    worksheet = workbook.sheet_by_name(u'Sheet')
    num_rows = worksheet.nrows
    num_cols = worksheet.ncols
    for i in range(num_rows):
        for j in range(num_cols):
            num = worksheet.cell_value(i, j)
            temp_list.append(num)
        sum_list.append(temp_list)
        temp_list = []
    return sum_list

def cal_distance(x1, y1, x2, y2):
    """计算两点之间的距离

    :param x1: x1坐标
    :param y1: y1坐标
    :param x2: x2坐标
    :param y2: y2坐标
    :return: distance between (x1,y1) and (x2,y2)
    """
    v1 = [x1, y1]
    v2 = [x2, y2]
    v1 = numpy.array(v1)
    v2 = numpy.array(v2)
    dist = numpy.sqrt(numpy.sum(numpy.square(v1 - v2)))
    return dist

def gen_star_neighbor(sum_list):
    ET = []
    CNT = {}
    SN = {}
    S = {}
    for i in range(len(sum_list)):
        feature1 = sum_list[i][1]  # 提取出英文
        id1 = str(int(sum_list[i][0]))  # 提取出数字
        # print('#####################################', feature + id)
        if feature1 not in ET:
            CNT[feature1] = 1  # 计算特征的实例数
            ET.append(feature1)
            S[feature1] = [id1]
        else:
            CNT[feature1] += 1
            S[feature1].append(id1)
        for j in range(i + 1, len(sum_list)):
            feature2 = sum_list[j][1]  # 提取出英文
            id2 = str(int(sum_list[j][0]))  # 提取出数字
            p1 = feature1 + id1
            p2 = feature2 + id2
            if feature1 != feature2:  # 如果特征不相同
                if cal_distance(sum_list[i][2], sum_list[i][3], sum_list[j][2], sum_list[j][3]) < d_treshold:
                    if p1 not in SN:
                        SN[p1] = [p2]
                    else:
                        SN[p1].append(p2)
                        SN[p1].sort()
            else:
                continue
    ET.sort()
    return ET, CNT, SN, S

def subset(featureSet, P):
    for i in featureSet:
        rlist = []
        for j in featureSet:
            if j != i:
                rlist.append(j)
        if rlist not in P:
            return 0
    return 1

def gen_candidate_co_location(P, k):  # 生成候选集,传入上一阶频繁
    candidate_list = []
    if (k == 2):
        for i in range(len(P)):
            for j in range(i + 1, len(P)):
                featureSet = []
                featureSet.append(P[i])
                featureSet.append(P[j])
                featureSet.sort()
                candidate_list.append(featureSet)
    else:
        for i in range(len(P)):
            for j in range(i + 1, len(P)):
                T1 = P[i][:k - 2]  # P[i][0]取出频繁特征集
                T2 = P[j][:k - 2]
                if T1 == T2:
                    featureSet = list(set(P[i]).union(set(P[j])))
                    featureSet.sort()
                    if subset(featureSet, P):
                        candidate_list.append(featureSet)  # 查看子集是否频繁
    return candidate_list

#[['A', 'B', 'D'], ['A', 'B', 'G'], ['A', 'B', 'H'], ['A', 'B', 'I'], ['A', 'D', 'G'], ['A', 'D', 'H']]
def get_star_instances(candidate_list, sn, k):
    star_instances = []
    for mode in candidate_list:  # 循环提出候选模式
        # get_FT(candidate,fsn)
        FT = FeatureID(sn, S, mode)  # 找出所有满足模式为mode的表实例FT
        if len(FT) != 0:
            star_instances.append((mode, FT))
    return star_instances

def FeatureID(SN, S, item):
    table = []  # 用来存放所有模式行实例的所有
    for id in S[item[0]]:  # 循环候选模式第一个特征的实例号，如B1,B2,B3
        ins = item[0] + id  # 形成B1,B2,B3
        if ins in SN:  # 如果该实例有星型邻居
            star = SN[ins]
            l = [ins]  # L用来存储该模式下分别特征的实例号集合（例如以B1开头的所有）
            dfs_res = []
            dfs_item(star, item, 1, l, dfs_res,SN)
        else:
            continue
        if (len(dfs_res) != 0):
            table.extend(dfs_res)
    return table

def dfs_item(star, item, x, inst: list, dfs_res,SN):
    if x == len(item):
        if check_clique_instance(inst, SN):
            dfs_res.append(inst)
        return
    for instance in star:  # 循环查找星型邻居中该特征的实例号
        feature = ''.join(re.findall(r'[A-Za-z]', instance))  # 提取出英文
        if (feature == item[x]):
            inst.append(instance)
            dfs_item(star, item, x + 1, inst.copy(), dfs_res,SN)
            inst = inst[:-1]
    return

def check_clique_instance(instance, SN: dict):
    if len(instance) < 3:
        return True
    for i in range(1,len(instance) - 1):
        temp = instance[i+1:]
        if instance[i] in SN.keys():
            if not set().issubset(set(SN[instance[i]])):
                #print(instance,'...',temp,'....',instance[i],'....',SN[instance[i]])
                #print(1)
                return False
        else:
            #print(2)
            return False
    return True

#FT:候选特征下的实例（邻居关系）[([A,B],[[A1,B1],[A2,B2]]]),([A,D],[[]])] (元组：代表不可改变)
def select_prevalent_co_locations(Ck,CNT):
    P = []
    for mode, instances in Ck:
        flag = True
        for i in range(len(mode)):
            PR_S = []#存放每个实例的贡献值 应该要比较实例相同的行实例之间的贡献度 一个类型的实例专属 换下一个特征的时候
            #要清零
            for instance in instances:#拿出[A1,B1,C1,D1]  [A1,B2,C1,D1] [A1,B3,C1,D1]
                p1 = i #p1是基准 是我们要求的那特征的实例
                PR_S.append(instance[p1])
            PR_S = list(set(PR_S))
            PR_num = len(PR_S) / CNT[mode[i]]
            if PR_num < min_prev:
                flag = False
        if flag:
            P.append(mode)
    return P