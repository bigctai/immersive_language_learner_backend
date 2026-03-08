## Interactive Language Learner Backend

Backend API for an immersive language learner app.

- **Framework**: FastAPI
- **Server**: Uvicorn
- **Database**: SQLite (via SQLAlchemy ORM)
- **Translation**: Google Cloud Translate v2
- **Pronunciation**: Pinyin via `pypinyin`

## Requirements

- **Python**: 3.11+ recommended
- **Google Cloud credentials**: service account JSON for Translate API

## Setup

Create and activate a virtual environment, then install dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

If you use environment variables, create a `.env` (optional — current code uses `dotenv`):

```bash
cp .env.example .env 2>/dev/null || true
```

## Run the API

### Development (recommended)

```bash
uvicorn main:app --reload --port 8080
```

### Production-like

```bash
uvicorn main:app --host 0.0.0.0 --port 8080
```

The API will be at `http://localhost:8080`.

FastAPI docs:

- **Swagger UI**: `http://localhost:8080/docs`
- **OpenAPI JSON**: `http://localhost:8080/openapi.json`

## Database

This project uses a local SQLite DB file created automatically on startup:

- `immersive_language_learner_backend.db`

Tables are created at app startup via `create_all_tables()` in `main.py`, which calls SQLAlchemy `Base.metadata.create_all(...)`.

### Important: schema changes (e.g. adding `pronunciation`)

`create_all()` **does not** modify existing tables. If you add a new column in a model (like `pronunciation`), you must update the database schema yourself, otherwise you’ll see 500s when selecting/inserting.

To add a column in SQLite:

```bash
sqlite3 immersive_language_learner_backend.db "ALTER TABLE vocab_bank ADD COLUMN pronunciation TEXT;"
```

Or, if you don’t care about existing data, delete the DB file and restart the server to recreate tables.

## API Endpoints

### User

- **Create user**
  - `POST /user/create?username=<username>`

- **Get user id by username**
  - `GET /user/get/<username>`

- **Get user data (with vocab list)**
  - `GET /user/get_user_data/<id>`

- **Add vocab**
  - `POST /user/add_vocab`
  - JSON body:

```json
{
  "user_id": 1,
  "phrase": "hello",
  "translation": "你好",
  "pronunciation": "ni hao",
  "priority": 1,
  "difficulty": 1
}
```

### Translate

- **Translate an English phrase to zh-TW + pinyin**
  - `GET /translate/phrase?phrase=hello`
  - Response shape:

```json
{
  "original": "hello",
  "chinese": "你好",
  "pinyin": "ni hao"
}
```

## Google Cloud credentials (Translate API)

`routes/translate.py` currently loads credentials from a **hard-coded absolute path** to a service account JSON file.

If you move machines or share this repo, you’ll want to change this to use an env var (recommended), e.g. `GOOGLE_APPLICATION_CREDENTIALS`, and keep the JSON out of git.

## CORS / Frontend

CORS is configured to allow:

- `http://localhost:5173`

If your frontend runs elsewhere, update `allow_origins` in `main.py`.

## Handy SQLite commands

Open the DB:

```bash
sqlite3 immersive_language_learner_backend.db
```

List tables:

```sql
.tables
```

Show schema:

```sql
.schema user
.schema vocab_bank
```

Add a user manually:

```sql
INSERT INTO user (username) VALUES ('your_username');
```