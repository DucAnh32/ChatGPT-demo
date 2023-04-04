import mysql.connector
from tabulate import tabulate
def get_sql_from_msg(msg):
    idx1 = msg.find("```")
    idx2 = msg.rfind("```")
    sql = msg[idx1 + 3:idx2].replace('\n', ' ')
    idx = sql.find("SELECT")
    sql = sql[idx:]
    return sql

def get_alias_or_not(res):
    if ' as ' in res.lower():
        index=res.lower().find(' as ')
        return res[index+4:]
    return res

def sql_response_analyze(sql,sql_response):
    index2 = sql.rfind('FROM')
    list_col = (sql[7:index2].split(', '))
    headers = []
    for col in list_col:
        headers.append(get_alias_or_not(col))
    print(headers)
    return tabulate(sql_response, headers=headers)


class database():
    def __init__(self) -> None:
        self.mydb = mysql.connector.connect(
        host="localhost",
        port="3306",
        user="root",
        password="vcbdac2023",
        database="testdb"
        )
        self.mycursor = self.mydb.cursor()
    def get_table(self):
        self.mycursor.execute("show tables")
        myresult = self.mycursor.fetchall()
        myresult = list(map(lambda x: x[0], myresult))
        return myresult
    
    def get_column(self,table):
        sql="SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{}' ORDER BY ORDINAL_POSITION ".format(table)
        self.mycursor.execute(sql)
        myresult = self.mycursor.fetchall()
        myresult= list(map(lambda x:x[0],myresult))
        return myresult

    def get_sample_table(self,table):
        sql="SELECT * FROM {} limit 5".format(table)
        self.mycursor.execute(sql)
        myresult = self.mycursor.fetchall()
        return myresult
    
    def get_sample(self):
        output_string=''
        for table in self.get_table():
            col=self.get_column(table)
            col=','.join(col)
            sample=self.get_sample_table(table)
            output_string+="Here is 5 sample rows of talbe name {table} \n \
            {col} \n \
            {sample} \n".format(table=table,col=col,sample=sample)
        return output_string

    def execute_sql(self,sql):
        self.mycursor.execute(sql)
        myresult = self.mycursor.fetchall()
        return myresult

if __name__=="__main__":
    db=database()
    print(db.execute_sql('SELECT FLOOR(Age/10)*10 AS age_group, COUNT(*) AS number_of_customers FROM data_sample GROUP BY age_group;'))

