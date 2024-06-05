from tkinter import *
import tkinter
OntologyToChar = {'A':"Hotel",'B':"Hostel",'C':"Airport",'D':"Railway_Station",'E':"Car_Parks",'F':"Park",'G':"Gymnasium",'H':"Bubble_tea_shop",
            'I':"Clothes_Shop",'J':"Animal_Shop",'K':"National_Scenic_spots",'L':"Provincial_Scenic_spots",'M':"Chinese_Restaurant",'N':"Western_Restaurant"}


#def recommandMaxPatterns(patterns,owl):#patterns代表的是频繁的模式，owl是本体描述文件

    #return
K = 5 #定义每一轮的返回给用户交互的模式数目

def GetMaximalConcepts(ontology,cc):
    maxlist = []
    maxNum = 0
    maxDic = {}
    for tempPatterns in cc:
        tempDic = {}
        for item in tempPatterns:
            leaf_ontology_Concept = OntologyToChar[item] #拿出Chinese_Food之类的叶概念出来
            tempDic = Merge(get_keys(ontology,leaf_ontology_Concept),tempDic)
        #{'Traffic': 1.0, 'Food_and_Beverage': 1.0} {'Shopping': 1.0, 'Food_and_Beverage': 1.0} {'Shopping': 1.0, 'Food_and_Beverage': 1.0} tempDic里面是每个频繁模式
        #的父概念带上隶属度
        sumNum = 0
        for key,value in tempDic.items():
            sumNum = sumNum + value
        if sumNum > maxNum:
            maxlist = tempPatterns
            maxDic = tempDic
            maxNum = sumNum

        #在度数相同的情况下，去判断含的信息个数
        elif sumNum == maxNum:
            if len(tempDic) > len(maxDic):
                maxlist = tempPatterns
                maxDic = tempDic
        #print(tempPatterns,'对应的概念及其隶属度：',tempDic)
    #print('此时最大的模式是',maxlist)
    return maxlist,maxDic


#用来 获取对应的上层的概念 每次传入叶子结点，我们要获取具有叶子结点的上层结点及隶属度 d传入的是本体的概念 return 父概念：隶属度
def get_keys(d,element):
    TopDic = {}
    for outkey, outvalue in d.items():
        for inkey in outvalue.keys():
            if inkey == element:
                TopDic[outkey] = outvalue[inkey]
    return TopDic

#融合字典 dic2是最外层的dic储存每个模式的本体上层信息，dic1是要融合进去的
def Merge(dict1, dict2):
    res = {}
    for tKey, tValue in dict1.items():
        if tKey not in dict2:
            res = {**dict1, **dict2}
        else:
            res = dict2
            for sKey,sValue in dict2.items():
                if sKey == tKey:
                    res[sKey] = max(sValue, tValue)

    return res

def recommendPatterns(ontology,cc,comDic):
    jacarrd_dic = {}
    result = [] #存放前k个
    for tempPatterns in cc:
        tempDic = {}
        updateMinDic = {}
        updateMaxDic = {}
        for item in tempPatterns:
            leaf_ontology_Concept = OntologyToChar[item]  # 拿出Chinese_Food之类的叶概念出来
            tempDic = Merge(get_keys(ontology, leaf_ontology_Concept), tempDic)#每一个模式对应的父概念及其隶属度
        interList = intersectionOntology(comDic,tempDic)
        unionList = unionsectionOntology(comDic,tempDic)
        for index in interList:
            updateMinDic[index] = min(tempDic[index],comDic[index])
        for index in unionList:
            if index in tempDic and index in comDic:
                updateMaxDic[index] = max(tempDic[index],comDic[index])
            elif index in tempDic:
                updateMaxDic[index] = tempDic[index]
            else:
                updateMaxDic[index] = comDic[index]
        #print('更新的并集及更新的隶属度',updateMaxDic)
        #print('更新的交集及更新的隶属度',updateMinDic)
        numInter = 0
        numUnion = 0
        for value in updateMaxDic.values():
            numUnion = numUnion+value
        for value in updateMinDic.values():
            numInter = numInter+value
        jacarrd_distance = 1-numInter/numUnion
        #print('jaccard距离为：',jacarrd_distance)
        jacarrd_dic[tuple(tempPatterns)] = jacarrd_distance
    #print(jacarrd_dic)
    return getTopK(jacarrd_dic)


def getTopK(dict_):
    keys = list(dict_.keys())
    for key_i in range(len(keys)):
        for key_j in range(key_i+1, len(keys)):
            if dict_[keys[key_i]] < dict_[keys[key_j]]:
                temp = keys[key_i]
                keys[key_i] = keys[key_j]
                keys[key_j] = temp

    resu_ = []
    for i in range(K):
        if len(keys) > i:
            resu_.append(keys[i])
    return resu_


