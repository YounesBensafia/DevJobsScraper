# app/database.py
import aiosqlite

DB_PATH = "./data/jobs.db"

async def get_jobs():
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT * FROM jobs")
        rows = await cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        await cursor.close()
    return [dict(zip(columns, row)) for row in rows]
