import mysql.connector

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
        return myresult
    
    def get_column(self,table):
        sql="""SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'data_sample' ORDER BY ORDINAL_POSITION """.format(table)
        self.mycursor.execute(sql)
        myresult = self.mycursor.fetchall()
        myresult= list(map(lambda x:x[0],myresult))
        return myresult

    def get_sample(self,table):
        sql="SELECT * FROM {} limit 5".format(table)
        self.mycursor.execute(sql)
        myresult = self.mycursor.fetchall()
        return myresult
    
    def get_sample_table(self,table):
        col=self.get_column(table)
        print(col)
        sample=self.get_sample(table)
        output_string="Here is 5 sample rows of talbe name {table} \n \
        {col} \n \
        {sample}".format(table=table,col=col,sample=sample)
        return output_string

if __name__=="__main__":
    db=database()
    print(db.get_sample_table('data_sample'))

