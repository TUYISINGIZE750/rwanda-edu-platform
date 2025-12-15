# 📱 PHONE ACCESS - 3 MINUTE SETUP

## 🎯 Goal
Test REAL live audio/video between your laptop and phone!

## ⚡ Quick Steps

### 1️⃣ Find Your Laptop IP (30 seconds)

**Open Command Prompt and type:**
```bash
ipconfig
```

**Look for "IPv4 Address":**
```
IPv4 Address. . . . . . . . . . . : 192.168.1.100
```

**Write it down:** `192.168.1.100` (yours will be different)

### 2️⃣ Stop Current Servers (10 seconds)

- Press `Ctrl+C` in backend terminal
- Press `Ctrl+C` in frontend terminal

### 3️⃣ Start Backend with Network Access (20 seconds)

```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

**Wait for:** `Application startup complete`

### 4️⃣ Start Frontend with Network Access (20 seconds)

**Open NEW terminal:**
```bash
cd frontend
npm run dev -- --host
```

**You'll see:**
```
➜  Local:   http://localhost:5173/
➜  Network: http://192.168.1.100:5173/
```

**Copy the Network URL!**

### 5️⃣ Open on Laptop (10 seconds)

**Browser on laptop:**
- Go to: `http://localhost:5173`
- Login: `Elam@gmail.com` / `password123` (Teacher)

### 6️⃣ Open on Phone (30 seconds)

**On your phone:**
1. Connect to **SAME WiFi** as laptop
2. Open Chrome/Safari
3. Go to: `http://192.168.1.100:5173` (use YOUR IP!)
4. Login: `teststudent1@school.rw` / `password123` (Student)

## 🎥 Test Live Session!

### Laptop (Teacher):
1. Go to any channel
2. Click **"Go Live"** 🎥
3. Type: "Test Call"
4. Click **"Video Call"**
5. Allow camera/mic
6. **Session starts!**

### Phone (Student):
1. See red banner: **"🔴 LIVE NOW: Test Call"**
2. Click **"Join Now"**
3. Allow camera/mic
4. **You're connected!**

## ✅ SUCCESS!

**You should now:**
- ✅ See each other's video
- ✅ Hear each other's audio
- ✅ Be able to mute/unmute
- ✅ Be able to turn video on/off

## 🔥 Test Audio Only

### Phone (Student):
1. Click **"Go Live"**
2. Type: "Audio Question"
3. Click **"Audio Only"** 🎤
4. See: "Request sent to teacher"

### Laptop (Teacher):
1. See **"Live Requests"** badge (1)
2. Click it
3. Click **"✓ Approve"**
4. **Session auto-starts!**

### Phone (Student):
1. See **"🔴 LIVE NOW"** banner
2. Click **"Join Now"**
3. **Talk to each other!** 🎤

## ❌ Troubleshooting

### "Can't access from phone"

**Check:**
- [ ] Both on same WiFi
- [ ] Used correct IP address
- [ ] Backend shows: `0.0.0.0:8080`
- [ ] Frontend shows Network URL

**Windows Firewall Fix:**
```bash
# Run as Administrator
netsh advfirewall firewall add rule name="Backend" dir=in action=allow protocol=TCP localport=8080
netsh advfirewall firewall add rule name="Frontend" dir=in action=allow protocol=TCP localport=5173
```

### "Camera/Mic not working"

- Click "Allow" when browser asks
- Check phone settings → Browser → Permissions
- Try Chrome (works best)

### "Can't see/hear each other"

- Refresh both devices
- Rejoin the session
- Check permissions again
- Make sure both in same session

## 📝 Quick Reference

**Laptop IP:** `192.168.x.x` (your IP)

**URLs:**
- Laptop: `http://localhost:5173`
- Phone: `http://192.168.x.x:5173`

**Logins:**
- Teacher: `Elam@gmail.com` / `password123`
- Student: `teststudent1@school.rw` / `password123`

**Ports:**
- Backend: `8080`
- Frontend: `5173`

## 🎉 ENJOY!

You now have REAL live audio/video working between devices!

**Test everything:**
- Video calls
- Audio calls
- Mute/unmute
- Video on/off
- Multiple participants
- Teacher controls
- Student requests
