import os
from addNewChannel import pickUsefulFiles
from addNewChannel import getFuncName
import re
'''
this file find functions advote themselves
'''

def findTestFunction(old_prefix,all_funcs,all_demos,file_name):
    f_old = open(os.path.join(old_prefix,file_name))
    lines = f_old.readlines()
    func_location = []
    page = 0
    for line in lines:
        p = re.compile('WINAPI\s([a-zA-Z0-9_]+)')
        func = p.findall(line)
        if func != []:
            func = func[0]
            try:
                '''
                first ,the func is in the file
                '''
                if (all_funcs[func][0] != -10):
                    all_funcs[func][0] += 1
                    all_funcs[func][2] = file_name
                    all_funcs[func][4] = line.split(" ")[0]
                    func_location.append([func, page])

            except KeyError:
                # TODO: there are cases declared WINAPI but not in spec file
                page += 1
                all_funcs[func] = [-10, page, file_name, [], line.split(" ")[0]]
                # print(func,all_funcs[func])

                continue

        page += 1
    func_location.sort(key=lambda x: -x[1])

    insertnum = 0

    for name, i in func_location:
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
            if is_useful == 0 and list(lines[i + j].strip())[-1] == ';':
                for m in all_funcs.keys():
                    if m in lines[i+j]:
                        if m not in all_demos.keys():
                            all_demos[m] = []
                        if(m==name):
                            input()
                            print('-_____')
                        all_demos[m].append([[name,m],[file_name,i+j],all_funcs[m]])
                break

            if is_useful == 0 and p.findall(lines[i + j]) != []:
                pass
                # for m in all_funcs.keys():
                #     if m in lines[i+j]:
                #         if m not in all_demos.keys():
                #             all_demos[m] = []
                #         # all_demos[m].append([[name,m],[file_name,i+j],all_funcs[m]])
                #         if (m == name):
                #             print('++++++')
                #             print(m)
                #             print(lines[i+j])
                #             # input()


            p2 = re.compile('([a-zA-Z]+)\)')

            if is_useful == 0 and p2.findall(lines[i + j]) != []:
                pass
            if is_useful == 0 and '{' in lines[i + j]:
                left_location = i + j
                is_useful = 1
                for m in all_funcs.keys():
                    if m in lines[i+j]:
                        if m not in all_demos.keys():
                            all_demos[m] = []
                        all_demos[m].append([[name,m],[file_name,i+j],all_funcs[m]])

            if 'return ' in lines[i + j] and ';' == list(lines[i + j].strip())[-1]:
                right_location.append(i + j)
                for m in all_funcs.keys():
                    if m in lines[i+j]:
                        if m not in all_demos.keys():
                            all_demos[m] = []
                        all_demos[m].append([[name,m],[file_name,i+j],all_funcs[m]])
                theone = ''
                ingetval = 0
                continue

            elif 'return ' in lines[i + j]:
                right_location.append(i + j)

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

            if '}\n' == lines[i + j]:
                end_location = i + j
                # print(lines[i+j])
                # print(all_funcs[name])
                # input()
                is_useful = 2
                for m in all_funcs.keys():
                    if m in lines[i+j]:
                        if m not in all_demos.keys():
                            all_demos[m] = []
                        all_demos[m].append([[name,m],[file_name,i+j],all_funcs[m]])
                break
            for m in all_funcs.keys():
                if m in lines[i + j]:
                    if (m == name):
                       continue
                    if m not in all_demos.keys():
                        all_demos[m] = []
                    all_demos[m].append([[name, m], [file_name, i + j], all_funcs[m]])



        if (is_useful == 0):
            print('is userful == 0')
            print(name, i, all_funcs[name])

            continue
        elif (is_useful == 1):

            print("-------there is one with no } but { exist")
            print(name, i, all_funcs[name])

            continue

        elif (is_useful == 2):
            # TODO:every func who has been inserted is marked as page num
            # as there are func in // so only explicit one has been inserted

            # TODO:接下来做行数标记
            all_funcs[name][1] = page
            insertnum += 1
            '''
            insert ret value as ret val
            '''



    return 0

def main():
    path = 'crypt42'
    prefix = '../'

    # os.rename(prefix+path,prefix+path+'bac')
    # os.mkdir(prefix+path)
    old_path = prefix + path + 'bac'

    all_cfile_name, spec_name = pickUsefulFiles(old_path)

    # print(dllname)
    all_funcs = getFuncName(old_path, spec_name)
    all_demos = {}

    for cfile in all_cfile_name:
        findTestFunction(old_path, all_funcs,all_demos,cfile)
    for i in all_demos:
        print(i)
        print(all_demos[i])


if __name__ == '__main__':
    main()