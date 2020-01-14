

'''
this file deal the API folder
output as follows:
1.a group that :
 funcname funcdll funcgroup1 funcgroup2 funcgroup3
'''

'''

1. know the longest api group could be
[6]
DsBrowseForContainer ['Security and Identity', 'Directory, Identity, and Access Services', 'Directory Services', 'Directories', 'Active Directory Domain Services', 'Display']

why there are func (stub) like this:
 ?CreateVssSnapshotSetDescription@@YGJU_GUID@@JPAPAVIVssSnapshotSetDescription@@@Z
 
 how long is it?
 
2. make a [] serial, like [group1, group2, group3, 0 , 0]
[300,100,200,100 ]

SELECT * FROM peekvar.funcgroup where funcname = "strcat";
用谁 结果都一样；相似性怎么求。
'''
# group1 group2 group3 group4

import os
import re
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from tqdm import  tqdm
import sys

from db import bigDb
import numpy as np
import cv2
import pandas as pd


def dirpass(dirin):
    num = 0
    alldll = []
    g = os.walk(dirin)
    all_file = []
    p = re.compile(r'Module Name="(.*).dll')
    for path,d,filelist in g:
        # print(path)
        for filename in filelist:
            filepath = os.path.join(path,filename)
            if os.path.splitext(filename)[1] == '.xml' and 'new.xml' not in filename:
                all_file.append(filepath)


    return all_file

def changeXMLFont1(filename,new_f):

    f = open(filename)
    f_new = open(new_f,'w')
    try:
        lines = f.read()
    except UnicodeDecodeError:
        print(filename)
    if "Category" not in lines:
        f_new.write(lines.strip())
        return
    p = re.compile('<Category Name="([^>]+) />')
    for i in p.findall(lines):
        lines = lines.replace(i+"\" />",i+"\" >")

    # lines = lines.replace('</Api>\n        <Category','</Api>\n        </Category>\n        <Category')
    lines = lines.replace('        <Category','\n        </Category>\n        <Category')
    # lines = lines.replace('</Api>\n    </Module>','</Api>\n        </Category>\n    </Module>')

    lines = lines.replace('    </Module>','        </Category>\n    </Module>')

    #find the first category one and change it:
    lineses = lines.split('\n')
    for i in lineses:
        if i == '        </Category>':
            lineses.remove(i)
            break



    f_new.write("\n".join(lineses))


def changeXMLFont(filename,new_f):

    f = open(filename)
    f_new = open(new_f,'w')
    try:
        lines = f.readlines()
    except UnicodeDecodeError:
        print(filename)
    if "Category" not in "".join(lines):
        f_new.write("".join(lines))
        return
    flag = 0
    for i,line in enumerate(lines):
        if "<Category" in line:
            flag = 1
            lines[i] = lines[i].replace('/>','>')

    lines = "".join(lines)
    # lines = lines.replace('</Api>\n        <Category','</Api>\n        </Category>\n        <Category')
    lines = lines.replace('        <Category','\n        </Category>\n        <Category')
    # lines = lines.replace('</Api>\n    </Module>','</Api>\n        </Category>\n    </Module>')

    lines = lines.replace('    </Module>','        </Category>\n    </Module>')

    #find the first category one and change it:
    lineses = lines.split('\n')
    for i in lineses:
        if i == '        </Category>':
            lineses.remove(i)
            break



    f_new.write("\n".join(lineses))

