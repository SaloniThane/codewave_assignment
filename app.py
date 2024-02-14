from flask import Flask,render_template
import sqlite3 as sql
app=Flask(__name__)

@app.route("/")
def index():
    
    return render_template("index.html")
    

@app.route("/type_of_fit/<string:type_of_fit>", methods=['GET'])
def get_type(type_of_fit):
    con=sql.connect("flipkartdb.db")
    con.row_factory=sql.Row
    cur=con.cursor()

    table = ''
    success = ''
    message = ''

    if (type_of_fit == "relaxed") :
        table = "RelaxedFit"
    elif (type_of_fit == "regular"):
        table = "RegularFit"
    else :
        table = "Skip"

    if (table != "Skip") :
        # cur.execute("SELECT ap.product_name, ap.pid, ap.retail_price, ap.discounted_price, rf.ideal_for, rf.fabric FROM "+str(table)+" AS rf INNER JOIN AllProducts AS ap ON rf.uniq_id = ap.uniq_id;" )
        # cur.execute("SELECT uniq_id FROM "+str(table))
        cur.execute("SELECT ap.uniq_id, ap.pid, ap.product_name, rf.fabric, rf.ideal_for FROM  AllProducts as ap join " + str(table) + " as rf on rf.uniq_id = ap.uniq_id")

        data = cur.fetchall()
        # results = [tuple(row) for row in data]
        records = []
        for row in data:
            cols = {}
            for col in row.keys():
                cols[col] = row[col]
            records.append(cols)
        result = records
        success = True
        message = "Product details found"
        return {"success" : success, "message" : message,"data": result }
    else :
        success = False
        message = "Product details not found"
        return { "success" : success, "message" : message, "data": {} }
    
   
    
if __name__=='__main__':
    app.run(debug=True)
