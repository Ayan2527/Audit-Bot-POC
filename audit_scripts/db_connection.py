import oracledb

def get_connection():
    return oracledb.connect(
        user="audit_bot",
        password="auditbot123",
        dsn="127.0.0.1:1521/orclpdb1"
    )
