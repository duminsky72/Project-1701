import os
import pymysql


def get_db_connection():
    return pymysql.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
        cursorclass=pymysql.cursors.DictCursor
    )


def get_contacts(severity: str, service: str):
    """
    Fetch contacts matching severity and service
    """

    query = """
        SELECT c.name, c.phone, c.whatsapp, p.channels
        FROM contacts c
        JOIN notification_preferences p ON c.id = p.contact_id
        WHERE p.severity_min <= %s
          AND c.active = 1
    """

    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute(query, (severity,))
        results = cursor.fetchall()

    conn.close()

    for r in results:
        r["channels"] = r["channels"].split(",")

    return results
