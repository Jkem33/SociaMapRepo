# SocioMap Project

## 🧠 Requirements
- Python 3.10+
- Node.js 18+
- PostgreSQL running locally

---

## 🚀 Setup Instructions

### 1. Backend Setup
```bash
cd SocioMapBackend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn main:app --reload