def findfuncgroupinonefile(filename,allfuncandtheirgroup ):
    # filename = "../API/Windows/Crypt32.xml"

    new_xml = os.path.splitext(filename)[0]+"new"+os.path.splitext(filename)[1]

    changeXMLFont(filename,new_xml)

    lines = open(new_xml).read()
    print(filename)
    # try:
    tree = ET.fromstring(lines)
    # except ET.ParseError:
    #     print(filename)
    #
    #     input()

    group_pkey = {}
    group_n = []
    group = []
    for m in tree.findall("Module"):
        dllname = m.get("Name")

        for Category in m.findall("Category"):
            cname = Category.get("Name")
            group = cname.split('/')
            if group[0] not in group_pkey:
                group_pkey[group[0]] = [len(group_pkey.keys())+1,0]

            for api in Category.findall("Api"):
                aname = api.get("Name")

                allfuncandtheirgroup[aname,dllname] = group
                if((aname,dllname) in allfuncandtheirgroup.keys()):
                    if(allfuncandtheirgroup[aname,dllname] != group):
                        print(aname)
                        print(group)
                        print(dllname)
                        input()
                    else:
                        pass
                anum = group_pkey[group[0]][0]*100 + group_pkey[group[0]][1]+1
                group_pkey[group[0]][1] += 1
                # db = bigDb()
                # db.buildFuncGroupTable(aname,('%05d') % anum)
                # input()

def findfuncinfoinonefile(filename,allfuncandtheirgroup,allfuncandtheirgroup1 ):
    '''

    :param filename:
    :param allfuncandtheirgroup:
    :param allfuncandtheirgroup1:
    :return:
    '''
    '''
    the main problem is:
    in xml file,
     function   two different var  different dll
     functoin    two different var   same dll
    function      same var          different dll
    function       sanme var          sanme dll
    
    改名字为 num；
    define func func_a 问题解决
    
    :param filename:
    :param allfuncandtheirgroup:
    :return:
    '''
    # filename = "../API/Windows/Crypt32.xml"

    lines = open(filename).read()
    # try:
    tree = ET.fromstring(lines)
    # except ET.ParseError:
    #     print(filename)
    #
    #     input()
    maxparamlen = 0
    maxparamfunc = None

    for m in tree.findall("Module"):
        dllname = m.get("Name")
        for Api in m.findall("Api"):


            aname = Api.get("Name")
            paramgroup = []
            paramgroup.append(dllname)
            paramgroup.append(filename)
            if(aname == 'CreateAssemblyNameObject'):
                input()

            for param in Api.findall("Param"):
                paramgroup.append(param.get("Type"))
            all_diff_minus_one = 2

            if aname in allfuncandtheirgroup.keys() and allfuncandtheirgroup[aname][2:]!=paramgroup[2:]:
                if(allfuncandtheirgroup[aname][1] == '../API/Microsoft.NET/fusion.xml'):
                    allfuncandtheirgroup[aname][0] = paramgroup[0]
                    continue
                if (paramgroup[1] == '../API/Microsoft.NET/fusion.xml'):
                    paramgroup[0] = allfuncandtheirgroup[aname][0]
                    allfuncandtheirgroup[aname] = paramgroup
                    continue

                if(allfuncandtheirgroup[aname][0] == dllname):
                    continue

                all_diff_minus_one = 1

                for i in range(len(paramgroup)-1):
                    if (abs(len(paramgroup[i]) - len(allfuncandtheirgroup[aname][i])) > 1):
                        all_diff_minus_one = 0
                        break

            if (all_diff_minus_one == 0):
                print(aname)
                print(filename)
                print(allfuncandtheirgroup[aname])
                print(paramgroup)
                print("went wrong")
                allfuncandtheirgroup1[aname] = paramgroup
                continue

            if(all_diff_minus_one == 1):
                allfuncandtheirgroup1[aname] = paramgroup
                continue

            if aname in allfuncandtheirgroup.keys() and allfuncandtheirgroup[aname][2:] == paramgroup[2:] :
                if(allfuncandtheirgroup[aname][0] == dllname):
                    continue
                else:
                    allfuncandtheirgroup1[aname] = paramgroup
                    continue

            # just look that these things look like: indeed all the same; no nedd to worry
            # elif(all_diff_minus_one == 1):
            #     print("+++" + aname)
            #     print(paramgroup)
            #     print(allfuncandtheirgroup[aname])
            #     input()

            allfuncandtheirgroup[aname] = paramgroup
            # print(aname)
            # print(allfuncandtheirgroup[aname])



