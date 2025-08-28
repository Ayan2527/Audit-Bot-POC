import json
from audit_scripts.db_connection import get_connection

def audit_roles():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT grantee, granted_role FROM dba_role_privs order by grantee")
    roles = []
    for row in cur:
        grantee, role = row
        risk = "High" if role in ["DBA", "IMP_FULL_DATABASE", "EXP_FULL_DATABASE"] else "Low"
        roles.append({
            "grantee": grantee,
            "role": role,
            "risk": risk
        })

    cur.close()
    conn.close()
    return {"roles": roles}

if __name__ == "__main__":
    print(json.dumps(audit_roles(), indent=2))
