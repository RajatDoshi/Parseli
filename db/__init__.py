# import pymysql
import mysql.connector

connection = mysql.connector.connect(port = 3309, user='root', passwd='hackmit', database='drug_data')
drug_info_table_name = "drugfacts_allinfo"
drug_reviews_table_name = "DRUG_REVIEWS"