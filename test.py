import sqlite3


def view_jobs():
    conn = sqlite3.connect("src/data/jobs.db")
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM jobs")
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]

        print(f"\n📄 Total jobs: {len(rows)}\n")

        for i, row in enumerate(rows, 1):
            job = dict(zip(columns, row))
            print(f"\nJob:",job['id'])
            print(f"at {job['company']}")
            print(f"   Posted: {job['time']}")
            print(f"   Tags: {job['tags']}")
            print(f"   Location: {job['locations']}")
            print(f"   Salary: {job['salary']}")
            print(f"   Link: {job['link']}")
            print(f"   Logo: {job['logo']}")
            print("-" * 50)

    except sqlite3.OperationalError as e:
        print("Error:", e)
    finally:
        conn.close()


if __name__ == "__main__":
    view_jobs()
