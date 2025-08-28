import json
from audit_scripts.db_connection import get_connection

def audit_passwords():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT username, account_status FROM dba_users")
    results = []
    for row in cur:
        username, status = row
        risk = "High" if status != "OPEN" else "Low"
        results.append({
            "username": username,
            "status": status,
            "risk": risk
        })

    cur.close()
    conn.close()
    return {"password_audit": results}

if __name__ == "__main__":
    print(json.dumps(audit_passwords(), indent=2))
