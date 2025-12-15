# 📋 COMMANDS CHEAT SHEET - Phone Access

## 🚀 Quick Commands

### 1. Find Your IP
```bash
ipconfig
```
Look for: `IPv4 Address. . . . . . . . . . . : 192.168.x.x`

### 2. Start Backend (Network Mode)
```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

### 3. Start Frontend (Network Mode)
```bash
cd frontend
npm run dev -- --host
```

### 4. Allow Firewall (If Needed)
```bash
# Run as Administrator
netsh advfirewall firewall add rule name="Backend" dir=in action=allow protocol=TCP localport=8080
netsh advfirewall firewall add rule name="Frontend" dir=in action=allow protocol=TCP localport=5173
```

## 🌐 URLs

| Device | URL | Login |
|--------|-----|-------|
| **Laptop** | `http://localhost:5173` | Teacher: `Elam@gmail.com` / `password123` |
| **Phone** | `http://192.168.x.x:5173` | Student: `teststudent1@school.rw` / `password123` |

## 🎯 Quick Test Flow

### Teacher (Laptop):
```
1. Click "Go Live" 🎥
2. Enter title
3. Click "Video Call"
4. Allow camera/mic
5. ✓ Session starts
```

### Student (Phone):
```
1. See "🔴 LIVE NOW" banner
2. Tap "Join Now"
3. Allow camera/mic
4. ✓ Connected!
```

## 🔧 Troubleshooting Commands

### Check if Backend is Running
```bash
netstat -an | findstr :8080
```
Should show: `0.0.0.0:8080`

### Check if Frontend is Running
```bash
netstat -an | findstr :5173
```
Should show: `0.0.0.0:5173`

### Restart Everything
```bash
# Stop all (Ctrl+C in each terminal)
# Then restart:
cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
cd frontend && npm run dev -- --host
```

## 📱 Phone Browser Settings

### Chrome (Android):
```
Settings → Site Settings → Camera → Allow
Settings → Site Settings → Microphone → Allow
```

### Safari (iPhone):
```
Settings → Safari → Camera → Allow
Settings → Safari → Microphone → Allow
```

## ✅ Success Checklist

- [ ] Backend shows: `Uvicorn running on 0.0.0.0:8080`
- [ ] Frontend shows: `Network: http://192.168.x.x:5173`
- [ ] Phone can access the URL
- [ ] Both can login
- [ ] Camera/mic permissions granted
- [ ] Can see/hear each other
- [ ] Controls work (mute/video)

## 🎉 That's It!

Copy these commands and you're ready to test live sessions between devices!
