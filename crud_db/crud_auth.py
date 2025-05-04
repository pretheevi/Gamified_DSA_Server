import sqlite3
import random
import string
import resend
from datetime import datetime, timedelta
from query import create_connection_db
#____________________________________________________________________________________________________

class DBExecutor:
    @staticmethod
    def execute_query(query, params=(), fetch_one=False, fetch_all=False):
        conn = create_connection_db()
        if not conn:
            return None
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()

            if fetch_one:
                result = cursor.fetchone()
                return result
            if fetch_all:
                result = cursor.fetchall()
                return result

            return True
        except sqlite3.Error as e:
            print(f"SQLite Error: {e}")
            return None
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

#____________________________________________________________________________________________________

class crud_auth:
    #------------------------------------------------------------------------------------------------
    @staticmethod
    def Register(username: str, email: str, password: str):
        query = """
                INSERT INTO users (username, email, password, created_at, updated_at) 
                VALUES (?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                """
        try:
            params = (username, email, password)
            result = DBExecutor.execute_query(query, params)
            if result:
                print("DATABASE result : User successfully registered in SQLite database")
                return True
            else:
                print("DATABASE result : Error registering user in SQLite Database")
                return False
        except Exception as e:
            print(f"DATABASE result : Validation Error: {e}")
            return False  
    #------------------------------------------------------------------------------------------------
    @staticmethod
    def Login(email: str):
        query = """
                SELECT * FROM users WHERE email = ?
                """
        try:
            params = (email,)
            result = DBExecutor.execute_query(query, params, fetch_one=True)
            columns = ['id', 'username', 'email', 'password', 'created_at', 'updated_at']
            
            if result:
                print("DATABASE result : User successfully logged in")
                result_dict = dict(zip(columns, result))
                return result_dict
            else:
                print("DATABASE result : Invalid username or password")
                return False  # return False if user is not found or invalid credentials
            
        except Exception as e:
            print(f"Error: {e}")
            return False  # return False if any error occurs
    #------------------------------------------------------------------------------------------------
    @staticmethod
    def FindByEmail(email: str):
        query = """
                SELECT * FROM users WHERE email = ?
                """
        try:
            params = (email,)
            result = DBExecutor.execute_query(query, params, fetch_one=True)
            columns = ['id', 'username', 'email', 'password', 'created_at', 'updated_at']
            
            if result:
                print("DATABASE result : User found successfully")
                result_dict = dict(zip(columns, result))
                return result_dict
            else:
                print("DATABASE result : User not found")
                return False
        except Exception as e:
            print(f"DATABASE result : Validation Error: {e}")
            return False
    #------------------------------------------------------------------------------------------------
    @staticmethod
    def UpdatePassword(email, new_password):
        query = """
                UPDATE users
                SET password = ?, updated_at = CURRENT_TIMESTAMP
                WHERE email = ?
                """
        try:
            params = (new_password, email)
            result = DBExecutor.execute_query(query, params)
            if result:
                print("DATABASE result : Password successfully updated")
                return True
            else:
                print("DATABASE result : Error updating password")
                return False
        except Exception as e:
            print(f"DATABASE result : Validation Error: {e}")
            return False
#____________________________________________________________________________________________________

