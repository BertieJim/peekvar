import pymysql




class bigDb:
    def __init__(self):
        self.conn = pymysql.connect(user='root', password='12345QwertM', database='peekvar', charset='utf8')
        self.cursor = self.conn.cursor()
    def close(self):
        self.cursor.close()
        self.conn.close()
    def buildFuncGroupTable(self,func,dllname,groups,lennum):
        sql = None
        listnew = [func,dllname]
        for i in groups:
            listnew.append(i)
        var = tuple(listnew)

        if lennum == 1:
            sql = 'INSERT INTO funcgroup (`funcname`,dllname,group0) VALUES (%s,%s,%s)'
        elif  lennum == 2:
            sql = 'INSERT INTO funcgroup (`funcname`,dllname,group0,group1) VALUES (%s,%s,%s,%s)'
        elif lennum == 3:
            sql = 'INSERT INTO funcgroup (`funcname`,dllname,group0,group1,group2) VALUES (%s,%s,%s,%s,%s)'
        elif lennum == 4:
            sql = 'INSERT INTO funcgroup (`funcname`,dllname,group0,group1,group2,group3) VALUES (%s,%s,%s,%s,%s,%s)'
        elif lennum == 5:
            sql = 'INSERT INTO funcgroup (`funcname`,dllname,group0,group1,group2,group3,group4) VALUES (%s,%s,%s,%s,%s,%s,%s)'
        elif lennum == 6:
            sql = 'INSERT INTO funcgroup (`funcname`,dllname,group0,group1,group2,group3,group4,group5) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
        else:
            print("Something went wrong in db.py" + func+str(groups))
        try:
            self.cursor.execute(sql, var)
            self.conn.commit()
        except pymysql.err.DataError:
            print(var)
            input()
    def getfuncinfo(self,funcname):
        sql = 'SELECT `funcname`, `varlen` FROM funcinfo WHERE funcname = (%s)'
        try:
            self.cursor.execute(sql,funcname)
            self.conn.commit()
        except pymysql.err.DataError:
            print(funcname)
            print(pymysql.err.DataError)
            input()
    def buildFuncVarTypeXmlTable(self,funcanme,dllname,vartype,lenth):
        string1 = "/".join(vartype)
        var = tuple([funcanme,dllname,string1,int(lenth)])

        sql = 'INSERT INTO `funcinfo` (`funcname`,dllname,`vartype_mul`,varlen) VALUES (%s,%s,%s,%s)'
        try:
            self.cursor.execute(sql, var)
            self.conn.commit()
        except pymysql.err.DataError:
            print(vartype)
            print(funcanme)
            print(pymysql.err.DataError)
            input()
    def iffuncinfuncinfo(self,funcname,dllname=None):
        '''
        funcname,dllname,varlen,vartype_mul,rettype,vartype_sim,filename,implemented
        :param funcname:
        :param dllname:
        :return:
        '''
        if dllname == None:
            var = tuple([funcname])
            sql = 'select * from `funcinfo` where funcname = %s'
        else:
            var = tuple([funcname,dllname])
            sql = 'select * from `funcinfo` where funcname = %s and dllname = %s'
        try:
            self.cursor.execute(sql, var)
            print(self.cursor.rowcount)
            # print(len(self.cursor))

            for i in self.cursor:
                print(i[0])
        except pymysql.err.DataError:
            print(dllname)
            print(funcname)
            print(pymysql.err.DataError)
            input()

    def updateFuncInfoTable_Dll(self,funcname,dllname,rettype,vartype_sim,filename,implemented):
        var = tuple([rettype,vartype_sim,filename,implemented,funcname,dllname])

        sql = 'update `funcinfo` set `rettype` = %s,`vartype_sim` = %s,`filename` = %s,`implemented` = %s where funcname = %s and dllname = %s'
        try:
            self.cursor.execute(sql, var)
            self.conn.commit()
        except pymysql.err.DataError:
            print(filename)
            print(funcname)
            print(pymysql.err.DataError)
            input()

def main():

    test = bigDb()
    # test.buildFuncGroupTable("test12","00000")
    # test.iffuncinfuncinfo('testname','testdll')
    test.updateFuncInfoTable_Dll("testname","testdll","","","",0)
if __name__ == '__main__':
    main()