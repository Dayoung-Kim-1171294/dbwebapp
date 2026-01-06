from flask import Flask, render_template
import db, connect

app = Flask(__name__)
connection = db.init_db(app, user=connect.dbuser, password=connect.dbpass, host=connect.dbhost, database=connect.dbname)

@app.route('/')
def index():
    cur = db.get_cursor()
    cur.execute("SELECT * FROM tournament;")
    results = cur.fetchall()
    print(results)
    return render_template('results.html', tournaments=results)
