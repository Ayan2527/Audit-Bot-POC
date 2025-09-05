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
            ts.tablespace_name,
            ts.contents,
            ts.status,
            ROUND(SUM(df.bytes)/1024/1024, 2) AS allocated_mb,
            ROUND((SUM(df.bytes) - NVL(fs.free_bytes, 0))/1024/1024, 2) AS used_mb,
            ROUND(((SUM(df.bytes) - NVL(fs.free_bytes, 0)) / SUM(df.bytes)) * 100, 2) AS pct_used
        FROM dba_users u
        LEFT JOIN dba_ts_quotas q 
            ON u.username = q.username
        JOIN dba_tablespaces ts 
            ON q.tablespace_name = ts.tablespace_name
        JOIN dba_data_files df 
            ON ts.tablespace_name = df.tablespace_name
        LEFT JOIN (
            SELECT tablespace_name, SUM(bytes) AS free_bytes
            FROM dba_free_space
            GROUP BY tablespace_name
        ) fs 
            ON ts.tablespace_name = fs.tablespace_name
        GROUP BY u.username, ts.tablespace_name, ts.contents, ts.status, fs.free_bytes
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
