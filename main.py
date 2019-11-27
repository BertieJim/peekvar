import copy
import os
import re


TYPE_TO_TYPE ={
    "str":"%d",
    "ptr":"%p",
    "long":"%d",
    "wstr":"%s"
}

def getDirFiles(dir):
    '''
    :param dir: input relative or full path
    :return: all file path
    '''
    files_ = []
    list = os.listdir(dir)

    for i in range(0, len(list)):

        path = os.path.join(dir, list[i])
        if os.path.isdir(path):
            files_.extend(getDirFiles(path))
        if os.path.isfile(path):
            files_.append(path)
    return files_

def pickUsefulFiles(dir):
    '''
    :param dir: dir like ../crypt32_bac
    :return: filename without path
    '''
    allFiles = getDirFiles(dir)
    specfile = []
    cfile = []
    for i in allFiles:

        suffix = os.path.splitext(i)[1]
        if suffix == '.spec':
            specfile.append(os.path.split(i)[-1])
        elif suffix == '.c':
            cfile.append(os.path.split(i)[-1])

    return cfile,specfile

def getFuncName(prefix,specfile):
    allfuncs = {}

    for i in specfile:
        f = open(os.path.join(prefix,i))
        alllines = f.readlines()
        for line in alllines:
            sec = line.split(" ")
            if sec[1].lower() == 'stdcall':
                p = re.compile('\(([^\)]+)\)')
                try:
                    type = p.findall(line)[0].split(' ')
                except IndexError:
                    allfuncs[sec[2].split("(")[0]] = [0, 0,'null',[],'VOID']
                    continue
                allfuncs[sec[2].split("(")[0]] = [0,0,'null',type,"VOID"]
    return allfuncs

def insertContentRet(all_funcs,func_name,var_name):
    var_list = "str,str"


    var_list += ','+ all_funcs[func_name][4]

    var_name_list = ","+var_name
    new_line = "    "+"VARPEEK(\"(" + \
               var_list + ")\\n\",\"RET\",\""+func_name+"\""+var_name_list +");\n"
    return new_line

def insertContentVar(all_funcs,func_name,var_name):
    var_list = "str"

    for var in all_funcs[func_name][3]:
        var_list += ','+ var

    var_name_list = str()
    for i in var_name:
        var_name_list += ","+str(i)
    new_line = "    "+"VARPEEK(\"(" + \
               var_list + ")\\n\",\"CALL\",\""+func_name+"\""+var_name_list +");\n"
    return new_line

