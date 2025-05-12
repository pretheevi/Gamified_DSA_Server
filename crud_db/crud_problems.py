import sqlite3
# from crud_db.problem_data import problem_data
from query import create_connection_db

class DBExecutor:
    @staticmethod
    def execute_query(query, params=None, fetch_all=False, fetch_one=False, return_cursor=False):
        conn = create_connection_db()
        cursor = conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            if fetch_all:
                results = cursor.fetchall()
                return results

            if fetch_one:
                result = cursor.fetchone()
                return result

            conn.commit()

            if return_cursor:
                return cursor  # Return the cursor so caller can access cursor.rowcount

        except sqlite3.Error as e:
            print(f"SQLite error occurred: {e}")
            raise

        finally:
            # Don't close the cursor if it's returned
            if not return_cursor:
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

    @staticmethod
    def check_problem_row_already_exists(user_id: int, problem_id: int):
        query = """
            SELECT status, time_spent FROM user_problem_progress
            WHERE user_id = ? AND problem_id = ?
        """
        params = (user_id, problem_id)
        try:
            result = DBExecutor.execute_query(query, params, fetch_one=True)
            if result is None:
                return False
            return result
        except sqlite3.Error as e:
            print(f"SQlite error occurred while fetching problem: {e}")
            return False

    @staticmethod
    def insert_new_problem_progress_row(user_id: int, problem_id: int, time_spend: int):
        query = """
            INSERT INTO user_problem_progress (
                user_id, problem_id, status, time_spent, last_updated
            ) VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        """
        params = (user_id, problem_id, "In Progress", time_spend)
        try:
            DBExecutor.execute_query(query, params)
            return True
        except sqlite3.Error as e:
            print(f"SQlite error occurred while fetching problem: {e}")
            return False

    @staticmethod
    def update_time_spend(user_id: int, problem_id: int, status: str, added_time: int):
        query = """
            UPDATE user_problem_progress
            SET status = ?, time_spent = time_spent + ?, last_updated = CURRENT_TIMESTAMP
            WHERE user_id = ? AND problem_id = ?
        """
        params = (status, added_time, user_id, problem_id)
        try:
            DBExecutor.execute_query(query, params)
            return True
        except sqlite3.Error as e:
            print(f"SQlite error occurred while fetching problem: {e}")
            return False
    
    @staticmethod
    def update_status_solved(user_id: int, problem_id: int, status: str):
        query = """
            UPDATE user_problem_progress
            SET status = ?, last_updated = CURRENT_TIMESTAMP
            WHERE user_id = ? AND problem_id = ?
        """
        params = (status, user_id, problem_id)
        try:
            cursor = DBExecutor.execute_query(query, params, return_cursor=True)
            if cursor.rowcount == 0:
                print("Update failed: No matching problem for the user.")
                return False
            print(f"✅ Updated: user_id={user_id}, problem_id={problem_id}, status='{status}'")
            return True
        except sqlite3.Error as e:
            print(f"❌ SQLite Error during update: {e}")
            return False