#对俩个字典序进行取交集 返回[list类型]
def intersectionOntology(DicA,DicB):
    setA = set(DicA)
    setB = set(DicB)
    return list(setA.intersection(setB))


def unionsectionOntology(DicA,DicB):
    setA = set(DicA)
    setB = set(DicB)
    return list(setA.union(setB))

def connetInteractively(recommendList):
    dicTest = {}
    def send():
        x = ""
        for j in cheakboxs:
            # 这里实际上是cheakboxs[j].get() == True
            # 如果被勾选的话传回来的值为True
            # 如果没有被勾选的话传回来的值为False
            #patterns[j]代表的是
            if cheakboxs[j].get():
                dicTest[tuple(patterns[j])] = 1
            else:
                dicTest[tuple(patterns[j])] = 0
    # 创建主窗口
    root = tkinter.Tk()
    root.title("Selecting")
    label = tkinter.Label(root, text="If you are interested in any one of the patterns below,just check it!", bg="lightyellow", fg="red", width=55)
    label.grid(row=0)

    index = 0
    patterns = {}
    recommendList2 = []
    recoDic = {}
    for item in recommendList:
        ttlist = []
        for i in item:
            ttlist.append(OntologyToChar[i])
        recommendList2.append(ttlist)
        recoDic[tuple(ttlist)] = item
    for item in recommendList2:
        patterns[index] = item
        index = index+1
    # 这里负责给予字典的键一个False或者True的值，用于检测是否被勾选
    cheakboxs = {}
    #print('测试',patterns)
    for i in range(len(patterns)):
        # 这里相当于是{0: ABC, 1: ABD, 2: BC, 3: CG, 4: FH}
        cheakboxs[i] = tkinter.BooleanVar()
        # 只有被勾选才变为True
        tkinter.Checkbutton(root, text=patterns[i], variable=cheakboxs[i]).grid(row=i + 1, sticky=tkinter.W)

    buttonOne = tkinter.Button(root, text="Submit", width=10, command=send)
    buttonOne.grid(row=len(patterns) + 1)
    #buttonTwo = tkinter.Button(root, text="Exit", width=10, command=quit)
    #buttonTwo.grid(row=len(patterns) + 2)
    root.mainloop()
    return dicTest,recoDic

def FilterPatterns(data,dic,lastDic,ontology,min_jac):
    for key,value in dic.items():
        lastDic[key] = value
        for tempI in data:
            if computJaccrd(list(key),tempI,ontology) < min_jac:
                lastDic[tuple(tempI)] = value
                data.remove(tempI)
    return lastDic,data



def computJaccrd(list1,list2,ontology):
    list1Dic = {}
    list2Dic = {}
    updateMinDic = {}
    updateMaxDic = {}
    for i in list1:
        leaf_ontology_Concept = OntologyToChar[i]  # 拿出Chinese_Food之类的叶概念出来
        list1Dic = Merge(get_keys(ontology, leaf_ontology_Concept), list1Dic)
    for i in list2:
        leaf_ontology_Concept = OntologyToChar[i]  # 拿出Chinese_Food之类的叶概念出来
        list2Dic = Merge(get_keys(ontology, leaf_ontology_Concept), list2Dic)
    interList = intersectionOntology(list1Dic, list2Dic)
    unionList = unionsectionOntology(list1Dic, list2Dic)
    for index in interList:
        updateMinDic[index] = min(list1Dic[index], list2Dic[index])
    for index in unionList:
        if index in list1Dic and index in list2Dic:
            updateMaxDic[index] = max(list1Dic[index], list2Dic[index])
        elif index in list1Dic:
            updateMaxDic[index] = list1Dic[index]
        else:
            updateMaxDic[index] = list2Dic[index]
    numInter = 0
    numUnion = 0
    for value in updateMaxDic.values():
        numUnion = numUnion + value
    for value in updateMinDic.values():
        numInter = numInter + value
    if numUnion == 0:
        for i in list1:
            leaf_ontology_Concept = OntologyToChar[i]  # 拿出Chinese_Food之类的叶概念出来\
            print(leaf_ontology_Concept)
            print(get_keys(ontology, leaf_ontology_Concept))
            list1Dic = Merge(get_keys(ontology, leaf_ontology_Concept), list1Dic)
        for i in list2:
            leaf_ontology_Concept = OntologyToChar[i]  # 拿出Chinese_Food之类的叶概念出来
            list2Dic = Merge(get_keys(ontology, leaf_ontology_Concept), list2Dic)

    jacarrd_distance = 1 - numInter / numUnion
    return jacarrd_distance