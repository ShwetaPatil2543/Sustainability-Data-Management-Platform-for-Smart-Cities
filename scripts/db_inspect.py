import os, sqlite3, json
p = 'db.sqlite3'
full = os.path.join(os.path.dirname(__file__), '..', p)
full = os.path.abspath(full)
print('db_path:', full)
print('exists:', os.path.exists(full))
if os.path.exists(full):
    print('size_bytes:', os.path.getsize(full))
    conn = sqlite3.connect(full)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [r[0] for r in cur.fetchall()]
    print('tables:', json.dumps(tables))
    # print some sample from emissions if table exists
    if 'emissions_carbonemission' in tables:
        cur.execute('SELECT id, industry_id, date, co2_emission, methane_emission, nitrous_oxide, created_at FROM emissions_carbonemission ORDER BY created_at DESC LIMIT 10')
        rows = cur.fetchall()
        print('recent_emissions:', json.dumps(rows, default=str))
    conn.close()
