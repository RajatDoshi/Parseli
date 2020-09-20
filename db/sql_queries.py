from . import connection, drug_reviews_table_name

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
        cursor.execute(f"select distinct(drugName) from DRUG_REVIEWS where cond = '{cond_name}'")
        rows = cursor.fetchall()
    return rows

def getCondNames(drug_name):
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute(f"select distinct(cond) from DRUG_REVIEWS where drugName = '{drug_name}'")
        rows = cursor.fetchall()
    return rows
