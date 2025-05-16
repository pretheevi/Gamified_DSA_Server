import sqlite3

def create_connection_db():
    """
    Creates and returns a connection to the SQLite database.
    
    Returns:
        sqlite3.Connection: The connection object or None if connection failed
    """
    try:
        conn = sqlite3.connect("database.db")
        print("DATABASE result : Connected to SQLite Database")
        return conn
    except sqlite3.Error as e:
        print(f"DATABASE result : Error connecting to SQLite Database: {e}")
        return None
#____________________________________________________________________________________________________

def execute_query(query):
    conn = create_connection_db()
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"SQLite Error: {e}")
        return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
#____________________________________________________________________________________________________

def create_user_table():
    query = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT UNIQUE,
            password TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """
    if execute_query(query):
        print("User table successfully created in SQLite database")
    else:
        print("Error creating user table in SQLite Database")
    return None
#____________________________________________________________________________________________________

def create_problems_table():
    query = """
        CREATE TABLE IF NOT EXISTS problems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            slug TEXT UNIQUE NOT NULL,
            url TEXT NOT NULL,
            topic TEXT,
            difficulty TEXT CHECK(difficulty IN ('Easy', 'Medium', 'Hard')),
            xp_value INTEGER DEFAULT 10
        );
    """
    if execute_query(query):
        print("Problems table successfully created in SQLite database")
    else:
        print("Error creating problems table in SQLite Database")
    return None 
#____________________________________________________________________________________________________

def create_user_problem_progress_table():
    query = """
        CREATE TABLE IF NOT EXISTS user_problem_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            problem_id INTEGER NOT NULL,
            status TEXT CHECK(status IN ('Not Started', 'In Progress', 'Solved')) DEFAULT 'Not Started',
            time_spent INTEGER DEFAULT 0,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (problem_id) REFERENCES problems(id),
            UNIQUE(user_id, problem_id)
        );
    """
    if execute_query(query):
        print("User problem progress table successfully created in SQLite database")
    else:
        print("Error creating user problem progress table in SQLite Database")
    return None
#____________________________________________________________________________________________________

def create_otp_table():
    query = """
        CREATE TABLE IF NOT EXISTS otp_verification (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            otp TEXT NOT NULL,
            expires_at DATETIME NOT NULL,
            is_verified BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(email, otp)
        );
    """
    if execute_query(query):
        print("OTP verification table successfully created in SQLite database")
    else:
        print("Error creating OTP verification table in SQLite Database")
    return None
    
#____________________________________________________________________________________________________

def view_table_data(table_name):
    conn = create_connection_db()
    cursor = conn.cursor()
    try:
        query = f"SELECT * FROM {table_name};"
        cursor.execute(query)
        rows = cursor.fetchall()
        print(f"\nData from '{table_name}' table:")
        for row in rows:
            print(row)
        print(f"Total rows: {len(rows)}")

    except sqlite3.Error as e:
        print(f"Error fetching data from {table_name}: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
#____________________________________________________________________________________________________

def check_table_schema(table_name):
    conn = create_connection_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute(f"PRAGMA table_info({table_name});")
        schema = cursor.fetchall()
        print(f"\nSchema for '{table_name}' table:")
        for col in schema:
            print(col)
    except sqlite3.Error as e:
        print(f"Error fetching schema: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
#____________________________________________________________________________________________________

def setup_database():
    create_user_table()
    create_problems_table()
    create_user_problem_progress_table()
    create_otp_table()

#

def testing():
    query = """
        SELECT 
            p.id, 
            p.title, 
            p.slug,
            p.url,
            p.topic,
            p.difficulty, 
            p.xp_value, 
            up.id AS user_problem_progress_id,
            up.user_id,
            CASE 
                WHEN up.id IS NULL THEN 'Not Started'
                ELSE up.status
            END AS status,
            COALESCE(up.time_spent, 0) AS time_spent,
            COALESCE(up.last_updated, '0') AS last_updated
        FROM problems as p
        LEFT JOIN user_problem_progress as up
            ON p.id = up.problem_id AND up.user_id = ?
        ORDER BY p.id ASC;
    """
    try:
        conn = create_connection_db()
        cursor = conn.cursor()
        user_id = 4  # 👈 Dynamically pass this in real code
        cursor.execute(query, (user_id,))
        rows = cursor.fetchall()
        print("Query executed successfully")
        for row in rows:
            format_row = {
                "problem_id": row[0],
                "title": row[1],
                "slug": row[2],
                "url": row[3],
                "topic": row[4],
                "difficulty": row[5],
                "xp_value": row[6],
                "user_problem_progress_id": row[7],
                "user_id": row[8],
                "status": row[9],
                "time_spent": row[10],
                "last_updated": row[11]
            }
            print(format_row)
    except sqlite3.Error as e:
        print(f"SQLite error occurred: {e}")
        return None
    

def AlterTable():
    query = """
        DELETE FROM users;
    """
    if execute_query(query):
        print("Column 'status' successfully added to user_problem_progress table")
    else:
        print("Error adding column to user_problem_progress table")
    return None


from crud_db.problem_data import problem_data;

def Insert_all_problem_data():
    conn = create_connection_db()
    cursor = conn.cursor()
    insert_query = """
        INSERT OR IGNORE INTO problems (title, slug, url, topic, difficulty, xp_value)
        VALUES (?, ?, ?, ?, ?, ?);
    """
    try:
        for p in problem_data:
            cursor.execute(insert_query, (
                p['title'], 
                p['slug'], 
                p['url'], 
                p.get('topic'), 
                p.get('difficulty'), 
                p.get('xp_value', 10)
            ))
        conn.commit()
        print(f"Inserted {len(problem_data)} problems into the database.")
    except sqlite3.Error as e:
        print(f"Error inserting problem data: {e}")
    finally:
        cursor.close()
        conn.close()   
        pass

if __name__ == "__main__":
    Insert_all_problem_data()
    pass
#____________________________________________________________________________________________________