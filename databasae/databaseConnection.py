import mysql.connector

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
