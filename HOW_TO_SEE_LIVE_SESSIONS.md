# 🎥 HOW TO SEE LIVE AUDIO/VIDEO SESSIONS WORKING

## Step-by-Step Demo Guide

### SETUP (Do This First)

1. **Restart Backend:**
   ```bash
   cd backend
   uvicorn app.main:app --reload --port 8080
   ```

2. **Refresh Frontend:**
   - Press `Ctrl+F5` to clear cache
   - Login as teacher: `Elam@gmail.com` / `password123`

### DEMO 1: Teacher Starts Live Session (Instant)

**As Teacher:**

1. Go to any channel (e.g., "General Discussion")

2. Click the **"Go Live"** button (🎥 red/pink gradient button)

3. Enter a title: `"Math Lesson"`

4. Click **"Video Call"** (or "Audio Only")

5. **BOOM! 💥 Live session opens immediately!**
   - You'll see:
     - ✅ Your camera/microphone feed
     - ✅ "LIVE 00:00" timer counting up
     - ✅ Demo participants joining (2-3 people)
     - ✅ Mute/Video controls at bottom
     - ✅ Full-screen live interface

6. **Test Controls:**
   - Click 🎤 to mute/unmute
   - Click 📹 to turn video on/off
   - See the timer counting: 00:01, 00:02, 00:03...

7. Click **"End Session"** when done

### DEMO 2: Student Requests → Teacher Approves

**Open TWO Browser Windows:**

**Window 1 - Student:**
1. Login as student: `teststudent1@school.rw` / `password123`
2. Go to same channel
3. Click **"Go Live"**
4. Enter title: `"Question about homework"`
5. Click **"Audio Only"**
6. See notification: "Live session request sent to teacher"

**Window 2 - Teacher:**
1. Look for **"Live Requests"** button (purple, should show "1")
2. Click it to open pending requests
3. See student's request with title and name
4. Click **"✓ Approve"**
5. **BOOM! 💥 Live session auto-starts!**
6. Both teacher and student see the live interface

**Back to Window 1 - Student:**
1. See red banner: "🔴 LIVE NOW: Question about homework"
2. Click **"Join Now"**
3. **BOOM! 💥 Student enters live session!**
4. See your audio/video feed
5. See teacher and other participants

### WHAT YOU'LL SEE IN LIVE SESSION

**Visual Elements:**

1. **Header Bar (Top):**
   - Session title
   - "LIVE 00:15" timer (animated, pulsing)
   - Participant count
   - "End Session" button (host/teacher)
   - "Leave" button

2. **Video Grid (Center):**
   - **Your Video:** Your camera feed with "You 🔇/🎤" label
   - **Participants:** 2-3 demo participants with:
     - Colorful gradient backgrounds
     - Large avatar circles with initials
     - Names below
     - Green pulse indicator (online)
     - "📹 Video On" or "🎤 Audio Only" status

3. **Controls (Bottom):**
   - 🎤 Microphone button (click to mute/unmute)
     - Red when muted
     - Gray when active
   - 📹 Camera button (video sessions only)
     - Red when off
     - Gray when active

4. **Live Banner (In Chat):**
   - When session is active but you're not in it
   - Red/pink gradient with pulse animation
   - "🔴 LIVE NOW" text
   - "Join Now" button

### AUDIO vs VIDEO Differences

**Audio Only Session:**
- No camera feed (just audio waveform or avatar)
- Only microphone control
- Lower bandwidth
- Participants show as avatars with "🎤 Audio Only"

**Video Session:**
- Full camera feed
- Both microphone and camera controls
- HD video quality
- Participants show video or "📹 Video On" status

### TESTING CHECKLIST

- [ ] Teacher can start session instantly
- [ ] Student request shows in "Live Requests" button
- [ ] Teacher can approve/reject requests
- [ ] Live session opens in full screen
- [ ] Timer counts up (00:00, 00:01, 00:02...)
- [ ] Demo participants appear after 2 seconds
- [ ] Mute button works (toggles red/gray)
- [ ] Video button works (video sessions)
- [ ] "LIVE NOW" banner shows in chat
- [ ] "Join Now" button works
- [ ] "End Session" closes for everyone
- [ ] "Leave" exits but session continues

### TROUBLESHOOTING

**"Failed to access camera/microphone"**
- Browser will ask for permissions
- Click "Allow" when prompted
- Check browser settings if blocked

**"No participants showing"**
- Wait 2 seconds after joining
- Demo participants auto-appear
- Real WebRTC connections would show here

**"Live Requests button not showing"**
- Must be logged in as teacher
- Button always visible (shows "0" if no requests)
- Refresh page if needed

### WHAT'S HAPPENING BEHIND THE SCENES

1. **Database:** Live session created with status PENDING/APPROVED/ACTIVE
2. **WebRTC:** Browser accesses your camera/microphone
3. **Demo Mode:** Simulated participants show the interface works
4. **Real Mode:** Would connect actual peer-to-peer video/audio streams
5. **Polling:** Every 3 seconds checks for new sessions/requests

### NEXT STEPS FOR PRODUCTION

To make this work with REAL participants (not demo):
1. Add WebRTC signaling server (Socket.io)
2. Implement peer connection logic
3. Exchange ICE candidates
4. Stream actual video/audio between peers

But for NOW, you can SEE and TEST the complete UI and workflow! 🎉
