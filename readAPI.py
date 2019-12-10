

'''
this file deal the API folder
output as follows:
1.a group that :
 funcname funcdll funcgroup1 funcgroup2 funcgroup3
'''
import os
import re
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from db import bigDb

def dirpass(dirin):
    num = 0
    alldll = []
    g = os.walk(dirin)
    p = re.compile(r'Module Name="(.*).dll')
    for path,d,filelist in g:
        # print(path)
        for filename in filelist:
            filepath = os.path.join(path,filename)
            f = open(filepath)
            for line in f.readlines():
                if p.findall(line)!=[]:
                    num += 1
                    # print(str(p.findall(line)[0])+'.dll')
                    alldll += [str(p.findall(line)[0]).lower()+'.dll' ]
                    # print()

    return num,alldll

def changeXMLFont(filename,new_f):
    f = open(filename)
    f_new = open(new_f,'w')
    lines = f.read()
    p = re.compile('<Category Name="([^"]+)"')
    for i in p.findall(lines):
        lines = lines.replace(i+"\" />",i+"\" >")

    lines = lines.replace('</Api>\n        <Category','</Api>\n        </Category>\n        <Category')
    lines = lines.replace('</Api>\n    </Module>','</Api>\n        </Category>\n    </Module>')
    f_new.write(lines)

def main():
    filename = "../API/Windows/Crypt32.xml"
    new_xml = os.path.splitext(filename)[0]+"new"+os.path.splitext(filename)[1]
    changeXMLFont(filename,new_xml)
    lines = open(new_xml).read()
    tree = ET.fromstring(lines)
    group_pkey = {}
    group_n = []
    group = []
    for m in tree.findall("Module"):
        for Category in m.findall("Category"):
            cname = Category.get("Name")
            group = cname.split('/')
            if group[0] not in group_pkey:
                group_pkey[group[0]] = len(group_pkey.keys())+1

            for api in Category.findall("Api"):
                aname = api.get("Name")

                print(aname)
                input()




if __name__ == '__main__':

    main()
