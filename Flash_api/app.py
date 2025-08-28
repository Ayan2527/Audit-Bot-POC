from flask import Flask, jsonify
from audit_scripts.risk_engine import run_full_audit
from audit_scripts.user_audit import audit_users
from audit_scripts.password_audit import audit_passwords
from audit_scripts.role_audit import audit_roles
from audit_scripts.session_audit import audit_sessions

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Audit Bot API is running!"})

# 🔹 Full audit
@app.route('/audit', methods=['GET'])
def full_audit():
    try:
        results = run_full_audit()
        return jsonify({"status": "success", "data": results})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# 🔹 User audit only
@app.route('/audit/users', methods=['GET'])
def user_audit():
    try:
        results = audit_users()
        return jsonify({"status": "success", "data": results})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# 🔹 Password audit only
@app.route('/audit/passwords', methods=['GET'])
def password_audit():
    try:
        results = audit_passwords()
        return jsonify({"status": "success", "data": results})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# 🔹 Role audit only
@app.route('/audit/roles', methods=['GET'])
def role_audit():
    try:
        results = audit_roles()
        return jsonify({"status": "success", "data": results})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# 🔹 Session audit only
@app.route('/audit/sessions', methods=['GET'])
def session_audit():
    try:
        results = audit_sessions()
        return jsonify({"status": "success", "data": results})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    # Accessible externally
    app.run(host="0.0.0.0", port=5000, debug=True)
