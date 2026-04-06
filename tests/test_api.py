from fastapi.testclient import TestClient
from src.api.main import app
import sqlite3
import pytest

client = TestClient(app)

def test_read_main(mocker):
    mock_conn = sqlite3.connect(":memory:", check_same_thread=False)
    mock_conn.row_factory = sqlite3.Row
    cursor = mock_conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY, 
            title TEXT, 
            company TEXT, 
            time TEXT,
            tags TEXT,
            locations TEXT,
            link TEXT,
            logo TEXT,
            salary_from INTEGER,
            salary_to INTEGER,
            currency TEXT
        )
    ''')
    cursor.execute("""
        INSERT INTO jobs (id, title, company, link, tags) 
        VALUES (1, 'Tester', 'QA Inc', 'http://qa.com', 'testing')
    """)
    mock_conn.commit()
    
    mocker.patch("src.api.main.get_db_connection", return_value=mock_conn)
    
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Tester"
    assert data[0]["company"] == "QA Inc"
