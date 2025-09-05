import json
from audit_scripts.db_connection import get_connection


def get_tablespace_info():
    """
    Fetch tablespace usage details per user and tablespace.
    Returns list of dicts with username, tablespace, allocated, used, pct_used.
    """
    query = """
        SELECT 
            u.username,
            q.tablespace_name,
            ROUND(SUM(d.bytes) / 1024 / 1024, 2) AS allocated_mb,
            ROUND((SUM(d.bytes) - NVL(f.free_bytes, 0)) / 1024 / 1024, 2) AS used_mb,
            ROUND(((SUM(d.bytes) - NVL(f.free_bytes, 0)) / SUM(d.bytes)) * 100, 2) AS pct_used
        FROM dba_users u
        JOIN dba_ts_quotas q ON u.username = q.username
        JOIN dba_tablespaces t ON q.tablespace_name = t.tablespace_name
        JOIN dba_data_files d ON t.tablespace_name = d.tablespace_name
        LEFT JOIN (
            SELECT tablespace_name, SUM(bytes) AS free_bytes
            FROM dba_free_space
            GROUP BY tablespace_name
        ) f ON t.tablespace_name = f.tablespace_name
        GROUP BY u.username, q.tablespace_name, f.free_bytes
        ORDER BY pct_used DESC
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query)

    columns = [col[0].lower() for col in cursor.description]
    results = [dict(zip(columns, row)) for row in cursor]

    cursor.close()
    conn.close()
    return results


if __name__ == "__main__":
    data = get_tablespace_info()
    for row in data:
        print(row)

