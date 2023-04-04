import mysql.connector


mydb = mysql.connector.connect(
host="localhost",
port="3306",
user="root",
password="vcbdac2023",
database="testdb"
)
mycursor = mydb.cursor()


mycursor.execute("show tables")

myresult = mycursor.fetchall()


sql="SELECT * FROM {}".format(myresult[0][0])
mycursor.execute(sql)
myresult = mycursor.fetchall()




