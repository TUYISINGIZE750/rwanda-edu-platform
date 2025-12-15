# 📱 PHONE ACCESS - EASY START

## ⚡ Super Quick Method (30 Seconds!)

### Step 1: Get Your IP (10 seconds)
```bash
ipconfig
```
**Write down:** `192.168.___.___ ` (your IPv4 Address)

### Step 2: Start Backend (10 seconds)
**Double-click:** `START_BACKEND_NETWORK.bat`

**Or manually:**
```bash
cd backend
venv\Scripts\activate
python -m uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

**Wait for:** `Uvicorn running on http://0.0.0.0:8080`

### Step 3: Start Frontend (10 seconds)
**Double-click:** `START_FRONTEND_NETWORK.bat`

**Or manually:**
```bash
cd frontend
npm run dev -- --host
```

**Copy the Network URL:** `http://192.168.x.x:5173`

## 🎯 Test It!

### On Laptop:
```
http://localhost:5173
```
Login: `Elam@gmail.com` / `password123`

### On Phone:
```
http://192.168.x.x:5173
```
(Use YOUR IP!)
Login: `teststudent1@school.rw` / `password123`

## ✅ Quick Test

**On phone, go to:**
```
http://192.168.x.x:5173/test-connection.html
```

**Click buttons - should see:**
- ✅ Backend is running!
- ✅ Login successful!

## 🔧 If It Doesn't Work

### Problem: "uvicorn not recognized"

**Solution:**
```bash
cd backend
venv\Scripts\activate
python -m uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

### Problem: "Can't access from phone"

**Solution:**
1. Check both on same WiFi
2. Test on laptop first: `http://192.168.x.x:8080/health`
3. If laptop fails, check firewall:
   ```bash
   # Run as Administrator
   netsh advfirewall firewall add rule name="Backend" dir=in action=allow protocol=TCP localport=8080
   netsh advfirewall firewall add rule name="Frontend" dir=in action=allow protocol=TCP localport=5173
   ```

### Problem: "Backend starts but phone can't connect"

**Check backend shows:**
```
Uvicorn running on http://0.0.0.0:8080
```
NOT `http://127.0.0.1:8080`

If it shows `127.0.0.1`, you forgot `--host 0.0.0.0`!

## 📋 Commands Reference

### Start Backend (with venv):
```bash
cd backend
venv\Scripts\activate
python -m uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

### Start Frontend:
```bash
cd frontend
npm run dev -- --host
```

### Get IP:
```bash
ipconfig
```

### Test Backend:
```bash
# On laptop browser:
http://192.168.x.x:8080/health
```

### Allow Firewall:
```bash
# Run as Administrator
netsh advfirewall firewall add rule name="Backend" dir=in action=allow protocol=TCP localport=8080
netsh advfirewall firewall add rule name="Frontend" dir=in action=allow protocol=TCP localport=5173
```

## 🎉 That's It!

Use the `.bat` files or the manual commands above!
