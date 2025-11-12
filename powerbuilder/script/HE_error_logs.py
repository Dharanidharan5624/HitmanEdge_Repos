from datetime import datetime
import traceback
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from HE_database_connect import get_connection

try:
    from HE_database_connect import get_connection
except ImportError as e:
    print(f"[ERROR] Cannot import get_connection: {e}")
    sys.exit(1)

def log_error_to_db(file_name, error_description=None, created_by=None, env="dev"):
    try:
        if error_description is None:
            error_description = traceback.format_exc()
        if not created_by:
            created_by = os.getenv("USERNAME", "system")

        conn = get_connection(env=env)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO he_error_logs (file_name, error_description, created_at, created_by)
            VALUES (%s, %s, %s, %s)
        """, (file_name, error_description, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), created_by))

        conn.commit()
        print(f"[INFO] Error logged from {file_name} by {created_by}")

    except Exception as db_err:
        print(f"[ERROR] Failed to log error: {db_err}")
        print(traceback.format_exc())
    finally:
        try:
            if cursor: cursor.close()
            if conn: conn.close()
        except: pass

# from datetime import datetime
# import traceback
# import os
# import sys
# sys.path.append(os.path.abspath(os.path.dirname(__file__)))
# from HE_database_connect import get_connection

# try:
#     from HE_database_connect import get_connection
# except ImportError as e:
#     print(f"[ERROR] Cannot import get_connection: {e}")
#     sys.exit(1)

# def log_error_to_db(file_name, error_description=None, created_by=None, env="dev"):
#     conn = None
#     cursor = None
#     try:
#         if error_description is None:
#             error_description = traceback.format_exc()

#         # Default username (if not passed)
#         if not created_by:
#             created_by = os.getenv("USERNAME", "system")

#         # Connect to DB
#         conn = get_connection(env=env)
#         cursor = conn.cursor()

#         # Find user_id from username
#         cursor.execute("SELECT id FROM he_usermaster WHERE username = %s LIMIT 1", (created_by,))
#         user_row = cursor.fetchone()
#         user_id = user_row[0] if user_row else None

#         # If user_id not found, set to NULL (or default system id)
#         if not user_id:
#             print(f"[WARNING] User '{created_by}' not found in he_usermaster table. Using NULL for created_by.")
        
#         # Insert error log
#         cursor.execute("""
#             INSERT INTO he_error_logs (file_name, error_description, created_at, created_by)
#             VALUES (%s, %s, %s, %s)
#         """, (file_name, error_description, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), user_id))

#         conn.commit()
#         print(f"[INFO] Error logged from {file_name} by user_id={user_id} ({created_by})")

#     except Exception as db_err:
#         print(f"[ERROR] Failed to log error: {db_err}")
#         print(traceback.format_exc())
#     finally:
#         try:
#             if cursor: cursor.close()
#             if conn: conn.close()
#         except: 
#             pass

