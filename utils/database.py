import sqlite3, os
SAVE_FOLDER = "../database"
os.makedirs(SAVE_FOLDER, exist_ok=True)

def create_db(db_name):
    # Create a connection to the SQLite database
    db_path = os.path.join(SAVE_FOLDER, db_name)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Create a table to store job listings if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS job_listings
                (id INTEGER PRIMARY KEY,
                location TEXT,
                job_title TEXT,
                level TEXT,
                corporate TEXT,
                requirements TEXT)''')

    conn.commit()

    conn.close()
    return db_path
