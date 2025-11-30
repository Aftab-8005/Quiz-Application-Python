import mysql.connector

def connect():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Aftab@123",
        database="quizapp"
    )

def execute(query, params=None):
    conn = connect()
    cur = conn.cursor()
    cur.execute(query, params)
    conn.commit()
    conn.close()

def fetchone(query, params=None):
    conn = connect()
    cur = conn.cursor()
    cur.execute(query, params)
    data = cur.fetchone()
    conn.close()
    return data

def fetchall(query, params=None):
    conn = connect()
    cur = conn.cursor()
    cur.execute(query, params)
    data = cur.fetchall()
    conn.close()
    return data
