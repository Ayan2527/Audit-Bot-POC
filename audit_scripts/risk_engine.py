import json
from audit_scripts.user_audit import audit_users
from audit_scripts.role_audit import audit_roles
from audit_scripts.password_audit import audit_passwords
from audit_scripts.session_audit import audit_sessions

def run_full_audit():
    return {
        "users": audit_users(),
        "roles": audit_roles(),
        "passwords": audit_passwords(),
        "sessions": audit_sessions()
    }

if __name__ == "__main__":
    print(json.dumps(run_full_audit(), indent=2))
