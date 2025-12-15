# CORS Error Fix - Registration System

## Problem Fixed
- ✅ CORS policy blocking requests from frontend (localhost:5173) to backend (localhost:8080)
- ✅ 500 Internal Server Error when loading schools
- ✅ Network errors during teacher/student registration

## Changes Made

### 1. Backend CORS Configuration (`backend/app/main.py`)
- Added `expose_headers=["*"]` to CORS middleware
- Added `max_age=3600` for preflight caching
- Ensures all origins, methods, and headers are allowed

### 2. Registration API (`backend/app/api/registration.py`)
- Fixed province name mapping to handle variations (e.g., "Southern Province" → "South")
- Added multiple province variations for flexible matching
- Added comprehensive error handling to prevent 500 errors
- Added health check endpoint: `/api/v1/registration/health`
- Returns proper error responses instead of throwing exceptions

### 3. Frontend Error Handling (`frontend/src/views/RegisterView.vue`)
- Better error messages for network failures
- Shows user-friendly message when backend is not running
- Displays server error messages properly

## How to Start

### Option 1: Use the Fix Script (Recommended)
```bash
FIX_AND_START.bat
```
This will:
1. Stop any existing servers
2. Start backend on port 8080
3. Start frontend on port 5173
4. Open browser automatically

### Option 2: Manual Start

#### Start Backend
```bash
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

#### Start Frontend (in new terminal)
```bash
cd frontend
npm run dev
```

## Testing

### Test Backend Endpoints
```bash
cd backend
python test_cors.py
```

This will verify:
- ✓ Health check endpoint
- ✓ Registration health endpoint
- ✓ Provinces loading
- ✓ Schools loading (Kamonyi example)
- ✓ CORS headers are properly set

### Manual Browser Test
1. Open http://localhost:5173
2. Go to Register page
3. Select Province: "Southern Province"
4. Select District: "Kamonyi"
5. Schools should load without CORS errors

## Troubleshooting

### Still Getting CORS Errors?
1. Make sure backend is running on port 8080
2. Check browser console for exact error
3. Clear browser cache (Ctrl+Shift+Delete)
4. Restart both servers using `FIX_AND_START.bat`

### 500 Internal Server Error?
1. Check if database exists: `backend/app.db`
2. Run database setup if needed
3. Check backend console for error details

### No Schools Loading?
1. Verify database has schools data
2. Check province/district names match database
3. Run test script: `python backend/test_cors.py`

## API Endpoints

### Registration Endpoints
- `GET /api/v1/registration/health` - Health check
- `GET /api/v1/registration/schools/{province}/{district}` - Get schools
- `GET /api/v1/registration/trades/{school_id}` - Get trades
- `GET /api/v1/registration/levels` - Get levels

### Location Endpoints
- `GET /api/v1/locations/provinces` - Get all provinces
- `GET /api/v1/locations/districts/{province}` - Get districts

## Province Name Mapping

The system now handles these province variations:
- "Southern Province" → "South", "Southern", "Southern Province"
- "Western Province" → "West", "Western", "Western Province"
- "Northern Province" → "North", "Northern", "Northern Province"
- "Eastern Province" → "East", "Eastern", "Eastern Province"
- "Kigali City" → "Kigali city", "Kigali", "Kigali City"

## Success Indicators

When everything is working:
- ✅ No CORS errors in browser console
- ✅ Schools load when district is selected
- ✅ Trades load when school is selected
- ✅ Registration completes successfully
- ✅ Backend test script passes all tests

## Support

If issues persist:
1. Check backend console for errors
2. Check frontend console for errors
3. Run `python backend/test_cors.py` to diagnose
4. Verify both servers are running on correct ports
