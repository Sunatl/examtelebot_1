import psycopg2
from secret import * 

def connection_database():
    conn = psycopg2.connect(
        database="exam_telebot_1",
        host="localhost",
        user="postgres",
        password=databasess,
        port=5432
    )
    return conn

def close_con(conn, cur):
    cur.close()
    conn.close()

def setup_database():
    conn = connection_database()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        user_id SERIAL PRIMARY KEY,
        username VARCHAR(100) UNIQUE,
        chat_id BIGINT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS trips (
        trip_id SERIAL PRIMARY KEY,
        user_id serial primary key,
        start_location VARCHAR(255),
        end_location VARCHAR(255),
        trip_date TIMESTAMP,
        seats_available INT,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS companion_requests (
        request_id SERIAL PRIMARY KEY,
        user_id serial primary key,
        start_location VARCHAR(255),
        end_location VARCHAR(255),
        trip_date TIMESTAMP,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    close_con(conn, cur)

def add_user(username, chat_id):
    conn = connection_database()
    cur = conn.cursor()
    cur.execute(f"""
    INSERT INTO Users (username, chat_id) 
    VALUES ('{username}', '{chat_id}') 
    ON CONFLICT (username) DO NOTHING
    """)
    conn.commit()
    close_con(conn, cur)

def get_user(username):
    conn = connection_database()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM Users WHERE username = '{username}'")
    user = cur.fetchone()
    close_con(conn, cur)
    return user

def get_trips():
    conn = connection_database()
    cur = conn.cursor()
    cur.execute("SELECT * FROM trips")
    trips = cur.fetchall()
    close_con(conn, cur)
    return trips



# def add_companion_request(user_id, start_location, end_location, trip_date, description):
#     conn = connection_database()
#     cur = conn.cursor()
#     cur.execute(f"""
#     INSERT INTO companion_requests(user_id, start_location, end_location, trip_date, description) 
#     VALUES ({user_id}, '{start_location}', '{end_location}', '{trip_date}', '{description}')
#     """)
#     conn.commit()
#     close_con(conn, cur)

def get_companion_requests():
    conn = connection_database()
    cur = conn.cursor()
    cur.execute("SELECT * FROM companion_requests")
    requests = cur.fetchall()
    close_con(conn, cur)
    return requests


def delete_trip(trip_id):
    conn = connection_database()
    cur = conn.cursor()
    cur.execute(f"DELETE FROM trips WHERE trip_id = {trip_id}")
    conn.commit()
    close_con(conn, cur)

def delete_companion_request(request_id):
    conn = connection_database()
    cur = conn.cursor()
    cur.execute(f"DELETE FROM companion_requests WHERE request_id = {request_id}")
    conn.commit()
    close_con(conn, cur)


def update_trip(trip_id, start_location, end_location, trip_date, seats_available, description):
    conn = connection_database()
    cur = conn.cursor()
    cur.execute("""
    UPDATE trips 
    SET start_location = %s, end_location = %s, trip_date = %s, seats_available = %s, description = %s 
    WHERE trip_id = %s
    """, (start_location, end_location, trip_date, seats_available, description, trip_id))
    conn.commit()
    close_con(conn, cur)

def add_companion_request(user_id, start_location, end_location, trip_date, description):
    conn = connection_database()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO companion_requests (user_id, start_location, end_location, trip_date, description) 
    VALUES (%s, %s, %s, %s, %s)
    """, (user_id, start_location, end_location, trip_date, description))
    conn.commit()
    close_con(conn, cur)

def delete_companion_request(request_id):
    conn = connection_database()
    cur = conn.cursor()
    cur.execute("DELETE FROM companion_requests WHERE request_id = %s", (request_id,))
    conn.commit()
    close_con(conn, cur)

def view_companion_requests():
    conn = connection_database()
    cur = conn.cursor()
    cur.execute("SELECT * FROM companion_requests")
    rows = cur.fetchall()
    close_con(conn, cur)
    return rows

def update_companion_request(request_id, start_location, end_location, trip_date, description):
    conn = connection_database()
    cur = conn.cursor()
    cur.execute("""
    UPDATE companion_requests 
    SET start_location = %s, end_location = %s, trip_date = %s, description = %s 
    WHERE request_id = %s
    """, (start_location, end_location, trip_date, description, request_id))
    conn.commit()
    close_con(conn, cur)


