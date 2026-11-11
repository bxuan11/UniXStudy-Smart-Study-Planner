# UniXStudy backend — Step 45.1

Python FastAPI backend for the future Flutter/Dart student application, using
Supabase Authentication and existing PostgreSQL tables through PostgREST.

## Run (PowerShell, from this backend folder)

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

No activation is needed when using the virtual environment's Python directly.
Open http://127.0.0.1:8000/health and http://127.0.0.1:8000/docs.
Expected health response: `{"status":"ok","system":"UniXStudy"}`.
Stop the server with Ctrl+C. Health is liveness, not a database connectivity test.

## Files

- `app/main.py`: app, explicit CORS configuration, health endpoint and Swagger docs.
- `app/config.py`: environment settings; `.env` is resolved relative to backend.
- `app/database.py`: independent Supabase client for each dependency invocation.
- `app/auth.py`: reusable Bearer JWT verification and RLS-aware client dependencies.
- `app/routers`, `schemas`, `models`, `services`: packages for later endpoints.
- `.env.example`: blank configuration template; `.gitignore`: secrets/venv exclusions.
- `requirements.txt`: compatible dependency ranges; `requirements.lock.txt`: tested versions.

## Supabase preparation

Enter your Supabase project URL and publishable/legacy anon key in local `.env`.
Never use service_role/secret keys in this scaffold, Flutter, or Git.
No database connection string or JWT signing secret is required.
`get_verified_token` validates access tokens with Supabase Auth `get_user`.
Future routes can depend on `get_authenticated_supabase`, which passes that user's
JWT to PostgREST. Do not share mutable authenticated clients across users.
Authentication, Courses, Scores and Timetable routes are not implemented in 45.1.
No table queries, migrations, schema changes or RLS changes run at startup.

## Required before domain APIs

Chapter 1–4 were not present at setup time. Supply those documents plus the
existing table/foreign-key and RLS definitions before implementing domain models.
Preserve exact case for Student, StudentCourse, Course, AssessmentScore,
StudyTimetable and their confirmed fields. Do not invent fields or rebuild tables.

Future Flutter clients sign in through Supabase Auth and send their access JWT in
`Authorization: Bearer <access_token>` to protected backend endpoints. Set exact
Flutter web origins in CORS_ORIGINS; Android emulator uses 10.0.2.2 for the host.
Binding to 0.0.0.0 is needed for device access on a trusted local network.

## Verification scope

The local smoke check covers /health, /docs and /openapi.json without credentials.
It does not prove Supabase connectivity, real JWT validation or RLS isolation.
Real RLS tests need signed-in Student A/B JWTs and confirmed target records.
SQL Editor SET ROLE/set_config tests simulate identity and are separate evidence.
Do not commit tokens, passwords, `.env`, or real test-user data.

Official references: https://fastapi.tiangolo.com/tutorial/first-steps/
and https://supabase.com/docs/reference/python/auth-getuser