def addNewChannel(old_prefix,new_prefix,all_funcs, file_name):
    '''
    :param all_funcs: spec name with reference number
    :param file_name: relative path
    :return:
    '''
    f_old = open(os.path.join(old_prefix,file_name))
    f_new = open(os.path.join(new_prefix , file_name),'w')
    '''
    for compatible
    '''
    print(file_name)
    func_location = []
    page = 0

    lines = f_old.readlines()
    for line in lines:
        p = re.compile('WINAPI\s([a-zA-Z0-9_]+)')
        func = p.findall(line)
        if func!=[]:
            func = func[0]
            try:
                '''
                first ,the func is in the file
                '''
                all_funcs[func][0] += 1
                all_funcs[func][2] = file_name

            except KeyError:
                #TODO: there are cases declared WINAPI but not in spec file
                page += 1
                all_funcs[func] = [-10, page,file_name,[],line.split(" ")[0]]
                # print(func,all_funcs[func])
                continue

            all_funcs[func][4] = line.split(" ")[0]
            func_location.append([func,page])
        page += 1
    func_location.sort(key=lambda x:-x[1])

    insertnum = 0

    for name,i in func_location:
        left_location = i
        right_location = []
        end_location = i
        is_useful = 0
        var_name = []
        retvar_name = []
        theone = ''
        ingetval = 0
        for j in range(2000):
            ifdebug = 0

            p = re.compile('([a-zA-Z]+),')
            if is_useful != 1 and p.findall(lines[i + j]) != []:
                for eachone in p.findall(lines[i + j]):
                    var_name.append(eachone)
            p2 = re.compile('([a-zA-Z]+)\)')
            if is_useful != 1 and  p2.findall(lines[i + j]) != []:
                for eachone in p2.findall(lines[i + j]):
                    var_name.append(eachone)
            if is_useful != 1 and  '{' in lines[i+j]:
                left_location = i+j
                is_useful = 1

            if 'return ' in lines[i + j] and ';' == list(lines[i + j].strip())[-1]:
                right_location.append(i+j)

                p3 = re.compile('return ([^;]+);')
                theone += p3.findall(lines[i + j])[0]
                retvar_name.append(theone)
                theone = ''
                ingetval = 0
                continue
            elif 'return ' in lines[i + j]:
                right_location.append(i+j)

                p3 = re.compile('return ([^;]+)')

                theone += p3.findall(lines[i + j].strip())[0]
                ingetval = 1

                if (0):
                    print(lines[i + j].strip())
                    print(theone)
                    print(all_funcs[name])
                    input()
                continue
            elif ingetval == 1 and ';' == list(lines[i + j].strip())[-1]:

                p3 = re.compile('([^;]+);')
                ifdebug = 0
                theone += p3.findall(lines[i + j].strip())[0]
                retvar_name.append(theone)

                if (ifdebug):
                    print(lines[i + j].strip())
                    print(theone)
                    print(all_funcs[name])
                    input()
                theone = ''
                ingetval = 0
                continue

            elif ingetval == 1:

                ifdebug = 0
                theone += lines[i + j].strip()
                if (ifdebug):
                    print(lines[i + j].strip())
                    print(theone)
                    print(all_funcs[name])
                    input()
                continue
            if '}\n' == lines[i+j]:
                end_location = i+j
                # print(lines[i+j])
                # print(all_funcs[name])
                # input()
                is_useful = 2
                break

        if(is_useful == 0):
            print('is userful == 0')
            print(name, i,all_funcs[name])

            continue
        elif(is_useful==1):

            print("-------there is one with no } but { exist")
            print(name, i,all_funcs[name])
            continue

        elif(is_useful == 2):
            #TODO:every func who has been inserted is marked as page num
            # as there are func in // so only explicit one has been inserted

            # TODO:接下来做行数标记
            all_funcs[name][1] = page
            insertnum += 1
            '''
            insert ret value as ret val
            '''
            retvar_name.reverse()
            right_location.reverse()
            for num,i in enumerate(right_location):
                # print(retvar_name[num])
                # print(i)
                # print(insertContentRet(all_funcs,name,retvar_name[num]))
                # input()
                lines.insert(int(i)-1,insertContentRet(all_funcs,name,retvar_name[num]))

            lines.insert(int(left_location)+1,insertContentVar(all_funcs,name,var_name))


    f_new.write("".join(lines))
    return insertnum
    # namee = re.split('\s', line)[8].lower()
    # for line in lines:


def whatProblem(all_funcs):
    for i in all_funcs:
        if all_funcs[i][0] == 0:
            '''
            means don't exist most time never happend
            '''
            print("don't exist "+i+str(all_funcs[i]))
        if all_funcs[i][1] == 0:
            '''
            means exist but not insert
            '''
            print("don't insert "+i+str(all_funcs[i]))
        if all_funcs[i][0] > 1:
            '''
            means implment above 1
            '''
            print("too much implement "+i+str(all_funcs[i]))

        if all_funcs[i][0] < 0:
            '''
            means not in spec file
            '''
            print("not in spec file "+i+str(all_funcs[i]))

def main():
    new_path = "../crypt32"
    old_path = "../crypt32_bac"
    all_cfile_name,spec_name = pickUsefulFiles(old_path)

    all_funcs = getFuncName(old_path,spec_name)

    insertnum = 0
    print(len(all_funcs))


    for cfile in all_cfile_name:
        insertnum += addNewChannel(old_path,new_path,all_funcs,cfile)

    print(len(all_funcs))
    # whatProblem(all_funcs)







if __name__ == '__main__':
    all_funcs = main()
    # a = '232 33;'
    # print(list(a)[-1])


'''
000000CreateFileU
1111111CreateFileU
000000CryptAcquireContextU
1111111CryptAcquireContextU
000000I_CryptGetDefaultCryptProv
1111111I_CryptGetDefaultCryptProv


000000CryptDecodeObject
000000CryptEncodeObjectEx

000000CryptEncodeObject
000000PFXExportCertStore

000000CreateFileU
1111111CreateFileU
000000CryptAcquireContextU
1111111CryptAcquireContextU
000000 I_CryptGetDefaultCryptProv
1111111 I_CryptGetDefaultCryptProv

000000CryptEncodeObject

000000 PFXExportCertStore
'''

