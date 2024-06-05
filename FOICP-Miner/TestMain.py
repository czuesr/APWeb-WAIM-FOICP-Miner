#这个是用来转换A：为正常本体概念的作用
# This is a sample Python script.
import FOICPM
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import utils
from getOntology import *
from load_data import *
#countInter = 1 #记录第几次交互
minJaccard = 0.2 #记录最小的Jaccard距离
# Press the green button in the gutter to run the script.
def startMain():
#if __name__ == "__main__":
    lastInterDic = {} #保存每一次交互的结果
    dicOntology = getOntology().getOntology()
    datafile = "frequentData1.data"
    data = load_data(datafile).get_data()
    reNum = len(data)
    favList = []
    print('原data的长度',reNum)
    while len(data) != 0:
        maxList,maxDic = utils.GetMaximalConcepts(dicOntology,data)
        data.remove(maxList)
        recommendList = []  # 保存交互到界面上的模式 每一轮要清零
        recommendList.append(maxList)
        backRecommList = utils.recommendPatterns(dicOntology,data,maxDic)
        for tempitem in backRecommList:
            data.remove(list(tempitem))
            recommendList.append(tempitem)
       # print('第',countInter,'轮推荐交互的模式是',recommendList)

        dicResponse,recoDic = utils.connetInteractively(recommendList)
        dicResponse1 = {}
        #print(countInter)
        #print('第', countInter, '次交互的结果', dicResponse)
        for key,value in dicResponse.items():
            dicResponse1[tuple(recoDic[key])] = value
        #print(dicResponse1)
        lastInterDic,data = utils.FilterPatterns(data, dicResponse1, lastInterDic,dicOntology,minJaccard)

        for key1,value1 in lastInterDic.items():
            if value1 == 1:
                favList.append(list(key1))

        #print('第',countInter,'次交互后筛选出来的模式',lastInterDic) #这里之后改掉,拿掉0 不把所有的放进去
        #print('筛选后的data长度',len(data))
        #countInter = countInter + 1
    #while len(data) != 0:
        #print()
    return favList
    #print('最后的dic长度是否与data长度相同，保证每个模式都已经打标签了',reNum == len(lastInterDic))

