# Analysea Backend

# Setup Guide
## 1. Clone the repo
```bash
git clone <repo>
cd analysea/backend
```

## 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

## 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## 4. Configure Environment
Copy `.env.sample` to `.env` and update values:
```bash
DATABASE_URL=postgresql+psycopg2://user:password@host:5432/dbname
GEMINI_API_KEY=example_key
FRONTEND_URL=url
```

## 5. Running the App
```bash
uvicorn main:app --reload
```