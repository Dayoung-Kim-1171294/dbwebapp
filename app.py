from flask import Flask, render_template, request
import db, connect

app = Flask(__name__)
connection = db.init_db(app, user=connect.dbuser, password=connect.dbpass, host=connect.dbhost, database=connect.dbname)

@app.route('/')
def index():
    # Get page number from query parameter (default to 1)
    page = request.args.get('page', 1, type=int)
    per_page = 2  # 2 rows per page
    
    cur = db.get_cursor()
    cur.execute("SELECT * FROM tournament;")
    results = cur.fetchall()
    print(results)
    
    # Calculate pagination
    total_rows = len(results)
    total_pages = (total_rows + per_page - 1) // per_page  # Ceiling division
    
    # Ensure page is within valid range
    page = max(1, min(page, total_pages if total_pages > 0 else 1))
    
    # Get rows for current page
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_results = results[start_idx:end_idx]
    
    return render_template('results.html', 
                         tournaments=paginated_results,
                         page=page,
                         total_pages=total_pages,
                         total_rows=total_rows)
