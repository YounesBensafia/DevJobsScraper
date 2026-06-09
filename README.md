# DevJobsScraper

Scrapes developer job listings from [Emploitic](https://emploitic.com) and exposes them via a paginated, filterable REST API.

---

## Quickstart

```bash
uv run python main.py api
```

Server starts at `http://localhost:8000`. On first launch, it downloads ChromeDriver, scrapes all sources, stores results in SQLite, and repeats every 30 minutes. The API is available immediately while scraping runs in the background.

---

## Usage

### API mode (default)

```bash
python main.py api
```

Starts a **FastAPI** server with Uvicorn (hot-reload enabled). A background asyncio task runs an infinite loop:

1. Instantiate each scraper from the `SCRAPERS` registry
2. Call `scraper.run()` — scrapes the site and saves jobs to SQLite
3. Run `main_cleaner()` — normalizes tags and removes old listings
4. Sleep 1800 seconds (30 minutes), then repeat

The background loop is managed via FastAPI's lifespan context, so it starts with the server and is cancelled cleanly on shutdown.

### Scraper mode (one-shot)

```bash
python main.py scraper
```

Runs every scraper exactly once, cleans the data, and exits. Useful for debugging or cron-based scheduling.

---

## API Reference

### `GET /jobs`

Returns paginated, filterable job listings from the SQLite database.

#### Query Parameters

| Param | Type | Default | Constraints | Description |
|---|---|---|---|---|
| `page` | int | `1` | `>= 1` | Page number |
| `limit` | int | `20` | `1-100` | Items per page |
| `tag` | str | — | — | Partial match on tags column (e.g. `python` matches `"Python, Remote"`) |
| `location` | str | — | — | Partial match on locations column (e.g. `Alger` matches `"Cheraga, Alger, Algerie"`) |
| `salary_min` | int | — | `>= 0` | Minimum salary — checks `COALESCE(salary_to, salary_from, 0) >= value` |
| `salary_max` | int | — | `>= 0` | Maximum salary — checks `COALESCE(salary_from, salary_to, 0) <= value` |

All filters are combined with AND. Omitting a filter skips it entirely.

#### Example

```bash
curl "http://localhost:8000/jobs?tag=python&salary_min=50000&limit=5"
```

#### Response

```json
{
  "data": [
    {
      "title": "Python Developer",
      "company": "Ampcontrol",
      "time": "2d",
      "tags": "Python, English, Remote",
      "locations": "Europe, Latin America",
      "link": "https://remoteok.com/remote-jobs/remote-python-developer-ampcontrol-1096950",
      "logo": "https://resizeapi.com/...png",
      "salary_from": 60000,
      "salary_to": 120000,
      "currency": "$"
    }
  ],
  "total": 1,
  "page": 1,
  "pages": 1
}
```

The `pages` field is `0` when there are no results.

---

## Architecture

```
                         main.py
                        /       \
                   api mode    scraper mode
                       |            |
                  src.api/      src.scrapers/
                  main.py       /         \
                  (FastAPI)    base.py    emploitic.py
                       |            |
                  src.core/     src.utils/
                  config.py     cleaner.py
                  database.py
                  models.py
                       |
                  src.data/
                  jobs.db
```

### Layer breakdown

#### `main.py` — Entry point

CLI dispatcher. Parses `api` or `scraper` argument and delegates. In API mode, it boots Uvicorn pointing at `src.api.main:app` with hot-reload on port 8000.

#### `src/core/config.py` — Configuration

Loads `.env` via `python-dotenv` from the project root. All variables have sensible defaults so the app runs with zero configuration:

| Variable | Default | Description |
|---|---|---|
| `DB_PATH` | `src/data/jobs.db` | Path to the SQLite database file (relative to project root) |
| `EMPLOITIC_URL` | `https://emploitic.com/offres-d-emploi` | Base URL for the Emploitic scraper |
| `ALLOWED_ORIGINS` | `*` | Comma-separated CORS allowed origins |

#### `src/core/database.py` — Database layer

Provides two functions:

- **`get_db_connection()`** — Opens a `sqlite3.Connection` to `DB_PATH` with:
  - `row_factory = sqlite3.Row` for dict-like row access
  - `timeout=30` — waits up to 30s if the DB is locked
  - `check_same_thread=False` — allows the connection to be shared between the API thread and the background scraper task
- **`init_db()`** — Creates the `jobs` table if it doesn't exist:

```sql
CREATE TABLE IF NOT EXISTS jobs (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    title           TEXT NOT NULL,
    company         TEXT NOT NULL,
    time            TEXT,
    tags            TEXT,
    locations       TEXT,
    link            TEXT UNIQUE,
    logo            TEXT,
    salary_from     INTEGER,
    salary_to       INTEGER,
    currency        TEXT
);
```

The `link` column has a `UNIQUE` constraint, which is used by `INSERT OR IGNORE` for deduplication.

#### `src/core/models.py` — Job model

A `@dataclass` with 10 fields (3 required: `title`, `company`, `link`; 7 optional). Two methods:

- **`to_dict()`** — delegates to `dataclasses.asdict()` for JSON serialization
- **`save_to_db(conn)`** — executes an `INSERT OR IGNORE` with parameterized SQL. The caller is responsible for committing/rolling back the transaction

#### `src/scrapers/base.py` — Abstract scraper

`BaseScraper(ABC)` defines the contract:

- **`scrape() -> List[Job]`** — abstract, implemented by concrete scrapers
- **`run() -> int`** — template method that:
  1. Calls `self.scrape()`
  2. Returns `0` immediately if no jobs found
  3. Opens a DB connection
  4. Saves each job in a loop
  5. **Commits once** at the end (atomic batch)
  6. On failure, **rolls back** and re-raises (prevents partial writes)
  7. Closes the connection in a `finally` block
  8. Returns the count of saved jobs

Uses `logging.getLogger(__name__)` instead of `print()`.

#### `src/scrapers/emploitic.py` — Emploitic scraper

Targets `https://emploitic.com/offres-d-emploi?search=developer`.

- Uses **Selenium WebDriver** with headless Chrome
- `WebDriverWait(driver, 15)` until `[data-testid="jobs-item"]` elements appear
- Extracts per job: `title` (h2), `company` (p), `link` (a href), `location` (via RoomRoundedIcon XPath), `posted_time` (via TimelapseRoundedIcon XPath)
- Sets `tags="emploitic"` constant for all scraped jobs
- ChromeDriver path is cached in `__init__` (downloaded once)
- Driver is always cleaned up via `try/finally` on `driver.quit()`

#### `src/utils/cleaner.py` — Data cleaning

Three functions:

- **`normalize_tags(tags)`** — splits comma-separated string, strips whitespace, re-joins. Returns `"not mentioned"` for empty input
- **`extract_salary_parts(raw_salary)`** — parses strings like `"$100k - $150k"` or `"€80,000"` into `(salary_from, salary_to, currency)`. Detects `$`, `€`, `£`; normalizes `k` → `000`; removes commas. Returns `(None, None, None)` for `"negotiable"`
- **`clean_jobs()`** — queries all jobs, normalizes their tags, deletes entries older than 1 year via `WHERE time LIKE '%1yr%'`

#### `src/api/main.py` — FastAPI server

- CORS middleware configured with `ALLOWED_ORIGINS`
- Lifespan handler initializes the database and spawns the background scraper loop
- Single endpoint `GET /jobs` with dynamic SQL query building based on provided filter parameters

---

## Scraper lifecycle (detailed)

```
run()                     BaseScraper
  │
  ├─ scrape()             implemented by EmploiticScraper
  │    │
  │    ├─ _get_driver()   headless Chrome via Selenium
  │    ├─ driver.get()    navigate to URL
  │    ├─ WebDriverWait   wait for job elements
  │    ├─ find_elements   locate all job cards
  │    ├─ loop            extract fields per card
  │    │    └─ Job(...)   build dataclass instance
  │    ├─ return jobs     return list
  │    └─ finally         driver.quit()
  │
  ├─ return 0             if no jobs
  │
  ├─ get_db_connection()  open SQLite
  ├─ job.save_to_db()     INSERT OR IGNORE each job
  ├─ conn.commit()        atomic commit
  ├─ return len(jobs)
  │
  └─ except               conn.rollback() + raise
     └─ finally           conn.close()
```

Each scraper is wrapped in an individual `try/except` in the background loop, so one failing scraper doesn't kill the entire cycle.

---

## Testing

```bash
pytest -v
```

10 tests covering:

| Test file | What it covers |
|---|---|
| `tests/test_api.py` | `GET /jobs` endpoint via `TestClient`, mocks DB connection |
| `tests/test_cleaner.py` | `normalize_tags()` and `extract_salary_parts()` edge cases |
| `tests/test_database.py` | `init_db()` table creation and `get_db_connection()` |
| `tests/test_models.py` | Job dataclass init, `to_dict()`, and `save_to_db()` with in-memory SQLite |

---

## Tech stack

| Layer | Technology |
|---|---|
| Language | Python 3.13 |
| API framework | FastAPI + Uvicorn |
| Scraping | Selenium + ChromeDriver |
| Database | SQLite (via `sqlite3` stdlib) |
| Data processing | pandas (CSV export, available but not actively used) |
| Testing | pytest + pytest-mock |
| Linting / formatting | ruff (line-length 88, `E`, `F`, `I`, `N`, `W` rules) |
| Package management | uv |
| Environment | python-dotenv |

---

## Project structure

```
DevJobsScraper/
├── main.py                        CLI entry point
├── pyproject.toml                 Project metadata & dependencies
├── pytest.ini                     Pytest configuration
├── uv.lock                        Locked dependency versions
├── .python-version                Python version pin
├── .gitignore
│
├── src/
│   ├── __init__.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── main.py                FastAPI app, endpoints, background loop
│   │
│   ├── core/
│   │   ├── __init__.py            Re-exports for clean imports
│   │   ├── config.py              Env vars & paths
│   │   ├── database.py            SQLite connection & schema init
│   │   └── models.py              Job dataclass
│   │
│   ├── scrapers/
│   │   ├── __init__.py            SCRAPERS registry
│   │   ├── base.py                Abstract scraper with transaction logic
│   │   └── emploitic.py           Emploitic job board scraper
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   └── cleaner.py             Tag cleaning, salary parsing, old job removal
│   │
│   └── data/
│       └── jobs.db                SQLite database (auto-created)
│
└── tests/
    ├── test_api.py
    ├── test_cleaner.py
    ├── test_database.py
    └── test_models.py
```
