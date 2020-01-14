'''
本文档用处如下：
peekvar -g
生成配置文件

peekvar -i
根据配置文件，生成patch

patch

'''

import copy
import os
import re
# from tqdm import tqdm


#from db import bigDb
TYPE_TO_TYPE ={
    "str":"%d",
    "ptr":"%p",
    "long":"%d",
    "wstr":"%s",
    "BOOL":"%d",
    "void*":"%p",
    "LONG":"%d",
    "DWORD":"%d"

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
global funchavetwoname
def getFuncName(prefix,specfile,dllname):
    '''
    :param prefix:
    :param specfile: only filename
    :return:
    '''
    allfuncs = {}

    for i in specfile:
        f = open(os.path.join(prefix,i))
        alllines = f.readlines()
        realname = None
        for line in alllines:
            sec = line.split(" ")
            if sec[1].lower() == 'stdcall':
                if list(line.strip())[-1] != ")":
                    realname = sec[-1].split(".")
                    # print(dllname)
                    dllname = realname[0]
                    # print(realname[0])
                    # print(sec[2].split("(")[0])
                    # funchavetwoname += 1
                p = re.compile('\(([^\)]+)\)')
                try:
                    type = p.findall(line)[0].split(' ')
                except IndexError:
                    allfuncs[sec[2].split("(")[0]] = [0, dllname,'null',[],[],[],'VOID']
                    continue
                allfuncs[sec[2].split("(")[0]] = [0,dllname,'null',type,[],[],"VOID"]

    return allfuncs

def insertContentRet(all_funcs,func_name,var_name,indent):
    #insertContentRet(all_funcs[name],name,"peekvar_temp"))
    #  allfuncs[sec[2].split("(")[0]] = [0,dllname,'null',type,[],[],"VOID"]
    #VARPEEK("(str,str,BOOL)\n","RET","CryptBinaryToStringW",encoder(pbBinary, cbBinary, dwFlags, pszString, pcchString));
    #FIXME("Unimplemented type %d\n", dwFlags & 0x0fffffff);

    string1 = "TRACE(\"_RET_\\n\");\n"
    string6 = indent+"return "+var_name+";}\n"
    new_line = string1 +string6
    return new_line

def insertContentVar(all_funcs,func_name,var_name):
    # insertContentRet(all_funcs[name],name,"peekvar_temp"))
    #  allfuncs[sec[2].split("(")[0]] = [0,dllname,'null',type,[],[],"VOID"]
    # VARPEEK("(str,str,BOOL)\n","RET","CryptBinaryToStringW",encoder(pbBinary, cbBinary, dwFlags, pszString, pcchString));
    # FIXME("Unimplemented type %d\n", dwFlags & 0x0fffffff);

    string1 = "TRACE(\"_CALL_\\n\");\n"
    # %d_%C_%S



    new_line = string1

    return new_line

def getvartypeandname(line):

    p = re.compile('\(([^(^)]+)\)')
    lines = p.findall(line)[0]
    eachones = lines.split(",")
    alltype = []
    allvar = []
    for each in eachones:
        if '*' in each:
            type = each.strip().split("*")[0].strip()+'*'
            var = each.strip().split("*")[1].strip()
            alltype.append(type)
            allvar.append(var)
        else:
            try:
                type = each.strip().split(" ")[0].strip()
                var = each.strip().split(" ")[1].strip()
                alltype.append(type)
                allvar.append(var)
            except IndexError:
                print(line)
                input()
    # print(line)
    # print(alltype)
    # print(allvar)
    # input()
    return alltype,allvar
def addNewChannel(old_prefix,new_prefix,all_funcs, file_name):
    '''
    :param all_funcs: spec name with reference number
    :param file_name: relative path
    :return:
    '''
    # print(os.path.join(prefix,file_name))
    f_old = open(os.path.join(old_prefix,file_name))
    f_new = open(os.path.join(new_prefix , file_name),'w')
    '''
    for compatible
    '''
    print("[-]now with "+file_name)
    func_location = []
    page = 0
    '''
    找到所有winapi函数的位置
    '''
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
                #     allfuncs[sec[2].split("(")[0]] = [0,dllname,'null',type,[],[],"VOID"]

                if(all_funcs[func][0] != -10):
                    all_funcs[func][0] += 1
                    all_funcs[func][2] = file_name
                    func_location.append([func, page])

            except KeyError:
                #TODO: there are cases declared WINAPI but not in spec file
                print(line)
                print("191")
                all_funcs[func] = [-10, page, file_name,[], [], [], "VOID"]

                # input()

            page += 1
            ret_type = line.split(" ")[0].strip()
            #allfuncs[sec[2].split("(")[0]] = [0,dllname,'null',type,[],[],"VOID"]

            if("*" in line.split(" ")[1].strip()):
                ret_type += "*"

            if (ret_type == "static"):
                ret_type = line.split(" ")[1].strip()
                if ("*" in line.split(" ")[2].strip()):
                    ret_type += "*"
                # print(line)
                # input()

            if (ret_type == "const"):
                ret_type = line.split(" ")[1].strip()
                if ("*" in line.split(" ")[2].strip()):
                    ret_type += "*"
                # print(line)
                # input()

            all_funcs[func][-1] = ret_type
            # print(func,all_funcs[func])
            continue


        page += 1
    func_location.sort(key=lambda x:-x[1])

    insertnum = 0

    for name,i in func_location:
        left_location = i
        right_location = []
        end_location = i
        get_startpos = 0
        var_name = []
        var_type = []
        retvar_name = []
        theone = ''
        end_getvar = 0
        ingetval = 0
        var_line = ""
        for j in range(2000):

            if(get_startpos == 0 and ';' in lines[i + j]):
                print(lines[i + j])
                input()
                # 这里，只声明，没有实现。
                break

            if get_startpos == 0 and '{' in lines[i + j]:
                left_location = i + j
                get_startpos = 1
                is_useful = 1
                var_type, var_name = getvartypeandname(var_line)
                var_line = str
                #  all_funcs[func] = [-10, page,file_name,[],[],[],ret_type]

                all_funcs[name][4] = var_type
                all_funcs[name][5] = var_name


                continue

            if(get_startpos == 0):
                # 循环得到所有的变量名和变量类型
                var_line += str(lines[i + j].strip())
                continue

            if(get_startpos == 1):

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
            # all_funcs[name][1] = page

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
                #        all_funcs[func] = [-10, page,file_name,[],[],ret_type]

                indent = lines[int(i)].split('return')[0]
                lines[int(i)] = lines[int(i)].replace("return","{"+all_funcs[name][-1]+" "+"peekvar_temp =")
                last_pos = int(i)
                while(1):
                    if ';' in lines[last_pos]:
                        the_last_pos = last_pos
                        break
                    else:
                        last_pos += 1
                try:
                    lines.insert(last_pos+1,indent+insertContentRet(all_funcs[name],name,"peekvar_temp",indent))
                except TypeError:
                    print(all_funcs[name])
                    print(lines[left_location])
                    print(name)
                    input()
            indent2 = "    "

            lines.insert(int(left_location)+1,indent2+insertContentVar(all_funcs[name],name,var_name))


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
        else:
            pass
            # print("perfect inserted funcs "+i+str(all_funcs[i]))


def test():
    new_path = "../crypt32"
    old_path = "../crypt32_bac"
    all_cfile_name,spec_name = pickUsefulFiles(old_path)

    all_funcs = getFuncName(old_path,spec_name)

    insertnum = 0
    print(len(all_funcs))


    for cfile in all_cfile_name:
        insertnum += addNewChannel(old_path,new_path,all_funcs,cfile)

    print(insertnum)
    print(len(all_funcs))
    whatProblem(all_funcs)

def getDllName(newpath,makefile):
    path = os.path.join(newpath,makefile)
    f = open(path)
    lines = f.read()
    p = re.compile('\s([a-zA-Z0-9]+).dll')
    match = p.findall(lines)
    if(len(match)!=1):
        for i in match:
            if i != match[0]:
                print(match)
                print("get dll name error")
                input()

        return match[0]
    return match[0]

def registerfuncinfo(path,prefix):

    # os.rename(prefix+path,prefix+path+'bac')
    # os.mkdir(prefix+path)

    old_path = prefix + path + 'bac'
    new_path = prefix + path
    all_cfile_name, spec_name = pickUsefulFiles(old_path)
    if(len(spec_name) != 1):
        print('spec file number > 1')
        print(path)
        return

    dllname = getDllName(old_path,'Makefile.in')
    print("[1]now start insert with--"+dllname)

    all_funcs = getFuncName(old_path, spec_name,dllname)
    print("[2]there are "+str(len(all_funcs))+" functions")


    for cfile in all_cfile_name:
        addNewChannel(old_path,new_path, all_funcs, cfile)



if __name__ == '__main__':


    # test()
    path = 'crypt52'
    prefix = '../'
    funchavetwoname = 0
    registerfuncinfo(path,prefix)
    # a = '232 33;'
    # print(list(a)[-1])

