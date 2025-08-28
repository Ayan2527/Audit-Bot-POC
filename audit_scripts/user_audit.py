import json
from audit_scripts.db_connection import get_connection

def audit_users():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT username, account_status, created FROM dba_users")
    users = []
    for row in cur:
        username, status, created = row
        risk = "High" if username in ["SYS", "SYSTEM", "DBA", "IMP_FULL_DATABASE"] else "Low"
        users.append({
            "username": username,
            "status": status,
            "created": str(created),
            "risk": risk
        })

    cur.close()
    conn.close()
    return {"users": users}

if __name__ == "__main__":
    print(json.dumps(audit_users(), indent=2))
