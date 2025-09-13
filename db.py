import psycopg2
import streamlit as st
import sqlite3

USE_SQLITE = False

def get_conn():
    global USE_SQLITE
    try:
        # Try PostgreSQL first
        conn = psycopg2.connect(
            dbname=st.secrets["postgres"]["dbname"],
            user=st.secrets["postgres"]["user"],
            password=st.secrets["postgres"]["password"],
            host=st.secrets["postgres"]["host"],
            port=st.secrets["postgres"]["port"]
        )
        USE_SQLITE = False
        return conn
    except Exception:
        # Fallback: SQLite
        conn = sqlite3.connect("local.db", check_same_thread=False)
        USE_SQLITE = True
        return conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()

    if USE_SQLITE:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                face_embedding BLOB
            );
        """)
    else:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                face_embedding BYTEA
            );
        """)

    conn.commit()
    cur.close()
    conn.close()
