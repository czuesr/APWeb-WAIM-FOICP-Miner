
class load_data():
    def __init__(self, filename):
        self.filename = filename
    def get_data(self):
        f = open(self.filename, 'r+', encoding='utf-8-sig')
        a = []
        for line in f.readlines():
            line = line.replace('\n', '')
            line = line.replace("'", '')
            line = line.replace(" ", "")
            res = line.strip('[')
            res = res.strip(']')
            res = res.split(',')
            a.append(res)
        #print(a)
        return(a)
