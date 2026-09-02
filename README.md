# NUMS — Backend

Django + Django REST Framework API that serves the exam-centre candidate list
consumed by the `NUMS` React Native app (sibling directory).

Data comes from the exam-centre spreadsheet (`data/islamabad.xlsx`), plus one
added column — `image`, a base64-encoded PNG photo. The photos are **generated
sample data** (initials on a coloured disc) standing in until real photographs
are supplied.

## Setup

```bash
python3 -m venv .venv
./.venv/bin/pip install -r requirements.txt
./.venv/bin/python manage.py migrate
./.venv/bin/python manage.py import_candidates data/islamabad.xlsx
./.venv/bin/python manage.py runserver 0.0.0.0:8000
```

Tests:

```bash
./.venv/bin/python manage.py test
```

Optional admin UI (`/admin`, shows each candidate's photo):

```bash
./.venv/bin/python manage.py createsuperuser
```

## Importing the spreadsheet

```bash
./.venv/bin/python manage.py import_candidates <path.xlsx> [--sheet NAME]
```

Rows are upserted on `roll_number`, so re-running is safe. Headers are matched
case- and punctuation-insensitively (the sheet's `Graudating Country` typo is
mapped explicitly); unmapped columns are reported and skipped. Excel date cells
such as `Test Month` are rendered as `May 2026`.

## API

Base path `/api`. No authentication — this is a development backend.

| Method | Path | Response |
| --- | --- | --- |
| `GET` | `/api/health` | `{"status": "ok", "candidates": 5}` |
| `GET` | `/api/users` | `{"users": [...]}` (no `image`, for debugging) |
| `GET` | `/api/users/{rollNumber}/exists` | `{"exists": true}` |
| `POST` | `/api/users/{rollNumber}/details` | `{"user": {...}}` |

`POST .../details` requires `{"verificationId": "..."}` — the id the native SDK
returns. Each call writes a `VerificationAttempt` audit row. An unknown roll
number returns `404` with `{"code": "USER_NOT_FOUND", ...}`, and a missing
`verificationId` returns `400`.

Example:

```bash
curl -s localhost:8000/api/users/91086798/exists
curl -s -X POST localhost:8000/api/users/91086798/details \
  -H 'Content-Type: application/json' -d '{"verificationId":"ver-1"}'
```

The candidate payload is camel-cased for the client:

```json
{
  "user": {
    "id": "1",
    "rollNumber": "91086798",
    "name": "Waqas Yasin",
    "fatherName": "Muhammad Yasin",
    "authorizationNo": "8141",
    "email": "aaa",
    "testType": "Medical",
    "contactNo": "3425120921",
    "gender": "Male",
    "city": "Kotli",
    "examCity": "ISLAMABAD/RAWALPINDI",
    "graduatingCountry": "CHINA",
    "graduatingCollege": "Xinxiang Medical University",
    "session": "Morning",
    "reportingTime": "0700 AM",
    "testTiming": "0930 AM",
    "examCenter": "King Hamad University of Nursing and Associated Medical Sciences, Park Road, Chak Shehzad, Islamabad",
    "centerLocation": "https://maps.app.goo.gl/...",
    "testMonth": "May 2026",
    "image": "<base64 PNG>"
  }
}
```

## Imported roll numbers

`91086798`, `91086800`, `91086807`, `91086813`, `91086814` — all eight digits,
which is the format the app validates.

## Layout

```
config/            settings, root urls
candidates/
  models.py        Candidate, VerificationAttempt
  serializers.py   camel-cased payloads
  views.py         exists / details / list / health
  urls.py          /api routes
  admin.py         admin with photo preview
  tests.py         endpoint + importer tests
  management/commands/import_candidates.py
data/islamabad.xlsx
```

## Environment variables

| Variable | Default |
| --- | --- |
| `DJANGO_SECRET_KEY` | dev-only placeholder |
| `DJANGO_DEBUG` | `1` |
| `DJANGO_ALLOWED_HOSTS` | `*` |

The SQLite database (`db.sqlite3`) is gitignored; re-create it with `migrate`
plus `import_candidates`.
