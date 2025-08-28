#Connection file for the DB connection
import oracledb

def get_connection():
    return oracledb.connect(
        user="audit_bot",
        password="audit_bot123",
        dsn="140.245.5.226:1521/ORCLPDB1"
    )
