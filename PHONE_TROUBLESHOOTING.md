# 📱 PHONE CONNECTION TROUBLESHOOTING

## 🔍 Step-by-Step Diagnosis

### STEP 1: Test Connection Page

**On your phone, go to:**
```
http://192.168.x.x:5173/test-connection.html
```
(Replace `192.168.x.x` with your laptop's IP)

**This page will:**
- ✅ Show your current URL
- ✅ Show backend URL it's trying to reach
- ✅ Test backend health
- ✅ Test login endpoint
- ✅ Test register endpoint

**Click each button and see what happens!**

### STEP 2: Check Backend is Running Correctly

**On your laptop, make sure you started backend with:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

**NOT:**
```bash
uvicorn app.main:app --reload  ❌ (This only binds to localhost!)
```

**You should see:**
```
INFO:     Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)
```

### STEP 3: Verify Your IP Address

**On laptop, run:**
```bash
ipconfig
```

**Look for the ACTIVE network adapter:**
- If using WiFi: Look under "Wireless LAN adapter Wi-Fi"
- If using Ethernet: Look under "Ethernet adapter"

**Example:**
```
Wireless LAN adapter Wi-Fi:
   IPv4 Address. . . . . . . . . . . : 192.168.1.100  ← USE THIS!
```

### STEP 4: Test Backend from Laptop Browser

**On your laptop, open browser and go to:**
```
http://192.168.x.x:8080/health
```
(Use YOUR IP address)

**You should see:**
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

**If this doesn't work on laptop, backend isn't accessible on network!**

### STEP 5: Check Windows Firewall

**Run as Administrator:**
```bash
# Allow Backend Port
netsh advfirewall firewall add rule name="E-Shuri Backend" dir=in action=allow protocol=TCP localport=8080

# Allow Frontend Port
netsh advfirewall firewall add rule name="E-Shuri Frontend" dir=in action=allow protocol=TCP localport=5173
```

**Or temporarily disable firewall to test:**
```
Control Panel → Windows Defender Firewall → Turn Windows Defender Firewall on or off
→ Turn off (for testing only!)
```

### STEP 6: Verify Same WiFi Network

**On Laptop:**
```bash
ipconfig
```
Look at: `IPv4 Address: 192.168.x.x`

**On Phone:**
- Settings → WiFi → Connected network
- Should show same network name as laptop
- IP should be in same range (e.g., 192.168.1.x)

### STEP 7: Test with Phone Browser Console

**On Phone (Chrome):**
1. Open: `chrome://inspect`
2. Or use Chrome DevTools
3. Check Console for errors

**On Phone (Safari):**
1. Enable Web Inspector on iPhone
2. Connect to Mac
3. Check Safari Developer Tools

### STEP 8: Check Backend Logs

**Look at your backend terminal for errors when phone tries to connect:**

**Good logs:**
```
INFO:     192.168.1.50:54321 - "GET /health HTTP/1.1" 200 OK
INFO:     192.168.1.50:54322 - "POST /api/v1/auth/login HTTP/1.1" 200 OK
```

**Bad logs (CORS error):**
```
WARNING:  CORS: Origin 'http://192.168.1.50:5173' not allowed
```

## 🔧 Common Issues & Fixes

### Issue 1: "Cannot connect to backend"

**Symptoms:**
- Login button does nothing
- Register doesn't work
- No error messages

**Fix:**
```bash
# Stop backend (Ctrl+C)
# Restart with network access:
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

### Issue 2: "CORS Error"

**Symptoms:**
- Browser console shows: "blocked by CORS policy"
- Backend logs show CORS warnings

**Fix:**
Backend `main.py` should have:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ← Should be "*" not specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue 3: "Connection Timeout"

**Symptoms:**
- Page loads but API calls timeout
- Takes forever then fails

**Fix:**
1. Check firewall (see Step 5)
2. Check both devices on same network
3. Try pinging laptop from phone:
   - Use app like "Network Analyzer"
   - Ping `192.168.x.x`

### Issue 4: "Wrong IP Address"

**Symptoms:**
- Can't access from phone
- Works on laptop

**Fix:**
```bash
# Get ALL IP addresses
ipconfig /all

# Look for:
# - Wireless LAN adapter Wi-Fi (if using WiFi)
# - Ethernet adapter (if using cable)
# - NOT "Loopback" or "VirtualBox" adapters!
```

### Issue 5: "Frontend loads but API fails"

**Symptoms:**
- Can see login page on phone
- Login button doesn't work
- Console shows 404 or connection errors

**Fix:**
Check frontend is using correct API URL:
```javascript
// frontend/src/utils/api.js should have:
const hostname = window.location.hostname
const baseURL = `http://${hostname}:8080/api/v1`
```

## 📊 Quick Diagnostic Commands

### On Laptop:

**1. Check if backend is listening on all interfaces:**
```bash
netstat -an | findstr :8080
```
Should show: `0.0.0.0:8080` (not `127.0.0.1:8080`)

**2. Check if frontend is accessible:**
```bash
netstat -an | findstr :5173
```
Should show: `0.0.0.0:5173`

**3. Test backend from laptop:**
```bash
curl http://localhost:8080/health
curl http://192.168.x.x:8080/health
```
Both should work!

### On Phone:

**1. Test connection page:**
```
http://192.168.x.x:5173/test-connection.html
```

**2. Test backend directly:**
```
http://192.168.x.x:8080/health
```

**3. Test frontend:**
```
http://192.168.x.x:5173
```

## ✅ Success Checklist

Work through this checklist:

- [ ] Backend started with `--host 0.0.0.0`
- [ ] Backend shows: "Uvicorn running on http://0.0.0.0:8080"
- [ ] Frontend started with `--host`
- [ ] Frontend shows: "Network: http://192.168.x.x:5173"
- [ ] Laptop can access: `http://192.168.x.x:8080/health`
- [ ] Laptop can access: `http://192.168.x.x:5173`
- [ ] Phone and laptop on SAME WiFi
- [ ] Phone can access: `http://192.168.x.x:5173/test-connection.html`
- [ ] Test page shows "✅ Backend is running!"
- [ ] Test page shows "✅ Login successful!"
- [ ] Windows Firewall allows ports 8080 and 5173
- [ ] No CORS errors in browser console
- [ ] Backend logs show requests from phone IP

## 🎯 Still Not Working?

### Try This:

**1. Restart Everything:**
```bash
# Stop all (Ctrl+C)
# Close all terminals
# Open new terminals
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload

# New terminal
cd frontend
npm run dev -- --host
```

**2. Use Different Port:**
```bash
# If 8080 is blocked, try 8000:
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Update frontend/src/utils/api.js:
# Change :8080 to :8000
```

**3. Check Router Settings:**
- Some routers block device-to-device communication
- Check "AP Isolation" or "Client Isolation" - should be OFF
- Try different WiFi network (mobile hotspot?)

**4. Test with Laptop Browser:**
Before testing on phone, make sure laptop can access:
- `http://192.168.x.x:8080/health` ✅
- `http://192.168.x.x:5173` ✅

If laptop can't access using IP, phone won't either!

## 📞 Need More Help?

**Check these logs:**
1. Backend terminal - any errors?
2. Frontend terminal - any errors?
3. Phone browser console (F12) - any errors?
4. Backend logs when phone tries to connect

**Share these details:**
- Your laptop IP: `192.168.x.x`
- Backend startup message
- Frontend startup message
- Error from test-connection.html page
- Browser console errors
