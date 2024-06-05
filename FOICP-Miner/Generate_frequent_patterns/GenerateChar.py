import random
import string


if __name__ == '__main__':
    a_str = string.ascii_uppercase
    a = a_str[0:14]
    print(a)
    cycleNum = 3000
    n = open('frequentData3.data', 'a+')
    i = 0
    while i < cycleNum:
        letters_list = []
        i = i + 1
        leng = random.randint(2, 14)  # 长度
        while len(letters_list) < leng:
            random_letter = random.choice(a)
            if (random_letter not in letters_list):
                letters_list.append(random_letter)
            else:
                pass
        # 将列表转换成元组输出
        letters_list.sort()

        n.write(str(letters_list) + '\n')
    n.close()


