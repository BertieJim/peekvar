import pandas as pd
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

def addTest(name,var):
    '''
    BOOL WINAPI DECLSPEC_HOTPATCH* (*MyCertAddEncodedCertificateToStore)(HCERTSTORE hCertStore,
 DWORD dwCertEncodingType, const BYTE *pbCertEncoded, DWORD cbCertEncoded,
 DWORD dwAddDisposition, PCCERT_CONTEXT *ppCertContext);
    '''
    line1 = "\n"+var[1] + " WINAPI" + " DECLSPEC_HOTPATCH* (* My" + name + ")("
    num = len(var[2])
    line2 = ""
    if(num == 0):
        line2 = ");"
        return line1+line2
    if(num == 1):
        if (var[3][0] == '='):
            line2 +=  var[2][0] + " "+ ");"
        else:
            if('[]' in var[2][0]):
                line2 +=  var[2][0].split("[")[0] + " " + var[3][0]+ "[]);"
            else:
                line2 +=  var[2][0] + " " + var[3][0]+ ");"
        return line1 + line2
    else:
        line2 = var[2][0] + " " +var[3][0]
        for i in range(num-1):
            if(var[3][i+1] == '='):
                line2 += "\n," + var[2][i + 1] + " "
            else:
                if ('[]' in var[2][i+1]):
                    line2 += "\n," +str(var[2][i+1]).split("[")[0] + " " + var[3][i+1] + "[]"
                else:
                    line2 += "\n," + var[2][i+1] +" "+var[3][i+1]
        line2 += ");"
        return line1+line2
def printContent(indent,name,var):
    dllname = var[0].split(".")[0]
    if (len(var[2]) == 0):

        string1 = indent+"PEEKVAR(\"_CALL_" + dllname + "." + name + "_("
        string2 = ""
        string3 = ")\\n\""
        string5 = ");\n"
        new_line = string1 + string2 + string3 + string5
        return new_line

    string1 = indent+"PEEKVAR(\"_CALL_" + dllname + "." + name + "_("
    # %d_%C_%S
    string2 = ""
    if (var[2][0] in TYPE_TO_TYPE.keys()):
        var_list = TYPE_TO_TYPE[var[2][0]]
    else:
        var_list = "%p"
        # print("--------————————" + var[2][0])

    for i in range(len(var[2]) - 1):
        if (var[2][i + 1] in TYPE_TO_TYPE.keys()):
            var_list += ',' + TYPE_TO_TYPE[var[2][i + 1]]
        else:
            var_list += ",%p"
            # print("--------————————" + var[2][i + 1])

    string2 = var_list

    string3 = ")\\n\","
    # varname,varname,varname
    if ("[" in var[3][0]):
        temp = var[3][0].split('[')[0]
        var_name_list = temp
    else:
        var_name_list = str(var[3][0])
    # var_name_list = str(var_name[0])
    for i in range(len(var[3]) - 1):
        try:
            if ("[" in var[3][i + 1]):
                temp = var[3][i + 1].split('[')[0]
                var_name_list += "," + temp
            else:
                var_name_list += "," + str(var[3][i + 1])
        except IndexError:
            print(name,var,i,len(var[3][0]) - 1)
            input()
    string4 = var_name_list

    string5 = ");\n"

    new_line = string1 + string2 + string3 + string4 + string5
    return new_line
def printRet(indent,name,var):


    if(str(var[1].strip().lower()) == 'void'):
        line1 = indent
    else:
        line1 = indent + var[1] + " peekvar_ret = "
    line2 = "My"+str(name) + "("
    num = len(var[2])
    if (num == 0):
        line2 += ");"
    if (num == 1):
        if (var[3][0] == '='):
            line2 +=   ""+ ");"
        else:
            line2 +=   var[3][0]+");"
    else:
        if (var[3][0] == '='):
            line2 += ""
        else:
            line2 += var[3][0]+""
        for i in range(num - 1):
            if (var[3][i + 1] == '='):
                line2 += ", "
            else:
                line2 += ", " + var[3][i + 1]
        line2 += ");"

    dllname = var[0].split(".")[0]
    line3 = "\n"+indent+"PEEKVAR(\"_RET_" + dllname + "." + name + "_("
    # %d_%C_%S
    line4 = ""
    if(str(var[1].strip().lower()) == 'void'):
        line4 = ""
        line5 = ")\\n\""

    else:
        try:
            line4 = TYPE_TO_TYPE[var[1]]
        except KeyError:
            line4 = "%p"
        line5 = ")\\n\","

    # varname,varname,varname
    if(str(var[1].strip().lower()) == 'void'):
        line6 = ""
    else:
        line6 = "peekvar_ret"
    line7 = ");\n"
    if (str(var[1].strip().lower()) == 'void'):
        line8 = "}\n"
    else:
        line8 = indent + "return peekvar_ret;\n}\n"
    new_line = line1 + line2 + line3 + line4 + line5 + line6 + line7 + line8
    return new_line

