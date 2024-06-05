import json


class getOntology():
    def __init__(self, filename='FuzzyOntology.json'):
        self.filename = filename

    def getOntology(self):
        with open(self.filename) as f:
            data = json.load(f)
        DT = dict()  # a = [type,sonconcept1,……]
        for key in data:
            data = data[key]     #删除首个点的信息 拿出 {type:{type:{'memebershipvalue':int# }}}

        for key in data:
            tempDic = {}#遍历第二个点开始的信息
            for inKey in data[key]:
                tempDic[inKey] = data[key][inKey]['membershipvalue']
            data[key] = tempDic
        #print(data)
        DT = data
        return (DT)
