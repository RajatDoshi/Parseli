#setup for google cloud sql
#Follow this: https://cloud.google.com/sql/docs/mysql/connect-external-app
#do step 1
#do step 2
#run "gcloud auth login" command to authenticate the Cloud SDK. Use your yale email
#do 7. Specifically run "./cloud_sql_proxy -instances=galvanic-axle-290004:us-west2:health-hack=tcp:3309 &"
#You are connected, so you can use the code below 

import pymysql
print("start_success")
connection = pymysql.connect(port = 3309, user='root', password='hackmit', db='drug_data')

print("end_success")

with connection.cursor() as cursor:
	#this will create a table within the drug_data database
    cursor.execute("CREATE TABLE table_name (col1 INT)")

    #this will insert values into the table. You can iterate over values using a for loop
    cursor.execute("INSERT INTO table_name (col1) VALUES (4)")

    #iterate thorugh a select * statement
    for value in cursor.execute("SELECT * from table_name"):
        print(value)







