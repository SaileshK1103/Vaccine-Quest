import mysql.connector

def create_connection():
    connection = mysql.connector.connect(
        user = 'sailesh',
        password = 'sailesh1103',
        host = 'localhost',
        port = '3306',
        database = 'flight_game',
        autocommit = True,
        charset = 'utf8mb4',
        collation = 'utf8mb4_unicode_ci'
    )
    return connection

def fetch_data(query):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results