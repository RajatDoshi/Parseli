#setup for google cloud sql
#Follow this: https://cloud.google.com/sql/docs/mysql/connect-external-app
#do step 1
#do step 2
#run "gcloud auth login" command to authenticate the Cloud SDK. Use your yale email
#do 7. Specifically run "./cloud_sql_proxy -instances=galvanic-axle-290004:us-west2:health-hack=tcp:3309 &"
#You are connected, so you can use the code below 

from . import connection, drug_info_table_name, drug_reviews_table_name

import pandas as pd
from tqdm import tqdm
from datetime import datetime

# print("start_success")
# connection = pymysql.connect(port = 3309, user='root', password='hackmit', db='drug_data')

# print("end_success")

def createDrugInfoTable():
    with connection.cursor() as cursor:
        #this will create a table within the drug_data database
        print('Connection opened')
        cursor.execute(f"DROP TABLE IF EXISTS {drug_info_table_name};")
        print('Dropped table')
        cursor.execute(f"""CREATE TABLE {drug_info_table_name} ( 
            id int PRIMARY KEY AUTO_INCREMENT,
            drugCode VARCHAR(10), 
            productType VARCHAR(1000), 
            propName VARCHAR(1000), 
            medName  VARCHAR(1000),
            dosage VARCHAR(1000),
            administered TEXT(65535), 
            substance TEXT(65535), 
            strength TEXT(65535), 
            unit TEXT(65535));""")
        print('Database created successfully')

        df = pd.read_csv("/Users/agong/research/hackmit2020/hackMIT/datasets/Drug_data_table.csv")

        values = []
        for i, row in tqdm(df.iterrows()):
            # print(tuple(row))
            values.append([None if pd.isnull(x) else x for x in tuple(row)[1:]])

        command = f"""INSERT INTO {drug_info_table_name} 
            (drugCode, productType, propName, medName, dosage, administered, substance, strength, unit) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        cursor.executemany( command, values )
        connection.commit()


        # with connection.cursor() as cursor:
        #     #this will create a table within the drug_data database
        #     cursor.execute(f"CREATE TABLE {drug_info_table_name} (INDEX_c int, Code CHAR(255), DType CHAR(255), Name CHAR(255), Administered CHAR(255), MName CHAR(255), Dosage CHAR(255), Istrength CHAR(255))")

        #     all_drug_data = pd.read_csv("Drug_data_table.csv")
        #     all_drug_data = all_drug_data.dropna().head(1000)
        #     all_drug_data = all_drug_data.drop(columns = ["Substance", "Active Ingredient Unit"])
        #     rows_drug_data = list(all_drug_data.itertuples(index=False, name=None))
        #     for row in rows_drug_data:
        #         cursor.execute(f"INSERT INTO {drug_info_table_name} (INDEX_c, Code, DType, Name, MName, Dosage, Administered, Istrength) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (row[0], row[1][0:255], row[2][0:255], row[3][0:255], row[4][0:255], row[5][0:255], row[6][0:255], row[7][0:255]));
        #     connection.commit()

        #     cursor.execute("select * from drugfacts_allinfo")
        #     rows = cursor.fetchall()
        #     for row in rows:
        #         print(row)

def createDrugReviewsTable():
    with connection.cursor() as cursor:
        #this will create a table within the drug_data database
        print('Connection opened')
        cursor.execute(f"DROP TABLE IF EXISTS {drug_reviews_table_name};")
        print('Dropped table')
        cursor.execute(f"""CREATE TABLE {drug_reviews_table_name} ( 
            id int PRIMARY KEY, 
            drugName VARCHAR(1000), 
            cond VARCHAR(1000), 
            review TEXT(65535), 
            rating int, 
            date DATE, 
            usefulCount int);""")
        print('Databases created successfully')

        df = pd.read_csv("/Users/agong/research/hackmit2020/Drug_Review_Dataset/drugsComTest_raw.csv", nrows=1000)

        for i, row in tqdm(df.iterrows()):
            # print(tuple(row))
            try:
                dt = datetime.strptime(row['date'], "%d-%b-%y")
                date_str = dt.strftime("%Y-%m-%d")
            except ValueError:
                date_str = None

            command = f"""INSERT INTO {drug_reviews_table_name} 
                (id, drugName, cond, review, rating, date, usefulCount) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            values = (
                row['uniqueID'], row['drugName'], row['condition'], 
                row['review'], row['rating'], date_str, row['usefulCount']
            )
            values = [None if pd.isnull(x) else x for x in values]
            cursor.execute( command, values )
        connection.commit()

        # cursor.execute("select * from DRUG_REVIEWS limit 10;")
        # rows = cursor.fetchall()
        # for row in rows:
        #     print(row)

if __name__ == "__main__":
    # createDrugInfoTable()
    # createDrugReviewsTable()

    with connection.cursor(dictionary=True) as cursor:
        cursor.execute(f"select * from {drug_info_table_name} limit 10;")
        rows = cursor.fetchall()
        for row in rows:
            print(row)