def getgroupinfo_prepare():
    all_files = dirpass('../API/')
    allfuncandtheirgroup = {}

    for file in all_files:
        findfuncgroupinonefile(file,allfuncandtheirgroup)

    maxlen = 0
    maxi = None
    for i in allfuncandtheirgroup:
        if maxlen < len(allfuncandtheirgroup[i]):
            maxlen = len(allfuncandtheirgroup[i])
            maxi = i


    pd.to_pickle(allfuncandtheirgroup, "../data/findfuncgroupinonefile.pdl")

def getfuncgroupinfo():

    allfuncandtheirgroup = pd.read_pickle("../data/findfuncgroupinonefile.pdl")

    for i,dllname in tqdm(allfuncandtheirgroup):
        db = bigDb()
        db.buildFuncGroupTable(i,dllname,allfuncandtheirgroup[i,dllname],len(allfuncandtheirgroup[i,dllname]))
        db.close()
def getfuncinfo_prepare():
    '''
    18 param the longest:
    ScriptPlaceOpenType
    ['HDC', 'SCRIPT_CACHE*', 'SCRIPT_ANALYSIS*', 'OPENTYPE_TAG', 'OPENTYPE_TAG', 'int*', 'TEXTRANGE_PROPERTIES**', 'int', 'const WCHAR*', 'WORD*', 'SCRIPT_CHARPROP*', 'int', 'const WORD*', 'const SCRIPT_GLYPHPROP*', 'int', 'int*', 'GOFFSET*', 'ABC*', '../API/Windows/Usp10.xml']
    :return:
    '''
    all_files = dirpass('../API/')
    allfuncandtheirinfo = {}
    allfuncandtheirinfo1 = {}

    maxplen = 0
    maxpname = None
    for file in tqdm(all_files):
        findfuncinfoinonefile(file, allfuncandtheirinfo,allfuncandtheirinfo1)

    pd.to_pickle(allfuncandtheirinfo, "../data/allfuncandtheirinfo.pdl")
    pd.to_pickle(allfuncandtheirinfo1, "../data/allfuncandtheirinfo1.pdl")


def getfuncinfo():
    allfuncandtheirinfo = pd.read_pickle("../data/allfuncandtheirinfo.pdl")
    allfuncandtheirinfo1 = pd.read_pickle("../data/allfuncandtheirinfo1.pdl")

    '''
    ['Cabinet.dll', '../API/Windows/Cabinet.xml', 'PCABINETDLLVERSIONINFO']
    '''

    for i in tqdm(allfuncandtheirinfo):
        db = bigDb()
        db.buildFuncVarTypeXmlTable(i, allfuncandtheirinfo[i][0],allfuncandtheirinfo[i][2:], len(allfuncandtheirinfo[i])-2)
        db.close()
    for i in tqdm(allfuncandtheirinfo1):
        # print(i)
        # print(allfuncandtheirinfo1[i])
        db = bigDb()
        db.buildFuncVarTypeXmlTable(i, allfuncandtheirinfo1[i][0],allfuncandtheirinfo1[i][2:], len(allfuncandtheirinfo1[i])-2)
        db.close()

def debug():
    allfuncandtheirinfo1 = pd.read_pickle("../data/allfuncandtheirinfo1.pdl")
    allfuncandtheirinfo = pd.read_pickle("../data/allfuncandtheirinfo.pdl")

    for i in tqdm(allfuncandtheirinfo1):
        print(i)
        print(allfuncandtheirinfo1[i])
        db = bigDb()
        db.buildFuncVarTypeXmlTable(i, allfuncandtheirinfo1[i][0], allfuncandtheirinfo1[i][2:],
                                    len(allfuncandtheirinfo1[i]) - 2)
        db.close()
def instrsingscene():
    a = {1:[1,2,3],2:[2,3],3:[3]}
    for i in a:
        a[i].insert(0,len(a[i]))
    print(a)

if __name__ == '__main__':
    # main()
    # debug()
    # getgroupinfo_prepare()
    getfuncgroupinfo()
    # getfuncinfo_prepare()
    # getfuncinfo()







    # a = ' ?CreateVssSnapshotSetDescription@@YGJU_GUID@@JPAPAVIVssSnapshotSetDescription@@@Z'
    # print(len(a))
    # instrsingscene()



