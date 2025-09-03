# audit_scripts/user.py
from flask import Blueprint, jsonify
from audit_scripts.db_connection import get_connection

user_bp = Blueprint("user", __name__)

@user_bp.route("/api/user-info", methods=["GET"])
def get_users_with_roles():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # 1. Get user info
        cursor.execute("""
            SELECT username, account_status, created
            FROM dba_users
        """)
        users_data = cursor.fetchall()

        # 2. Get roles info (who has what role)
        cursor.execute("""
            SELECT grantee, granted_role
            FROM dba_role_privs
        """)
        roles_data = cursor.fetchall()

        # Convert roles to dictionary {username: [roles]}
        roles_map = {}
        for grantee, role in roles_data:
            if grantee not in roles_map:
                roles_map[grantee] = []
            roles_map[grantee].append(role)

        # 3. Build response
        users = []
        for username, status, created in users_data:
            users.append({
                "username": username,
                "status": status,
                "risk": "High" if "OPEN" in status or "DBA" in roles_map.get(username, []) else "Low",
                "created": str(created),
                "roles": roles_map.get(username, [])
            })

        return {"status": "success", "data": {"users": users}}

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