def addTestHook(name,var):
    '''
    BOOL WINAPI DECLSPEC_HOTPATCH CertAddEncodedCertificateToStore_hook(HCERTSTORE hCertStore,
 DWORD dwCertEncodingType, const BYTE *pbCertEncoded, DWORD cbCertEncoded,
 DWORD dwAddDisposition, PCCERT_CONTEXT *ppCertContext)
 {
    printf("CertAddEncodedCertificateToStore_hookee is called\n");
    printf("hookee(%p, %08x, %p, %d, %08x, %p)\n", hCertStore, dwCertEncodingType,
     pbCertEncoded, cbCertEncoded, dwAddDisposition, ppCertContext);

    BOOL tempr = MyCertAddEncodedCertificateToStore( hCertStore,
  dwCertEncodingType, pbCertEncoded,  cbCertEncoded,
  dwAddDisposition,  ppCertContext);
    printf("hookee %p",tempr);

    return tempr;
}
    '''
    line1 = "\n" + var[1] + " WINAPI" + " DECLSPEC_HOTPATCH " + name + "_hook("
    line2 = ""
    num = len(var[2])
    if (num == 0):
        line2 = ")"
    if (num == 1):
        if (var[3][0] == '='):
            line2 +=  var[2][0] + " "+ ")"
        else:
            if ('[]' in var[2][0]):
                line2 += var[2][0].split("[")[0] + " " + var[3][0] + "[])"
            else:
                line2 += var[2][0] + " " + var[3][0] + ")"
    else:
        line2 = var[2][0] + " " + var[3][0]
        for i in range(num - 1):
            if (var[3][i + 1] == '='):
                line2 += "\n," + var[2][i + 1] + " "
            else:
                if ('[]' in var[2][i+1]):
                    line2 += "\n,"+str(var[2][i+1]).split("[")[0] + " " + var[3][i+1] + "[]"
                else:
                    line2 += "\n," + var[2][i+1] +" "+var[3][i+1]
        line2 += ")"
    line3 = "\n{"
    line4 = "\n"
    line5 = printContent("    ",name,var)
    line6 = printRet("    ",name,var)

    return line1 + line2 + line3 + line4 + line5 + line6

def addTestInMain(indent,name,var):
    '''
        MyCertCreateCertificateContext = CertCreateCertificateContext;
	   	funchook_prepare(funchook,(void**)&MyCertCreateCertificateContext,CertCreateCertificateContext_hook);
       '''
    t1 =  "\n"+indent + "My" + name + " = " +name + ";"
    t2 = "\n" + indent + "funchook_prepare(funchook,(void**)&My" +name + "," +name+"_hook" + ");\n"
    return t1+t2
def getFuncText(funcinfo):
    text = []
    for i in funcinfo.keys():
        text.append(addTest(i,funcinfo[i]))

    return '\n'+ "".join(text)
def getFuncHookTest(funcinfo):
    text = []
    for i in funcinfo.keys():
        text.append(addTestHook(i,funcinfo[i]))
    return '\n' + "".join(text)

def getDllMaintest(funcinfo):
    text = []
    t = "\n{\nint rv;\n" \
        "funchook = funchook_create();"
    t_e = "\nrv = funchook_install(funchook,0);" \
         "\nif(rv!=0){\n" \
         "printf(\"install funchook failed\\n\");" \
         "}\n}"
    text.append(t)
    for i in funcinfo.keys():
        text.append(addTestInMain("    ",i, funcinfo[i]))
    return '\n' + t + "".join(text) + t_e
def main():
    funcInfo = pd.read_pickle('../data/needToBeSet.pkl')
    t1 = getFuncText(funcInfo)
    t2 = getFuncHookTest(funcInfo)
    t3 = "\n    funchook_t *funchook = NULL;"
    print(t1+t2+t3)
def main2():
    funcInfo = pd.read_pickle('../data/needToBeSet.pkl')
    print(len(funcInfo))
    # t = getDllMaintest(funcInfo)
    # print(t)

if __name__ == '__main__':
    # main()
    main2()

    #TODO:1.main里的不声明 2[] 3.void