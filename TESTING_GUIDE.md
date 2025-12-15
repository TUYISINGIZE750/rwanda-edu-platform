# Testing Guide - Rwanda Education Platform

## 🧪 Testing Strategy

This guide covers manual testing workflows for the pilot deployment. Automated tests can be added in future iterations.

---

## 🚀 Pre-Testing Setup

### 1. Start the Platform
```bash
cd rwanda-edu-platform
./deploy.sh
```

Wait for:
- ✅ Backend: http://localhost:8000
- ✅ Frontend: http://localhost:5173
- ✅ Database seeded with 10 schools

### 2. Open Multiple Browser Windows
- Window 1: Teacher account
- Window 2: Student account
- Window 3: API documentation (http://localhost:8000/docs)

---

## 📋 Test Scenarios

### Scenario 1: Authentication Flow

#### Test 1.1: Teacher Login
**Steps:**
1. Navigate to http://localhost:5173
2. Enter email: `teacher1@school1.rw`
3. Enter password: `teacher123`
4. Click "Login"

**Expected:**
- ✅ Redirects to home page
- ✅ Shows list of groups
- ✅ Token stored in localStorage
- ✅ No errors in console

#### Test 1.2: Student Login
**Steps:**
1. Open incognito window
2. Navigate to http://localhost:5173
3. Enter email: `student11@school1.rw`
4. Enter password: `student123`
5. Click "Login"

**Expected:**
- ✅ Redirects to home page
- ✅ Shows student's groups (S1 class + clubs)
- ✅ Token stored in localStorage

#### Test 1.3: Invalid Credentials
**Steps:**
1. Try login with wrong password

**Expected:**
- ✅ Shows error message
- ✅ Stays on login page
- ✅ No token stored

---

### Scenario 2: Teacher Posts Announcement

#### Test 2.1: Create Announcement
**Steps:**
1. Login as teacher1@school1.rw
2. Click on "S1 - Kigali Secondary School"
3. Click on "Announcements" channel
4. Type message: "Welcome to the new term!"
5. Click "Send"

**Expected:**
- ✅ Message appears immediately
- ✅ Status shows "Approved"
- ✅ Timestamp is correct
- ✅ Message saved to database

#### Test 2.2: Schedule Announcement
**Steps:**
1. In Announcements channel
2. Check "Schedule for later"
3. Select tomorrow at 8:00 AM
4. Type message: "Tomorrow's lesson plan"
5. Click "Post Announcement"

**Expected:**
- ✅ Message saved with scheduled_at timestamp
- ✅ Not visible to students yet
- ✅ Will appear at scheduled time

#### Test 2.3: Student Views Announcement
**Steps:**
1. Login as student11@school1.rw (S1 student)
2. Navigate to same class and channel
3. View announcements

**Expected:**
- ✅ Sees teacher's approved message
- ✅ Does NOT see scheduled message
- ✅ Messages in chronological order

---

### Scenario 3: Student Message Approval

#### Test 3.1: Student Posts Message
**Steps:**
1. Login as student11@school1.rw
2. Go to "S1 - Kigali Secondary School"
3. Click "Discussion" channel
4. Type: "Can we have extra math practice?"
5. Click "Send"

**Expected:**
- ✅ Message shows status "Pending"
- ✅ Student sees their own message
- ✅ Other students do NOT see it yet
- ✅ Teacher receives notification

#### Test 3.2: Teacher Approves Message
**Steps:**
1. Login as teacher1@school1.rw
2. Go to "Moderation" page
3. See pending message from student11
4. Click "Approve"

**Expected:**
- ✅ Message status changes to "Approved"
- ✅ All students can now see it
- ✅ Message removed from moderation queue

#### Test 3.3: Teacher Rejects Message
**Steps:**
1. Student posts another message
2. Teacher goes to Moderation
3. Clicks "Reject"

**Expected:**
- ✅ Message status changes to "Rejected"
- ✅ Only student who posted can see it
- ✅ Shows rejection indicator

---

### Scenario 4: DM Request Workflow

#### Test 4.1: Student Requests DM
**Steps:**
1. Login as student11@school1.rw
2. Click "Request DM" or navigate to /dm-requests
3. Select teacher (teacher1)
4. Enter topic: "Math homework help"
5. Enter reason: "I don't understand quadratic equations"
6. Click "Send"

**Expected:**
- ✅ Request created with status "Pending"
- ✅ Student sees confirmation
- ✅ Teacher receives notification

#### Test 4.2: Teacher Views Pending Requests
**Steps:**
1. Login as teacher1@school1.rw
2. Navigate to DM Requests page
3. View pending requests

**Expected:**
- ✅ Sees student11's request
- ✅ Shows topic and reason
- ✅ Shows approve/reject buttons

#### Test 4.3: Teacher Approves DM
**Steps:**
1. Click "Approve" on student11's request
2. Confirm 48-hour window

**Expected:**
- ✅ Request status changes to "Approved"
- ✅ window_start set to now
- ✅ window_end set to now + 48 hours
- ✅ Student can now DM teacher

#### Test 4.4: Teacher Rejects DM
**Steps:**
1. Student12 creates another request
2. Teacher clicks "Reject"

**Expected:**
- ✅ Request status changes to "Rejected"
- ✅ Student12 sees rejection
- ✅ Cannot create DM channel

---

### Scenario 5: Resource Sharing

#### Test 5.1: Teacher Uploads Resource
**Steps:**
1. Login as teacher1@school1.rw
2. Go to "Resources" channel
3. Click "Upload"
4. Select a PDF file (<10MB)
5. Add title: "Chapter 1 Notes"
6. Click "Upload"

**Expected:**
- ✅ File uploads to Supabase Storage
- ✅ Resource card appears
- ✅ Shows file size
- ✅ Download link works

#### Test 5.2: Student Downloads Resource
**Steps:**
1. Login as student11@school1.rw
2. Navigate to Resources channel
3. Click "Download" on teacher's resource

**Expected:**
- ✅ File downloads successfully
- ✅ Cached in IndexedDB for offline access
- ✅ File size displayed correctly

---

### Scenario 6: Content Flagging

#### Test 6.1: Flag Inappropriate Content
**Steps:**
1. Login as student11@school1.rw
2. See another student's message
3. Click "Flag" button
4. Select severity: "Medium"
5. Enter reason: "Inappropriate language"
6. Submit flag

**Expected:**
- ✅ Incident created
- ✅ Teacher notified
- ✅ Message marked for review

#### Test 6.2: Teacher Reviews Flag
**Steps:**
1. Login as teacher1@school1.rw
2. Go to Moderation page
3. View flagged incidents
4. Review the flagged message
5. Take action (hide/dismiss)

**Expected:**
- ✅ Sees incident details
- ✅ Can view original message
- ✅ Can hide message or dismiss flag
- ✅ Decision logged in database

---

### Scenario 7: Office Hours (Jitsi)

#### Test 7.1: Teacher Creates Session
**Steps:**
1. Login as teacher1@school1.rw
2. Go to "Office Hours" channel
3. Click "Create Session"
4. Enter title: "Math Q&A"
5. Select date/time: Tomorrow 2 PM
6. Click "Create"

**Expected:**
- ✅ Session created with Jitsi link
- ✅ Link format: https://meet.jit.si/rwanda-edu-{uuid}
- ✅ Audio-first enabled by default
- ✅ Students can see scheduled session

#### Test 7.2: Student Joins Session
**Steps:**
1. Login as student11@school1.rw
2. Navigate to Office Hours channel
3. Click on scheduled session
4. Click Jitsi link

**Expected:**
- ✅ Opens Jitsi Meet in new tab
- ✅ Audio-first mode active
- ✅ Can join meeting
- ✅ Attendance tracked

---

### Scenario 8: Offline Functionality

#### Test 8.1: Cache Messages Offline
**Steps:**
1. Login as student11@school1.rw
2. View announcements and messages
3. Open browser DevTools → Network tab
4. Set to "Offline"
5. Refresh page

**Expected:**
- ✅ Page loads from Service Worker cache
- ✅ Previously viewed messages visible
- ✅ Can read cached content
- ✅ Shows offline indicator

#### Test 8.2: Queue Message While Offline
**Steps:**
1. While offline, type a new message
2. Click "Send"

**Expected:**
- ✅ Message saved to IndexedDB
- ✅ Shows "Queued for sync" indicator
- ✅ Does not show error

#### Test 8.3: Sync When Back Online
**Steps:**
1. Set network back to "Online"
2. Wait a few seconds

**Expected:**
- ✅ Queued message auto-sends
- ✅ Syncs with server
- ✅ Updates to "Pending" status
- ✅ Clears from queue

---

### Scenario 9: Multilingual Support

#### Test 9.1: Switch to Kinyarwanda
**Steps:**
1. Login to platform
2. Go to Settings
3. Select language: "Kinyarwanda"
4. Save

**Expected:**
- ✅ All UI text changes to Kinyarwanda
- ✅ Navigation labels translated
- ✅ Button text translated
- ✅ Preference saved in localStorage

#### Test 9.2: Switch to French
**Steps:**
1. In Settings, select "Français"
2. Save

**Expected:**
- ✅ All UI text changes to French
- ✅ Translations accurate
- ✅ No missing translations

---

### Scenario 10: Lite Mode

#### Test 10.1: Enable Lite Mode
**Steps:**
1. Go to Settings
2. Toggle "Lite Mode" ON
3. Navigate around the app

**Expected:**
- ✅ Images disabled/deferred
- ✅ Minimal CSS applied
- ✅ Page size <30KB
- ✅ Faster load times

#### Test 10.2: Disable Lite Mode
**Steps:**
1. Toggle "Lite Mode" OFF
2. Navigate around

**Expected:**
- ✅ Full styling restored
- ✅ Images load normally
- ✅ Enhanced UI visible

---

### Scenario 11: Accessibility

#### Test 11.1: Keyboard Navigation
**Steps:**
1. Login to platform
2. Use only Tab, Enter, and Arrow keys
3. Navigate through all pages

**Expected:**
- ✅ Can reach all interactive elements
- ✅ Focus indicators visible
- ✅ Logical tab order
- ✅ Can submit forms with Enter

#### Test 11.2: High Contrast Mode
**Steps:**
1. Go to Settings
2. Enable "High Contrast"
3. View all pages

**Expected:**
- ✅ Text clearly readable
- ✅ Sufficient color contrast
- ✅ Borders more prominent
- ✅ WCAG AA compliant

---

### Scenario 12: Realtime Chat (WebSocket)

#### Test 12.1: Realtime Message Delivery
**Steps:**
1. Open two browser windows
2. Window 1: Login as teacher1@school1.rw
3. Window 2: Login as student11@school1.rw
4. Both navigate to same Discussion channel
5. Teacher posts message

**Expected:**
- ✅ Student sees message instantly (no refresh)
- ✅ WebSocket connection active
- ✅ Message appears in real-time
- ✅ No polling required

#### Test 12.2: WebSocket Reconnection
**Steps:**
1. Open DevTools → Network
2. Disconnect WebSocket
3. Wait 5 seconds
4. Send a message

**Expected:**
- ✅ WebSocket auto-reconnects
- ✅ Message still delivers
- ✅ No data loss
- ✅ Graceful fallback

---

## 🔍 API Testing (via Swagger UI)

### Access API Docs
Navigate to: http://localhost:8000/docs

### Test 1: Authentication
1. Expand `POST /api/v1/auth/login`
2. Click "Try it out"
3. Enter:
   ```json
   {
     "email": "teacher1@school1.rw",
     "password": "teacher123"
   }
   ```
4. Click "Execute"

**Expected:**
- ✅ Status 200
- ✅ Returns access_token
- ✅ Returns user object

### Test 2: Get Groups (Authenticated)
1. Copy access_token from login
2. Click "Authorize" button at top
3. Enter: `Bearer {access_token}`
4. Expand `GET /api/v1/directory/groups`
5. Click "Try it out" → "Execute"

**Expected:**
- ✅ Status 200
- ✅ Returns array of groups
- ✅ Groups match user's school

### Test 3: Send Message
1. Expand `POST /api/v1/messages/`
2. Enter:
   ```json
   {
     "channel_id": 1,
     "content": "Test message from API",
     "attachments": []
   }
   ```
3. Execute

**Expected:**
- ✅ Status 200
- ✅ Message created
- ✅ Correct status (approved for teacher)

---

## 📊 Performance Testing

### Test 1: Page Load Time (3G)
**Steps:**
1. Open DevTools → Network
2. Set throttling to "Slow 3G"
3. Hard refresh page (Ctrl+Shift+R)
4. Measure load time

**Expected:**
- ✅ Initial load: <3 seconds
- ✅ Subsequent loads: <1 second (cached)

### Test 2: API Response Time
**Steps:**
1. Open DevTools → Network
2. Perform various actions
3. Check API response times

**Expected:**
- ✅ GET requests: <200ms
- ✅ POST requests: <500ms
- ✅ File uploads: <2s for 1MB

### Test 3: Bundle Size
**Steps:**
1. Build frontend: `npm run build`
2. Check `dist/` folder size

**Expected:**
- ✅ Total bundle: <500KB
- ✅ Initial JS: <100KB
- ✅ CSS: <50KB

---

## 🐛 Bug Reporting Template

When you find a bug, report it with:

```markdown
**Bug Title**: [Short description]

**Steps to Reproduce**:
1. Step 1
2. Step 2
3. Step 3

**Expected Behavior**:
What should happen

**Actual Behavior**:
What actually happened

**Environment**:
- Browser: Chrome 120
- OS: Windows 11
- User role: Teacher
- Network: 3G

**Screenshots**:
[Attach if applicable]

**Console Errors**:
[Copy from DevTools console]
```

---

## ✅ Testing Checklist

Before declaring pilot-ready, verify:

### Authentication
- [ ] Teacher login works
- [ ] Student login works
- [ ] Invalid credentials rejected
- [ ] Token persists across refresh
- [ ] Logout clears token

### Messaging
- [ ] Teacher posts auto-approved
- [ ] Student posts pending
- [ ] Teacher can approve/reject
- [ ] Realtime delivery works
- [ ] Offline queueing works

### DM Requests
- [ ] Student can request DM
- [ ] Teacher sees pending requests
- [ ] Approval creates time window
- [ ] Rejection prevents DM
- [ ] Window expires after 48h

### Resources
- [ ] Teacher can upload files
- [ ] Students can download
- [ ] Files cached offline
- [ ] File size limits enforced

### Moderation
- [ ] Flagging system works
- [ ] Teacher sees flagged content
- [ ] Can hide/dismiss flags
- [ ] Audit trail maintained

### Offline
- [ ] Service Worker caches assets
- [ ] IndexedDB stores messages
- [ ] Offline indicator shows
- [ ] Sync works when online

### Internationalization
- [ ] Kinyarwanda translations complete
- [ ] English translations complete
- [ ] French translations complete
- [ ] Language switching works

### Accessibility
- [ ] Keyboard navigation works
- [ ] High contrast mode works
- [ ] Focus indicators visible
- [ ] Screen reader compatible

### Performance
- [ ] Loads <3s on 3G
- [ ] API responses <500ms
- [ ] Bundle size <500KB
- [ ] Lite mode <30KB

---

## 📞 Support

If tests fail or you need help:
1. Check [QUICK_REFERENCE.md](QUICK_REFERENCE.md) → Troubleshooting
2. Review browser console for errors
3. Check backend logs: `docker-compose logs backend`
4. Verify database: `docker-compose exec postgres psql -U user -d rwanda_edu`

---

**Happy Testing! 🧪**
