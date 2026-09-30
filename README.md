# LegalEase - AI-Powered Legal Document Generator

LegalEase uses a Streamlit frontend, FastAPI backend, and Google Gemini for AI-assisted legal document drafting.

## Project structure

```text
LegalEase_Project/
├── main.py
├── routes.py
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── ai_core/
│   ├── __init__.py
│   └── gemini_generator.py
└── utils/
    ├── __init__.py
    └── formatters.py
```

## PowerShell setup

```powershell
cd "C:\path\to\LegalEase_Project"

py -3.10 -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt

Copy-Item .env.example .env
notepad .env
```

Put your Gemini API key in `.env`.

## Run backend

Open PowerShell window 1:

```powershell
cd "C:\path\to\LegalEase_Project"
.\.venv\Scripts\Activate.ps1
uvicorn main:app --reload
```

Backend:
http://127.0.0.1:8000

Swagger:
http://127.0.0.1:8000/docs

## Run frontend

Open PowerShell window 2:

```powershell
cd "C:\path\to\LegalEase_Project"
.\.venv\Scripts\Activate.ps1
streamlit run app.py
```

The Streamlit URL is normally:
http://localhost:8501

## Test without Gemini

If GEMINI_API_KEY is empty, the project returns a local sample document so you can test the UI and download functions.

## Important

AI-generated legal documents are drafts and should be reviewed by a qualified legal professional before use.
