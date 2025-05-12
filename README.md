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

For files SOCIALMAPSIMPLE and SMalchemyBase, make sure to have python3 installed, as well as SQLAlchemy.
you can then run the SocialMap code and interact with it in the terminal. THe SocialMap.db should be created when you interact with the terminal. 
