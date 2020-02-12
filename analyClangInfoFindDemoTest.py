import pandas as pd

def findifSet(funcinfile,functoset):
    for i in funcinfile.keys():
        if i in functoset:
            functoset[i] += 1

def getFuncInfo(dllname,funcinfile,filename):
    f = open(filename)
    lines = f.readlines()
    for line in lines:
        try:
            line = line.strip()
            tmp = line.split(':')
            funcname = tmp[0]

            rettype = tmp[1]
            vartype = []
            varname = []
            ts = tmp[2].split('+')
            for t in ts:
                if (t == ''):
                    continue
                vartype.append(t.split('^')[0])
                varname.append(t.split('^')[1])
            if funcname not in funcinfile.keys():
                funcinfile[funcname] = [dllname,rettype,vartype,varname]
            else:
                print(funcname)
                print(funcinfile[funcname])
                print(filename)
                input()


        except IndexError:
            print(line)
            input()
    return funcinfile



def getNeedFuncInfo(dllname,funcinfile,filename,funcinglobe):
    f = open(filename)
    lines = f.readlines()
    for line in lines:
        try:
            line = line.strip()
            tmp = line.split(':')
            funcname = tmp[0]
            if funcname not in funcinglobe:
                continue

            rettype = tmp[1]
            vartype = []
            varname = []
            ts = tmp[2].split('+')
            for t in ts:
                if (t == ''):
                    continue
                vartype.append(t.split('^')[0])
                varname.append(t.split('^')[1])
            if funcname not in funcinfile.keys():
                funcinfile[funcname] = [dllname,rettype,vartype,varname]
            else:
                print(funcname)
                print(funcinfile[funcname])
                print(filename)
                input()


        except IndexError:
            print(line)
            input()
    return funcinfile


def main():
    filename1 = '/Users/bertie/Downloads/FunctionStartEnd/encode_info.txt'
    filename2 = '/Users/bertie/Downloads/FunctionStartEnd/crl_info.txt'
    filename3 = '/Users/bertie/Downloads/FunctionStartEnd/main_info.txt'
    filename4 = '/Users/bertie/Downloads/FunctionStartEnd/cert_info.txt'
    filename5 = '/Users/bertie/Downloads/FunctionStartEnd/oid_info.txt'
    filename6 = '/Users/bertie/Downloads/FunctionStartEnd/store_info.txt'

    filename7 = '/Users/bertie/Downloads/FunctionStartEnd/decode_info.txt'
    filename8 = '/Users/bertie/Downloads/FunctionStartEnd/ctl_info.txt'



    funcglobe = ['CertCreateCertificateContext', 'CertCreateContext', 'CertCreateCRLContext', 'CertCreateCTLContext', 'CryptExportPublicKeyInfo', 'CertCreateSelfSignCertificate', 'CryptMemAlloc', 'CryptEncodeObject', 'CryptEncodeObjectEx', 'CryptMemFree', 'CertGetEnhancedKeyUsage', 'CertGetValidUsages', 'CertRemoveEnhancedKeyUsageIdentifier', 'CertSetEnhancedKeyUsage', 'CertAddEnhancedKeyUsageIdentifier', 'CertSetCertificateContextProperty', 'CertGetCertificateContextProperty', 'CryptDecodeObject', 'CryptDecodeObjectEx', 'CertFindExtension', 'CertGetIntendedKeyUsage', 'CryptVerifyCertificateSignature', 'CryptVerifyCertificateSignatureEx', 'CryptSignAndEncodeCertificate', 'CryptSignCertificate', 'CryptFindOIDInfo', 'I_CryptGetDefaultCryptProv', 'CryptHashToBeSigned', 'CryptHashPublicKeyInfo', 'CryptHashCertificate', 'CertIsRDNAttrsInCertificateName', 'CryptInitOIDFunctionSet', 'CertVerifyRevocation', 'CryptGetDefaultOIDDllList', 'CryptGetDefaultOIDFunctionAddress', 'CryptFreeOIDFunctionAddress', 'CertFindCertificateInStore', 'CertGetIssuerCertificateFromStore', 'CertVerifySubjectCertificateContext', 'CertFreeCertificateContext', 'CertGetCRLFromStore', 'CertVerifyCRLRevocation', 'CertVerifyTimeValidity', 'CertGetPublicKeyLength', 'CryptImportPublicKeyInfo', 'CertComparePublicKeyInfo', 'CertCompareCertificate', 'CertCompareCertificateName', 'CertCompareIntegerBlob', 'CryptAcquireCertificatePrivateKey', 'CertGetStoreProperty', 'CertOpenSystemStoreW', 'CertAddEncodedCertificateToSystemStoreW', 'CertAddEncodedCertificateToStore', 'CertCloseStore', 'CertOpenSystemStoreA', 'CertAddEncodedCertificateToSystemStoreA', 'CertAddCertificateContextToStore']
    dllname = 'crypt32.dll'
    funcset = {}
    funcinfile = {}
    for i in funcglobe:
        funcset[i] = 0
    funcinfile1 = getNeedFuncInfo(dllname,funcinfile,filename1,funcglobe)
    funcinfile2 = getNeedFuncInfo(dllname,funcinfile,filename2,funcglobe)
    funcinfile3 = getNeedFuncInfo(dllname,funcinfile,filename3,funcglobe)
    funcinfile4 = getNeedFuncInfo(dllname,funcinfile,filename4,funcglobe)
    funcinfile5 = getNeedFuncInfo(dllname,funcinfile,filename5,funcglobe)
    funcinfile6 = getNeedFuncInfo(dllname,funcinfile,filename6,funcglobe)
    funcinfile7 = getNeedFuncInfo(dllname,funcinfile,filename7,funcglobe)
    funcinfile8 = getNeedFuncInfo(dllname,funcinfile,filename8,funcglobe)

    funcandfile = pd.read_pickle("../data/funcs_and_files.pkl")
    '''
    这些函数，一定在spec里，一定是正宗api，不在cert里而已
    '''
    # funcinfile = funcinfile1 + funcinfile2 + funcinfile3 + funcinfile4 + funcinfile5 + funcinfile6 + funcinfile7 + funcinfile8

    findifSet(funcinfile,funcset)

    for i in funcset:
        if(funcset[i] == 0):
            # pass
            print(i+" "+str(funcandfile[i]))
        else:
            print("------")

    needtoBeSet = {}
    for i in funcglobe:
        needtoBeSet[i] = funcinfile[i]

    pd.to_pickle(needtoBeSet, "../data/needToBeSet.pkl")


if __name__ == '__main__':
    main()




