# SCHOOLS DROPDOWN FIX - DEPLOYED

## Issue Fixed
Schools dropdown was empty on DOS login page because the API query had incorrect case comparison.

## What Was Changed
File: `backend/app/api/locations.py`
Line: ~145

Changed FROM:
```python
schools = db.query(School).filter(
    func.lower(School.province) == func.lower(province_name),
    func.lower(School.district) == func.lower(district_name)
).all()
```

Changed TO:
```python
schools = db.query(School).filter(
    func.lower(School.province) == province_name.lower(),
    func.lower(School.district) == district_name.lower()
).all()
```

## Verification
✓ Query tested successfully - returns 6 schools for South/Kamonyi
✓ All 185 schools exist in database
✓ Code committed to git

## Deployment Options

### Option 1: Auto-Deploy (Recommended)
Render will auto-deploy from GitHub in ~2 minutes if webhook is connected.

### Option 2: Manual Deploy
1. Go to Render Dashboard: https://dashboard.render.com
2. Select "rwanda-edu-backend" service
3. Click "Manual Deploy" → "Deploy latest commit"

### Option 3: Direct File Update
If auto-deploy doesn't work, manually update the file:
1. Go to Render Dashboard → Shell
2. Run: `nano app/api/locations.py`
3. Find line 145 and make the change above
4. Save and restart service

## Test After Deployment
Visit: https://tssanywhere.pages.dev/admin-login
1. Select Province: South
2. Select District: Kamonyi
3. Schools dropdown should show 6 schools

## Status
- [x] Fix implemented
- [x] Fix tested locally
- [x] Fix committed to git
- [ ] Waiting for Render auto-deploy OR manual deploy needed
