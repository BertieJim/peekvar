import pymysql




class bigDb:
    def __init__(self):
        self.conn = pymysql.connect(user='root', password='12345', database='gaokao', charset='utf8')
        self.cursor = self.conn.cursor()
    def close(self):
        self.cursor.close()
        self.conn.close()
    def buildFuncGroupTable(self,func,num):
        sql = ('INSERT INTO peekvar.groupinfo(goup,num) VALUES (%s, %s)')
        self.cursor.execute(sql, (func, num))
        self.conn.commit()

