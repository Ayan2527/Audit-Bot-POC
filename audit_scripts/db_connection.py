#Connection file for the DB connection
import oracledb

def get_connection():
    return oracledb.connect(
        user="audit_bot",
        password="audit_bot123",
        dsn="140.245.5.226:1521/ORCLPDB1"
    )

if __name__ == "__main__":
    try:
        conn = get_connection()
        print("✅ Connection successful!")
        print("Database version:", conn.version)
        conn.close()
    except Exception as e:
        print("❌ Connection failed:", str(e))
