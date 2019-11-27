
import os
import re
import copy

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
    for i in allFiles:

        suffix = os.path.splitext(i)[1]
        if suffix == '.spec':
            specfile.append(os.path.split(i)[-1])

    return specfile


def doIt(allType,prefix,name):
    for i in name:
        f = open(os.path.join(prefix,i))
        alllines = f.readlines()
        for line in alllines:
            sec = line.split(" ")
            if sec[1].lower() == 'stdcall':
                p = re.compile('\(([^\)]+)\)')
                nov = 0
                func = []
                try:
                    func = p.findall(line)[0]
                except IndexError:
                    nov = 1
                if(nov):
                    continue
                newType = func.split(' ')
                for t in newType:
                    if t.strip() not in allType.keys():
                        allType[t.strip()] = 1
                    else:
                        allType[t.strip()] += 1



def whatWeHave():
    old_path = "../crypt32_bac"
    pec_name = pickUsefulFiles(old_path)
    allTypeString = dict()

    doIt(allTypeString,old_path,pec_name)
    print(allTypeString)

if __name__ == '__main__':
    whatWeHave()





