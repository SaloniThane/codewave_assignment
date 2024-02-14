import sqlite3
import pandas as pd
import ast
import json

df = pd.read_csv('flipkart.csv' ,encoding  = "utf-8-sig'")

con = sqlite3.connect('flipkartdb.db')

index = df.columns.get_loc("product_specifications") + 1

df.to_sql('AllProducts',con,if_exists='replace')

cursor = con.cursor()

cursor.execute("DROP TABLE IF EXISTS RelaxedFit")

sql ='''CREATE TABLE RelaxedFit(
   uniq_id CHAR(200) NOT NULL,
   fabric CHAR(200),
   ideal_for CHAR(200)
)'''
cursor.execute(sql)

cursor.execute("DROP TABLE IF EXISTS RegularFit")

sql ='''CREATE TABLE RegularFit(
   uniq_id CHAR(200) NOT NULL,
   fabric CHAR(200),
   ideal_for CHAR(200)
)'''
cursor.execute(sql)

cursor.execute("DROP TABLE IF EXISTS CheckProducts")
sql ='''CREATE TABLE CheckProducts(
   uniq_id CHAR(200) NOT NULL
)'''
cursor.execute(sql)

cursor.execute("SELECT * FROM AllProducts")
rows = cursor.fetchall()

for row in rows:
    if row[index] is not None and row[index].find("=>nil") ==-1  :
        array_of_objects = json.loads(row[index].replace("=>",':'))
        cursor.execute("insert into CheckProducts values (?)", [row[1]])
        fabric = ''
        ideal_for = ''
        table = 'Skip'
        regular_fit = ["regular", "regular fit"]
        relaxed_fit = ["relaxed", "relaxed fit"]
        for x in array_of_objects['product_specification']:

            if (type(x) == dict):
                value = x.get('key')

            if value is not None and value =='Fit' and x.get('value').lower() in relaxed_fit:
                table = "RelaxedFit"
            elif value is not None and value =='Fit' and x.get('value').lower() in regular_fit:
                table = "RegularFit"
            elif value is not None and value =='Fit' and x.get('value').lower() not in regular_fit and  x.get('value').lower() not in relaxed_fit:
                table = "Skip"
            
            if value is not None and value =='Fabric':
                kval = x.get('value')
                fabric = kval
            if value is not None and value =='Ideal For':
                kval = x.get('value')
                ideal_for = kval

    if table !='Skip': 
        cursor.execute("insert into "+ str(table) +" values (?, ?, ?)", [row[1], fabric, ideal_for])

print("completed")
# Commit your changes in the database
con.commit()

# Closing the connection
con.close()