class OTP_handler:
    @staticmethod
    def GenerateExpiryTime():
        expiry_time = datetime.utcnow() + timedelta(minutes=10)    
        return expiry_time.strftime("%Y-%m-%d %H:%M:%S")
    #------------------------------------------------------------------------------------------------
    @staticmethod
    def GenerateOTP():
        numbers = string.digits               
        alphabets = string.ascii_uppercase       
        num_alpha = numbers + alphabets        
        OTP = "".join(random.choices(num_alpha, k=5))
        return OTP
    #------------------------------------------------------------------------------------------------
    @staticmethod
    def InsertOTP(email: str, otp: str, expires_at: str):
        query = """
                INSERT INTO otp_verification (email, otp, expires_at, created_at) 
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
                """
        try:
            params = (email, otp, expires_at)
            result = DBExecutor.execute_query(query, params)
            if result:
                print("DATABASE result : OTP successfully inserted")
                return True
            else:
                print("DATABASE result : Error inserting OTP")
                return False
        except Exception as e:
            print(f"DATABASE result : Validation Error: {e}")
            return False
    #------------------------------------------------------------------------------------------------
    @staticmethod
    def FindByEmailAndOTP(email: str, otp: str):
        query = """
                SELECT * FROM otp_verification 
                WHERE email = ? 
                AND otp = ?
                """
        try:
            params = (email, otp)
            result = DBExecutor.execute_query(query, params, fetch_one=True)
            columns = ['id', 'email', 'otp', 'expires_at', 'is_verified', 'created_at']

            if result:
                print("DATABASE result : OTP found successfully")
                result_dict = dict(zip(columns, result))
                return result_dict
            else:
                print("DATABASE result : OTP not found or expired")
                return False
        except Exception as e:
            print(f"DATABASE result : Validation Error: {e}")
            return False
    #------------------------------------------------------------------------------------------------
    @staticmethod
    def UpdateVerified(email: str, otp: str):
        query = """
            UPDATE otp_verification
            SET is_verified = 1
            WHERE email = ? AND otp = ?
        """
        try:
            params = (email, otp)
            result = DBExecutor.execute_query(query, params)
            if result:
                print("DATABASE result : OTP successfully updated as verified")
                return True
            else:
                print("DATABASE result : Error updating OTP verification status")
                return False
        except Exception as e:
            print(f"DATABASE result : Validation Error: {e}")
            return False
    #------------------------------------------------------------------------------------------------
    @staticmethod
    def VerifyOTP(email: str, otp: str):
        query = """
            SELECT * FROM otp_verification 
            WHERE email = ? 
            AND otp = ?
            AND is_verified = 0
            AND expires_at > CURRENT_TIMESTAMP
            LIMIT 1
        """
        try:
            params = (email, otp)
            result = DBExecutor.execute_query(query, params, fetch_one=True)
            columns = ['id', 'email', 'otp', 'expires_at', 'is_verified', 'created_at']

            if result:
                # OTP is valid, now mark as verified
                updated = OTP_handler.UpdateVerified(email, otp)
                if updated:
                    print("DATABASE result : OTP successfully verified and updated")
                    result_dict = dict(zip(columns, result))
                    return result_dict
                else:
                    print("DATABASE result : Error updating OTP status")
                    return False
            else:
                print("DATABASE result : Invalid or expired OTP")
                return False
        except Exception as e:
            print(f"DATABASE result : Validation Error: {e}")
            return False
        #------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------
    @staticmethod
    def CheckIfVerified(email: str):
        query = """
                SELECT * FROM otp_verification 
                WHERE email = ? 
                AND is_verified = 1
                """
        try:
            params = (email,)
            result = DBExecutor.execute_query(query, params, fetch_one=True)
            columns = ['id', 'email', 'otp', 'expires_at', 'is_verified', 'created_at']

            if result:
                print("DATABASE result : Email is verified")
                result_dict = dict(zip(columns, result))
                return result_dict
            else:
                print("DATABASE result : Email not verified")
                return False
        except Exception as e:
            print(f"DATABASE result : Validation Error: {e}")
            return False
#____________________________________________________________________________________________________

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailService:
    @staticmethod
    def send_otp_email(to_email, otp):
        # Email details
        from_email = "pretheeviraj0805@gmail.com"  # Your email address
        subject = "Test OTP Email"
        body = f"Your OTP is: {otp}\n\nPlease use this OTP to verify your email address.\n OTP is valid for 10 minutes.\n\nThank you!"

        # App password (generated)
        app_password = "ojwt pqmj lirw vdzp"  # Replace with the app password you generated

        # Set up the MIME structure of the email
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            # Connect to Gmail's SMTP server and send the email
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()  # Start TLS encryption
            server.login(from_email, app_password)  # Use your email and app password
            server.sendmail(from_email, to_email, msg.as_string())
            server.quit()
            return True  # Return True if email sent successfully
        except Exception as e:
            print(f"Error sending email: {e}")
            return False  # Return False if there was an error