# Court Case Tracker

Backend service built with **FastAPI** to fetch court case details from the **Jagriti portal**.

## Features
- Fetch states and commissions
- Search cases by complainant, respondent, case number, advocates, judge, industry
- Handles Jagriti API limitations (403) with a local JSON fallback
- Base64 daily orders decoding to PDF

## Run locally
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
Access docs at: http://127.0.0.1:8000/docs

