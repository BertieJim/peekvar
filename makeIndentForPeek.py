
import re
import os

class Stack(object):

    def __init__(self):
     # 创建空列表实现栈
        self.__list = []

    def is_empty(self):
    # 判断是否为空
        return self.__list == []
    def push(self,item):
    # 压栈，添加元素
        self.__list.append(item)

    def pop(self):
    # 弹栈，弹出最后压入栈的元素
        if self.is_empty():
            return
        else:
            return self.__list.pop()

    def top(self):
    # 取最后压入栈的元素
        if self.is_empty():
            return
        else:
            return self.__list[-1]


def main():
    # filename = "usinguse32api_relay.log"
    filename = "new_test_cert3.log"
    f = open('../crypt32/tests/' + filename)
    f_o = open('../crypt32/tests/recon_'+filename,'w')
    lines = f.readlines()
    times = 0
    indent = '    '
    bigger = []
    p = re.compile('_RET_(.*)\(\)')
    p2 = re.compile('_CALL_(.*)\(\)')
    linenum = 0



    for line in lines:
        outputline = line.split(' ')[1]
        linenum += 1
        if "CALL" in line:
            f_o.write(indent*times+outputline)
            # print(line)
            # pause = input()
            times += 1
            try:
                thisone = line.split(' ')[1].split('_')[2].split(".")[1].strip().lower()
                # thisone = (str(p2.findall(line)[0]).strip().split('.')[0].lower() )

            except IndexError:
                print(line)
                pause = input()
            if thisone in bigger:
                print('-------find it!!!!!'+line)
                print(linenum)
                # pause = input()

            bigger.append(thisone)
            print(bigger)

        elif "RET" in line:
            times -= 1
            # print(line)
            # pause = input()

            # thisdll =  (str(p.findall(line)[0]).strip().split('.')[0].lower() )
            thisone = line.split(' ')[1].split('_')[2].split(".")[1].strip().lower()
            bigger.pop()
            f_o.write(indent*times + outputline)

    f.close()
    f_o.close()
if __name__ == '__main__':
    main()
    # checkDllInvoke()
    #p = "2323 _CALL_c.a_(2,2)\n2323 _CALL_c.b_(2,2)\n2323 _RET_c.b_(2,2)\n2323 _RET_c.a_(2,2)\n"
