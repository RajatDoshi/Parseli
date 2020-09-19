#setup for google cloud sql
#Follow this: https://cloud.google.com/sql/docs/mysql/connect-external-app
#do step 1
#do step 2
#run "gcloud auth login" command to authenticate the Cloud SDK. Use your yale email
#do 7. Specifically run "./cloud_sql_proxy -instances=galvanic-axle-290004:us-west2:health-hack=tcp:3309 &"
#You are connected, so you can use the code below 
import pandas as pd
import pymysql
print("start_success")
connection = pymysql.connect(port = 3309, user='root', password='hackmit', db='drug_data')

print("end_success")

with connection.cursor() as cursor:
	#this will create a table within the drug_data database
    cursor.execute("CREATE TABLE drugfacts_allinfo (INDEX_c int, Code CHAR(255), DType CHAR(255), Name CHAR(255), Administered CHAR(255), MName CHAR(255), Dosage CHAR(255), Istrength CHAR(255))")

    all_drug_data = pd.read_csv("Drug_data_table.csv")
    all_drug_data = all_drug_data.dropna().head(1000)
    all_drug_data = all_drug_data.drop(columns = ["Substance", "Active Ingredient Unit"])
    rows_drug_data = list(all_drug_data.itertuples(index=False, name=None))
    for row in rows_drug_data:
    	cursor.execute("INSERT INTO drugfacts_allinfo (INDEX_c, Code, DType, Name, MName, Dosage, Administered, Istrength) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (row[0], row[1][0:255], row[2][0:255], row[3][0:255], row[4][0:255], row[5][0:255], row[6][0:255], row[7][0:255]));
    connection.commit()

    cursor.execute("select * from drugfacts_allinfo")
    rows = cursor.fetchall()
    for row in rows:
    	print(row)







