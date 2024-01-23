import mysql.connector

conection = mysql.connector.connect(user= 'root', password= 'erick2003',
                                   host='localhost',
                                   database= 'Marketing',
                                   port= '3306')
#print (conection) 