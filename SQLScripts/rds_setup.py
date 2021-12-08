import pymysql

conn = pymysql.connect(host='charitystoredb.cchzjvmkb07e.us-east-1.rds.amazonaws.com',
            port=3306,
            user='admin',
            password='buckets1')

cursor = conn.cursor()

with open('SQLScripts/create_sellers.sql', 'r') as f:
    line = f.readline()
    while line:
        print(line)
        print(cursor.execute(line))
        line = f.readline()

with open('SQLScripts/create_products.sql', 'r') as f:
    line = f.readline()
    while line:
        print(line)
        print(cursor.execute(line))
        line = f.readline()

with open('SQLScripts/create_usersinfo.sql', 'r') as f:
    line = f.readline()
    while line:
        print(line)
        print(cursor.execute(line))
        line = f.readline()