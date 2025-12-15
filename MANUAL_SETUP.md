# Manual Setup Guide

## Step-by-Step Setup

### 1. Install Dependencies (if not done)
```bash
cd backend
pip install -r requirements.txt

cd ../frontend
npm install
```

### 2. Create Database Tables
```bash
cd backend
python -c "from app.core.database import Base, engine; Base.metadata.create_all(bind=engine); print('Tables created')"
```

### 3. Seed Schools
```bash
python seed_official_schools.py
```

### 4. Verify
```bash
python -c "from app.core.database import SessionLocal; from app.models.school import School; db = SessionLocal(); print(f'Total schools: {db.query(School).count()}'); db.close()"
```

Expected output: `Total schools: 70`

### 5. Start Backend
```bash
uvicorn app.main:app --reload
```

### 6. Start Frontend (new terminal)
```bash
cd frontend
npm run dev
```

### 7. Test
Visit: `http://localhost:5173/register`

## Quick Commands

```bash
# All in one (from project root)
cd backend && python -c "from app.core.database import Base, engine; Base.metadata.create_all(bind=engine)" && python seed_official_schools.py && uvicorn app.main:app --reload
```

## Troubleshooting

### Module not found errors?
```bash
cd backend
pip install fastapi sqlalchemy pydantic uvicorn python-jose passlib bcrypt
```

### Database errors?
Delete the database file and recreate:
```bash
cd backend
del app.db  # or rm app.db on Unix
python -c "from app.core.database import Base, engine; Base.metadata.create_all(bind=engine)"
python seed_official_schools.py
```

### Frontend errors?
```bash
cd frontend
npm install
npm run dev
```
