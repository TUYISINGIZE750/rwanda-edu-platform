# ✅ PHONE CONNECTION CHECKLIST

## Before You Start

### 1. Get Your IP Address
```bash
ipconfig
```
**Write down:** `192.168.___.___ ` ← Your IP

### 2. Start Backend (IMPORTANT!)
```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```
**Must see:** `Uvicorn running on http://0.0.0.0:8080`

### 3. Start Frontend
```bash
cd frontend
npm run dev -- --host
```
**Must see:** `Network: http://192.168.x.x:5173`

## Test on Laptop First

### 4. Test Backend with IP
**Open browser on laptop:**
```
http://192.168.x.x:8080/health
```
**Must see:** `{"status": "healthy", "version": "1.0.0"}`

❌ **If this fails, phone won't work either!**

### 5. Test Frontend with IP
**Open browser on laptop:**
```
http://192.168.x.x:5173
```
**Must see:** Login page loads

❌ **If this fails, fix it before trying phone!**

## Test on Phone

### 6. Check WiFi
- [ ] Phone on SAME WiFi as laptop
- [ ] WiFi name matches laptop's WiFi

### 7. Test Connection Page
**On phone browser:**
```
http://192.168.x.x:5173/test-connection.html
```

**Click buttons:**
- [ ] "Test Backend Health" → ✅ Backend is running!
- [ ] "Test Login" → ✅ Login successful!

❌ **If tests fail, see PHONE_TROUBLESHOOTING.md**

### 8. Test Main App
**On phone browser:**
```
http://192.168.x.x:5173
```

**Try:**
- [ ] Login page loads
- [ ] Can type in fields
- [ ] Login button works
- [ ] Can login successfully

## Common Fixes

### Backend Not Accessible

**Problem:** Can't access `http://192.168.x.x:8080/health` from laptop

**Fix:**
```bash
# Stop backend (Ctrl+C)
# Restart with correct command:
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
#                     ^^^^^^^^^^^^^^^^ IMPORTANT!
```

### Firewall Blocking

**Problem:** Backend works on localhost but not on IP

**Fix (Run as Administrator):**
```bash
netsh advfirewall firewall add rule name="Backend" dir=in action=allow protocol=TCP localport=8080
netsh advfirewall firewall add rule name="Frontend" dir=in action=allow protocol=TCP localport=5173
```

### Wrong IP Address

**Problem:** Using wrong IP

**Fix:**
```bash
ipconfig
# Look for "Wireless LAN adapter Wi-Fi"
# NOT "Loopback" or "VirtualBox"
# Use the IPv4 Address shown there
```

### Different WiFi Networks

**Problem:** Devices on different networks

**Fix:**
- Check laptop WiFi name
- Check phone WiFi name
- Must be EXACTLY the same
- Both should have IPs like 192.168.1.x

## Quick Debug

**On laptop, check if backend is listening on network:**
```bash
netstat -an | findstr :8080
```
**Must show:** `0.0.0.0:8080` (not `127.0.0.1:8080`)

**On laptop, check if frontend is accessible:**
```bash
netstat -an | findstr :5173
```
**Must show:** `0.0.0.0:5173`

## Success Indicators

**You'll know it's working when:**

✅ Laptop can access: `http://192.168.x.x:8080/health`
✅ Laptop can access: `http://192.168.x.x:5173`
✅ Phone can access: `http://192.168.x.x:5173/test-connection.html`
✅ Test page shows all green checkmarks
✅ Phone can login to main app
✅ Backend logs show phone's IP address

## Still Not Working?

**Read:** `PHONE_TROUBLESHOOTING.md` for detailed help

**Or try:**
1. Restart both servers
2. Restart phone WiFi
3. Try different browser on phone
4. Temporarily disable Windows Firewall
5. Use mobile hotspot instead of WiFi router
