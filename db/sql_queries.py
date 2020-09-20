from . import connection, drug_reviews_table_name, drug_info_table_name

def getReviews(drug_name=None, cond_name=None, nrows=10):
    command = f"SELECT * FROM {drug_reviews_table_name}"

    if drug_name is None and cond_name is None:
        pass
    elif drug_name is None:
        command += f" WHERE LOWER(cond) LIKE '%{cond_name}%'"
    elif cond_name is None:
        command += f" WHERE LOWER(drugName) LIKE '%{drug_name}%'"
    else:
        command += f" WHERE LOWER(drugName) LIKE '%{drug_name}%' AND LOWER(cond) LIKE '%{cond_name}%'"
    
    command += " ORDER BY usefulCount DESC"

    if nrows is not None:
        command += f" limit {nrows}"
    print(command)
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute(command)
        rows = cursor.fetchall()

    return rows

def getDrugNames(cond_name):
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute(f"select distinct(drugName) from {drug_reviews_table_name} where cond = '{cond_name}'")
        rows = cursor.fetchall()
    return rows

def getCondNames(drug_name):
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute(f"select distinct(cond) from {drug_reviews_table_name} where drugName = '{drug_name}'")
        rows = cursor.fetchall()
    return rows

def getDrugInfo(drug_name, nrows=10):
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute(f"select * from {drug_info_table_name} where " \
            f"LOWER(propName) LIKE '%{drug_name}%' OR " \
            f"LOWER(medName) LIKE '%{drug_name}%' LIMIT {nrows}")
        rows = cursor.fetchall()
    return rows