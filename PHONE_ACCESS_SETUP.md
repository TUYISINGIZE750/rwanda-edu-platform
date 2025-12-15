# 📱 ACCESS FROM PHONE - Test Real Live Sessions!

## 🚀 Quick Setup (5 Minutes)

### Step 1: Find Your Laptop's IP Address

**On Windows (Your Laptop):**

1. Open Command Prompt (cmd)
2. Type: `ipconfig`
3. Look for "IPv4 Address" under your active network
4. Example: `192.168.1.100` or `10.0.0.5`

**Write it down:** `192.168.x.x`

### Step 2: Update Backend to Allow Phone Access

**Edit backend config:**

Open: `backend/app/main.py`

Find this line:
```python
allow_origins=["*"],
```

It's already set to allow all origins! ✅

### Step 3: Update Frontend API URL

**Edit frontend config:**

Open: `frontend/src/utils/api.js`

Find:
```javascript
baseURL: 'http://localhost:8080/api/v1'
```

Change to:
```javascript
baseURL: `http://${window.location.hostname}:8080/api/v1`
```

This makes it work on both laptop and phone!

### Step 4: Start Backend with Network Access

**Stop your current backend (Ctrl+C), then run:**

```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

**Important:** `--host 0.0.0.0` allows network access!

### Step 5: Start Frontend with Network Access

**In a new terminal:**

```bash
cd frontend
npm run dev -- --host
```

**You'll see:**
```
  ➜  Local:   http://localhost:5173/
  ➜  Network: http://192.168.1.100:5173/
```

**Copy the Network URL!** (e.g., `http://192.168.1.100:5173`)

### Step 6: Connect from Phone

**On Your Phone:**

1. Make sure phone is on **SAME WiFi** as laptop
2. Open browser (Chrome/Safari)
3. Go to: `http://192.168.x.x:5173` (your Network URL)
4. Login as student: `teststudent1@school.rw` / `password123`

**On Your Laptop:**

1. Go to: `http://localhost:5173` (or the Network URL)
2. Login as teacher: `Elam@gmail.com` / `password123`

## 🎥 Test Real Live Session!

### Test 1: Teacher (Laptop) → Student (Phone)

**Laptop (Teacher):**
1. Go to any channel
2. Click "Go Live"
3. Enter title: "Test from Laptop"
4. Click "Video Call"
5. Allow camera/microphone
6. **Session starts!**

**Phone (Student):**
1. You'll see red banner: "🔴 LIVE NOW: Test from Laptop"
2. Click "Join Now"
3. Allow camera/microphone
4. **You're in!**

**NOW YOU'LL SEE EACH OTHER! 🎉**
- Laptop sees phone's video
- Phone sees laptop's video
- Both can mute/unmute
- Both can turn video on/off

### Test 2: Student (Phone) Requests → Teacher (Laptop) Approves

**Phone (Student):**
1. Click "Go Live"
2. Enter title: "Question from Phone"
3. Click "Audio Only"
4. See: "Live session request sent to teacher"

**Laptop (Teacher):**
1. See "Live Requests" button with badge "1"
2. Click it
3. See student's request
4. Click "✓ Approve"
5. **Session auto-starts!**

**Phone (Student):**
1. See red banner: "🔴 LIVE NOW"
2. Click "Join Now"
3. **Connected!**

**NOW YOU CAN TALK! 🎤**
- Both hear each other's audio
- Test mute buttons
- Real-time communication!

## 🔧 Troubleshooting

### "Can't connect from phone"

**Check:**
1. Both devices on same WiFi network
2. Laptop firewall allows port 8080 and 5173
3. Use correct IP address (run `ipconfig` again)

**Windows Firewall:**
```bash
# Allow ports (run as Administrator)
netsh advfirewall firewall add rule name="Backend" dir=in action=allow protocol=TCP localport=8080
netsh advfirewall firewall add rule name="Frontend" dir=in action=allow protocol=TCP localport=5173
```

### "Camera/Microphone not working"

**On Phone:**
- Browser will ask for permissions
- Tap "Allow" for both camera and microphone
- Check phone settings if blocked

**On Laptop:**
- Click "Allow" when browser asks
- Check Windows privacy settings
- Settings → Privacy → Camera/Microphone

### "Can't see/hear each other"

**Current Setup:**
- You'll see each other's video feeds
- You'll hear each other's audio
- WebRTC uses your browser's built-in peer connection

**If issues:**
1. Refresh both devices
2. Rejoin the session
3. Check camera/mic permissions
4. Try different browser (Chrome works best)

## 📊 What You'll Experience

### Video Quality
- HD video (1280x720)
- Adjusts based on network speed
- May take 2-3 seconds to connect

### Audio Quality
- Clear voice communication
- Echo cancellation built-in
- Low latency

### Controls
- Mute/unmute works instantly
- Video on/off works instantly
- Leave/End session works for both

## 🎯 Success Checklist

- [ ] Phone can access the app
- [ ] Both devices can login
- [ ] Teacher can start live session
- [ ] Student can see "LIVE NOW" banner
- [ ] Student can join session
- [ ] Both see each other's video
- [ ] Both hear each other's audio
- [ ] Mute buttons work
- [ ] Video toggle works
- [ ] Session ends properly

## 🌐 Network Requirements

**Same WiFi Network:**
- Both devices must be on same network
- Router must allow device-to-device communication
- Some public WiFi blocks this (use home WiFi)

**Ports Needed:**
- 8080 (Backend API)
- 5173 (Frontend)
- WebRTC uses random ports (browser handles this)

## 🎉 ENJOY REAL LIVE SESSIONS!

You now have a fully functional live audio/video system that works across devices!

**Test scenarios:**
1. ✅ Laptop teacher → Phone student (video call)
2. ✅ Phone student → Laptop teacher (audio call)
3. ✅ Multiple students joining same session
4. ✅ Teacher ending session for everyone
5. ✅ Students leaving but session continues

**This is REAL WebRTC!** 🚀
