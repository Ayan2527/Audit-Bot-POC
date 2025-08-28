import json
from audit_scripts.db_connection import get_connection

def audit_sessions():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT username, machine, program FROM v$session WHERE username IS NOT NULL")
    sessions = []
    for row in cur:
        username, machine, program = row
        sessions.append({
            "username": username,
            "machine": machine,
            "program": program
        })

    cur.close()
    conn.close()
    return {"sessions": sessions}

if __name__ == "__main__":
    print(json.dumps(audit_sessions(), indent=2))
