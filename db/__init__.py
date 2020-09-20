# import pymysql
import mysql.connector

connection = mysql.connector.connect(port = 3309, user='root', passwd='hackmit', database='drug_data')
# connection = pymysql.connect(port = 3309, user='root', password='hackmit', db='drug_data')

drug_info_table_name = "DRUG_INFO"
drug_reviews_table_name = "DRUG_REVIEWS"