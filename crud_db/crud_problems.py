import sqlite3
# from crud_db.problem_data import problem_data
from query import create_connection_db

class DBExecutor:
    @staticmethod
    def execute_query(query, params=None, fetch_all=False):
        conn = create_connection_db()
        cursor = conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            if fetch_all:
                return cursor.fetchall()
            conn.commit()
        except sqlite3.Error as e:
            print(f"SQLite error occurred: {e}")
        finally:
            cursor.close()
            conn.close()

class Problems:
    @staticmethod
    def insert_problem(title, slug, url, topic, difficulty, xp_value):
        query = """
                INSERT INTO problems (title, slug, url, topic, difficulty, xp_value)
                VALUES (?, ?, ?, ?, ?, ?)
                """
        params = (title, slug, url, topic, difficulty, xp_value)
        try:
            # DBExecutor.execute_query(query, params)
            print(f"Problem '{title}' inserted successfully.")
        except sqlite3.Error as e:
            print(f"SQLite error occurred while inserting problem '{title}': {e}")
    
    @staticmethod
    def get_all_problems(user_id: int):
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
            result = DBExecutor.execute_query(query, params=(user_id,), fetch_all=True)
            return result
        except sqlite3.Error as e:
            print(f"SQLite error occurred while fetching problems: {e}")
            return None

# Insert all problems
# def insert_all_problems():
#     for problem in problem_data:
#         Problems.insert_problem(
#             problem['title'],
#             problem['slug'],
#             problem['url'],
#             problem['topic'],
#             problem['difficulty'],
#             problem['xp_value']
#         )