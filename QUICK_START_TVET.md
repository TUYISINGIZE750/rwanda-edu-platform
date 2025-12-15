# 🚀 Quick Start - TVET Integration

## ⚡ 5-Minute Setup

### Step 1: Run Setup Script
```bash
setup-tvet.bat
```
**This will:**
- ✅ Run database migrations
- ✅ Seed 40 TVET/TSS schools
- ✅ Verify installation

### Step 2: Start Services
```bash
# Terminal 1 - Backend
cd backend
uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### Step 3: Test Registration
1. Open browser: `http://localhost:5173/register`
2. Fill in your details
3. Select location (Province → District → Sector)
4. Choose your TVET/TSS school
5. Complete registration
6. Login and explore!

---

## 📋 Pre-Setup Checklist

Before running setup, ensure you have:
- [ ] Python 3.8+ installed
- [ ] Node.js 16+ installed
- [ ] PostgreSQL/SQLite configured
- [ ] Backend dependencies installed (`pip install -r requirements.txt`)
- [ ] Frontend dependencies installed (`npm install`)

---

## 🎯 What You Get

### 40 Real Schools
- 5 IPRC (Major polytechnics)
- 15 TSS (Technical secondary)
- 20 TVET Centers (Vocational training)

### Complete Location System
- 5 Provinces
- 30 Districts
- 416 Sectors
- Schools mapped to sectors

### Multilingual Support
- 🇷🇼 Kinyarwanda
- 🇬🇧 English
- 🇫🇷 French

---

## 🔍 Quick Test

### Test API Endpoints
```bash
# Get all provinces
curl http://localhost:8000/api/v1/api/locations/provinces

# Get schools in Kigali
curl http://localhost:8000/api/v1/api/locations/schools/district/Umujyi%20wa%20Kigali/Gasabo

# Get all schools
curl http://localhost:8000/api/v1/api/locations/schools
```

### Test Frontend
1. Visit `/register`
2. Select "Umujyi wa Kigali" (Kigali City)
3. Select "Gasabo" district
4. Select "Kimironko" sector
5. Should see "IPRC Kigali" in schools dropdown

---

## 📊 Verify Installation

### Check Database
```bash
cd backend
python -c "from app.core.database import SessionLocal; from app.models.school import School; db = SessionLocal(); print(f'Schools: {db.query(School).count()}'); db.close()"
```
**Expected output:** `Schools: 40`

### Check Schools by Province
```bash
python -c "from app.core.database import SessionLocal; from app.models.school import School; db = SessionLocal(); provinces = db.query(School.province).distinct().all(); [print(f'{p[0]}: {db.query(School).filter(School.province==p[0]).count()} schools') for p in provinces]; db.close()"
```

---

## 🎓 Sample Schools by Location

### Kigali City
- **IPRC Kigali** (Kimironko, Gasabo)
- **Tumba College of Technology** (Ndera, Gasabo)
- **Don Bosco TVET** (Niboye, Kicukiro)

### Southern Province
- **IPRC Huye** (Ngoma, Huye)
- **TSS Byimana** (Byimana, Ruhango)
- **CFP Nyanza** (Busasamana, Nyanza)

### Eastern Province
- **IPRC Ngoma** (Kibungo, Ngoma)
- **TSS Murunda** (Muhazi, Rwamagana)
- **Don Bosco VTC Muhazi** (Muhazi, Rwamagana)

### Western Province
- **IPRC Karongi** (Bwishyura, Karongi)
- **TSS Rubengera** (Rubengera, Karongi)
- **Ecole Technique Rubavu** (Gisenyi, Rubavu)

### Northern Province
- **IPRC Musanze** (Muhoza, Musanze)
- **CFP Burera** (Cyeru, Burera)
- **Ecole Technique Gicumbi** (Byumba, Gicumbi)

---

## 🛠️ Troubleshooting

### Setup Script Fails?
```bash
# Manual setup
cd backend
python -m alembic upgrade head
python seed_tvet_schools.py
```

### No Schools Appearing?
1. Check backend is running: `http://localhost:8000/health`
2. Verify schools seeded: See "Check Database" above
3. Check browser console for errors
4. Verify API endpoint: `http://localhost:8000/api/v1/api/locations/schools`

### Dropdowns Not Loading?
1. Check `locations.json` exists in `rwanda-locations-json-master/`
2. Verify backend logs for errors
3. Test API: `http://localhost:8000/api/v1/api/locations/provinces`

### Registration Fails?
- Ensure all fields filled
- Password must be 6+ characters
- Email must be unique
- School must be selected
- Check backend logs

---

## 📚 Documentation

- **Full Guide**: `TVET_SETUP_GUIDE.md`
- **Quick Reference**: `TVET_README.md`
- **Architecture**: `TVET_ARCHITECTURE.md`
- **Implementation**: `IMPLEMENTATION_SUMMARY.md`

---

## 🎉 Success Indicators

You'll know it's working when:
- ✅ Setup script completes without errors
- ✅ Backend starts on port 8000
- ✅ Frontend starts on port 5173
- ✅ `/register` page loads
- ✅ Province dropdown shows 5 options
- ✅ Selecting province loads districts
- ✅ Selecting sector shows schools
- ✅ Registration completes successfully
- ✅ Login works with new account

---

## 🚦 Next Steps

After successful setup:

1. **Explore Registration**
   - Try different provinces
   - See schools in different sectors
   - Test multilingual support

2. **Create Test Accounts**
   - Create student account
   - Create teacher account
   - Test different schools

3. **Verify Data**
   - Check user has location data
   - Verify school_id is correct
   - Test login/logout

4. **Customize**
   - Add more schools
   - Update translations
   - Enhance UI

---

## 💡 Pro Tips

- **Use Kigali for testing**: Most schools are in Kigali
- **Try Kimironko sector**: Has IPRC Kigali
- **Test all languages**: Switch between rw/en/fr
- **Check API docs**: Visit `http://localhost:8000/docs`
- **Use browser DevTools**: Monitor network requests

---

## 📞 Need Help?

1. Check documentation files
2. Review backend logs
3. Check browser console
4. Verify database state
5. Test API endpoints directly

---

## ⏱️ Time Estimates

- **Setup**: 2-3 minutes
- **Testing**: 2-3 minutes
- **Total**: ~5 minutes

---

**Ready? Run `setup-tvet.bat` and get started!** 🎯
