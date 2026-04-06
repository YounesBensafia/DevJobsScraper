import os
import sqlite3
import pytest
from src.core.database import get_db_connection, init_db
from src.core.config import DB_PATH

def test_init_db(mocker):
    # Mock DB_PATH to a temporary test database
    temp_db = "temp_test_jobs.db"
    mocker.patch("src.core.database.DB_PATH", temp_db)
    
    if os.path.exists(temp_db):
        os.remove(temp_db)
    
    try:
        init_db()
        assert os.path.exists(temp_db)
        
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='jobs'")
        assert cursor.fetchone() is not None
        conn.close()
    finally:
        if os.path.exists(temp_db):
            os.remove(temp_db)

def test_get_db_connection(mocker):
    temp_db = "temp_test_conn.db"
    mocker.patch("src.core.database.DB_PATH", temp_db)
    
    try:
        conn = get_db_connection()
        assert isinstance(conn, sqlite3.Connection)
        conn.close()
    finally:
        if os.path.exists(temp_db):
            os.remove(temp_db)
