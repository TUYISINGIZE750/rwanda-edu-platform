# ✓ VERIFIED WORKING CREDENTIALS

All users confirmed to exist in database (app.db) with correct passwords.

## Teacher Account
- **Email**: `Elam@gmail.com`
- **Password**: `password123`
- **Name**: HAKIZIMANA Elam
- **ID**: 94
- **School**: 63
- **Role**: TEACHER

## Student Accounts (All in School 63)

### Student 1
- **Email**: `teststudent1@school.rw`
- **Password**: `password123`
- **Name**: Test Student 1
- **ID**: 98

### Student 2
- **Email**: `teststudent2@school.rw`
- **Password**: `password123`
- **Name**: Test Student 2
- **ID**: 99

### Student 3
- **Email**: `teststudent3@school.rw`
- **Password**: `password123`
- **Name**: Test Student 3
- **ID**: 100

## Test Group
- **Group ID**: 26
- **Name**: L3 LSV - Teacher Test Group
- **School**: 63
- **All members enrolled via group_members table**

## Access URLs
- **Frontend**: http://localhost:5173
- **Backend**: http://localhost:8080
- **Chat**: http://localhost:5173/hubs/26

## Important Notes
1. Backend MUST be running on port 8080
2. Frontend MUST be running on port 5173
3. All users are in the same school (63) for proper access control
4. Passwords are case-sensitive: `password123` (all lowercase)
5. Email addresses are case-sensitive as stored

## If Login Still Fails

### Check Backend is Running
```bash
cd backend
uvicorn app.main:app --reload --port 8080
```

### Check Frontend is Running
```bash
cd frontend
npm run dev
```

### Verify Database
The users are confirmed in `backend/app.db` - run `backend/check_users.py` to verify again.
