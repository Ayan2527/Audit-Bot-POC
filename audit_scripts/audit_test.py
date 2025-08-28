import oracledb
import json
import datetime

# connect to DB
conn = oracledb.connect(
    user="audit_bot",
    password="auditbot123",
    dsn="127.0.0.1:1521/orclpdb1"
)
cur = conn.cursor()

# ============================
# 1. Fetch all users
# ============================
cur.execute("SELECT username FROM dba_users")
users = [row[0] for row in cur]

# ============================
# 2. Risk scoring
# ============================
risk_map = {}
for user in users:
    if user in ["SYS", "SYSTEM", "DBA", "IMP_FULL_DATABASE"]:
        risk_map[user] = "High"
    else:
        risk_map[user] = "Low"

# ============================
# 3. Account status
# ============================
cur.execute("SELECT username, account_status, expiry_date, profile FROM dba_users")
user_status = {}
for row in cur:
    user_status[row[0]] = {
        "account_status": row[1],
        "expiry_date": str(row[2]),
        "profile": row[3]
    }

# ============================
# 4. Roles assigned
# ============================
cur.execute("SELECT grantee, granted_role FROM dba_role_privs")
role_map = {}
for grantee, role in cur:
    role_map.setdefault(grantee, []).append(role)

# ============================
# 5. System privileges
# ============================
cur.execute("SELECT grantee, privilege FROM dba_sys_privs")
sys_priv_map = {}
for grantee, priv in cur:
    sys_priv_map.setdefault(grantee, []).append(priv)

# ============================
# 6. Object privileges
# ============================
cur.execute("SELECT grantee, privilege, owner, table_name FROM dba_tab_privs")
tab_priv_map = {}
for grantee, priv, owner, table in cur:
    tab_priv_map.setdefault(grantee, []).append(
        {"privilege": priv, "object": f"{owner}.{table}"}
    )

# ============================
# Assemble per-user report
# ============================
user_reports = {}
for user in users:
    user_reports[user] = {
        "risk": risk_map.get(user, "Low"),
        "account_status": user_status.get(user, {}).get("account_status", "UNKNOWN"),
        "expiry_date": user_status.get(user, {}).get("expiry_date", None),
        "profile": user_status.get(user, {}).get("profile", None),
        "roles": role_map.get(user, []),
        "system_privileges": sys_priv_map.get(user, []),
        "object_privileges": tab_priv_map.get(user, [])
    }

# ============================
# Final JSON Output
# ============================
output = {
    "status": "success",
    "timestamp": datetime.datetime.now().isoformat(),
    "users": user_reports
}

print(json.dumps(output, indent=2))

# close connection
conn.close()
