# 🎯 COMPLETE USER GUIDE - All Features for Admin, Teacher & Student

## 🌐 System Access
**URL**: https://tssanywhere.pages.dev

---

## 👨‍💼 ADMIN/DOS USER GUIDE

### Login
1. Go to https://tssanywhere.pages.dev/admin-login
2. Enter admin credentials
3. Role: ADMIN or DOS

### Admin Dashboard Features

#### 1. **User Management** (`/admin/users`)
- View all users (students, teachers)
- Create new users
- Edit user details
- Assign roles
- Delete users
- **Assign Class Teachers**:
  ```
  Edit teacher → Set "is_class_teacher" = true
  ```

#### 2. **Class/Group Management** (`/admin/modules`)
- View all classes and groups
- Create new classes
- Assign teachers to classes
- View class members
- Delete classes

#### 3. **Analytics Dashboard** (`/admin/analytics`)
- Total students count
- Total teachers count
- Active classes
- Resource uploads
- User activity graphs

#### 4. **Content Moderation** (`/admin/moderation`)
- Review pending messages
- Approve/reject student messages
- View flagged content
- Moderate discussions

#### 5. **School Settings** (`/admin/settings`)
- Configure school details
- Manage departments/trades
- Set permissions
- System configuration

#### 6. **Backup & Reports** (`/admin/backup`)
- Download database backups
- Generate reports
- Export user data
- System logs

### Admin API Endpoints
```
GET  /api/v1/admin/users              - List all users
POST /api/v1/admin/users              - Create user
PUT  /api/v1/admin/users/{id}         - Update user
DELETE /api/v1/admin/users/{id}       - Delete user
GET  /api/v1/admin/analytics          - Get analytics
GET  /api/v1/admin/moderation         - Pending messages
POST /api/v1/admin/assign-teacher     - Assign class teacher
```

---

## 👨‍🏫 TEACHER USER GUIDE

### Login
1. Go to https://tssanywhere.pages.dev
2. Click "Login"
3. Enter teacher credentials
4. Role: TEACHER

### Teacher Dashboard (`/teacher-dashboard`)

#### A. CLASS TEACHER (Assigned by Admin)
**Features Available**:

##### 1. **Create Classes** ✅
- Click "Create Class" button
- Enter class name (e.g., "L5 Software Development")
- Select department from dropdown (real school trades)
- Select level (1-6)
- System auto-assigns matching students
- Confirmation: "X students auto-assigned"

##### 2. **Create Groups/Clubs** ✅
- Click "Create Group" button
- Enter group name
- Select type: Club, Group, Discussion
- Add description
- Create

##### 3. **Upload Resources** ✅
- Go to class hub (`/hubs/{class_id}`)
- Click "Upload Resource"
- Select file (PDF, DOC, PPT, etc.)
- Add title and description
- Upload
- **All students in class get notification instantly**

##### 4. **Manage Classes** ✅
- View all your classes
- Click class → Open hub
- See channels: Announcements, Discussion, Resources
- Post messages
- Moderate student messages

##### 5. **View Notifications** ✅
- Click bell icon (top right)
- See all notifications
- Click notification → Navigate to resource
- Mark as read

#### B. REGULAR TEACHER (Assigned to Groups)
**Features Available**:
- View assigned groups only
- Manage group content
- Upload resources to assigned groups
- Moderate messages in assigned groups
- **Cannot create new classes** (permission restricted)

#### C. UNASSIGNED TEACHER
**What They See**:
- Waiting message: "⏳ Waiting for assignment"
- No create buttons
- Dashboard shows: "Contact DOS for assignment"

### Teacher API Endpoints
```
GET  /api/v1/teacher/dashboard        - Get dashboard data
POST /api/v1/teacher/groups           - Create class/group
GET  /api/v1/teacher/groups/{id}      - Get class details
POST /api/v1/teacher/resources        - Upload resource (triggers notifications)
GET  /api/v1/teacher/resources        - Get teacher's resources
GET  /api/v1/teacher/pending-messages - Messages to moderate
POST /api/v1/teacher/messages/{id}/approve - Approve message
POST /api/v1/teacher/messages/{id}/reject  - Reject message
```

---

## 👨‍🎓 STUDENT USER GUIDE

### Login
1. Go to https://tssanywhere.pages.dev
2. Click "Login"
3. Enter student credentials
4. Role: STUDENT

### Student Dashboard (`/student-dashboard`)

#### Features Available:

##### 1. **View Classes** ✅
- See all enrolled classes
- Click class card → Open class hub
- View class details:
  - Class name
  - Member count
  - Channels count

##### 2. **Notification System** ✅
- **Bell icon** (top right) shows unread count
- Red badge: "5" = 5 unread notifications
- Click bell → See all notifications:
  - 📚 New Resource uploaded
  - 📢 New Announcement
  - 💬 New Message
  - ✅ Message Approved
  - ❌ Message Rejected
- Click notification → Navigate to resource/class
- Auto-marks as read when clicked

##### 3. **Class Hub** (`/hubs/{class_id}`)
- View channels:
  - **Announcements**: Teacher posts only
  - **Discussion**: Student discussions
  - **Resources**: Download materials
- Post messages (pending teacher approval)
- Download resources
- View classmates

##### 4. **Download Resources** ✅
- Go to class hub
- Click "Resources" channel
- See all uploaded files
- Click download button
- Files saved to device

##### 5. **Inter-School Connect** (`/inter-school`)
- Connect with students from other schools
- Join nationwide discussions
- Share experiences
- Network across 165 schools

##### 6. **Direct Messages** (`/direct-messages`)
- Send DM requests to classmates
- Chat privately
- View DM history

##### 7. **Profile** (`/profile`)
- View your profile
- Edit details
- See enrolled classes
- View activity

### Student API Endpoints
```
GET  /api/v1/student/dashboard        - Get dashboard data
GET  /api/v1/student/classes          - Get enrolled classes
GET  /api/v1/notifications/           - Get notifications
GET  /api/v1/notifications/unread-count - Unread count
PUT  /api/v1/notifications/{id}/read  - Mark as read
GET  /api/v1/groups/{id}/resources    - Get class resources
POST /api/v1/messages                 - Post message (pending approval)
GET  /api/v1/inter-school/students    - Inter-school connect
```

---

## 🔄 COMPLETE WORKFLOW EXAMPLES

### Example 1: Teacher Uploads Resource → Student Gets Notified

**Teacher Side**:
1. Login as Class Teacher
2. Go to Dashboard → Click class
3. Click "Upload Resource"
4. Select PDF file: "Python Tutorial.pdf"
5. Add title: "Python Basics"
6. Click Upload
7. System shows: "Resource uploaded! 45 students notified"

**Student Side**:
1. Student is browsing dashboard
2. Notification bell badge appears: "1"
3. Student clicks bell
4. Sees: "📚 New Resource: Python Basics"
5. Message: "Teacher John uploaded a new document in L5 Software Development"
6. Student clicks notification
7. Redirected to class hub → Resources channel
8. Downloads "Python Tutorial.pdf"
9. Notification marked as read
10. Badge count decreases

### Example 2: Admin Assigns Class Teacher

**Admin Side**:
1. Login as Admin/DOS
2. Go to `/admin/users`
3. Find teacher: "John Doe"
4. Click "Edit"
5. Set "is_class_teacher" = true
6. Optionally assign to existing class
7. Save

**Teacher Side**:
1. Teacher John logs in
2. Dashboard now shows "Create Class" button
3. Can create and manage classes
4. Has full permissions

### Example 3: Create Class with Auto-Assignment

**Teacher Side**:
1. Login as Class Teacher
2. Click "Create Class"
3. Enter name: "L5 Software Development"
4. Select department: "Software Development"
5. Select level: 5
6. Click Create
7. System matches: Level 5 + Software Development
8. Auto-assigns all matching students
9. Shows: "Class created! 45 students auto-assigned"

**Student Side**:
1. Students with Level 5 + Software Development
2. Automatically see new class on dashboard
3. Can access class immediately
4. No manual enrollment needed

---

## 🔐 PERMISSION MATRIX

| Feature | Admin | Class Teacher | Regular Teacher | Student |
|---------|-------|---------------|-----------------|---------|
| Create Classes | ✅ | ✅ | ❌ | ❌ |
| Create Groups | ✅ | ✅ | ❌ | ❌ |
| Upload Resources | ✅ | ✅ | ✅* | ❌ |
| Moderate Messages | ✅ | ✅ | ✅* | ❌ |
| View All Users | ✅ | ❌ | ❌ | ❌ |
| Assign Teachers | ✅ | ❌ | ❌ | ❌ |
| Receive Notifications | ✅ | ✅ | ✅ | ✅ |
| Download Resources | ✅ | ✅ | ✅ | ✅ |
| Post Messages | ✅ | ✅ | ✅ | ✅** |
| Inter-School Connect | ❌ | ❌ | ❌ | ✅ |

*Only in assigned groups  
**Requires teacher approval

---

## 🎯 TESTING CHECKLIST

### Test as Admin:
- [ ] Login with admin credentials
- [ ] View users list
- [ ] Create new teacher
- [ ] Assign teacher as class teacher
- [ ] View analytics
- [ ] Check moderation queue

### Test as Class Teacher:
- [ ] Login with teacher credentials
- [ ] See "Create Class" button
- [ ] Create class with auto-assignment
- [ ] Upload resource
- [ ] Check notification sent
- [ ] View class members

### Test as Student:
- [ ] Login with student credentials
- [ ] See enrolled classes
- [ ] Click notification bell
- [ ] See notification badge
- [ ] Click notification
- [ ] Navigate to resource
- [ ] Download resource
- [ ] Badge count decreases

---

## 📞 QUICK ACCESS URLS

### Public Pages:
- Landing: https://tssanywhere.pages.dev
- Login: https://tssanywhere.pages.dev/login
- Register: https://tssanywhere.pages.dev/register

### Student Pages:
- Dashboard: `/student-dashboard`
- Class Hub: `/hubs/{class_id}`
- Profile: `/profile`
- Inter-School: `/inter-school`
- Direct Messages: `/direct-messages`

### Teacher Pages:
- Dashboard: `/teacher-dashboard`
- Upload Resource: `/upload-resource`
- My Resources: `/my-resources`
- Moderation: `/moderation`

### Admin Pages:
- Dashboard: `/admin-dashboard`
- Users: `/admin/users`
- Analytics: `/admin/analytics`
- Moderation: `/admin/moderation`
- Settings: `/admin/settings`
- Backup: `/admin/backup`

---

## ✅ ALL ROUTES VERIFIED

**Backend Routes**: ✅ All registered in main.py
**Frontend Routes**: ✅ All configured in router
**Notifications**: ✅ Live and operational
**Permissions**: ✅ Properly enforced
**Database**: ✅ Migration completed

---

**System Status**: 🟢 FULLY OPERATIONAL  
**All Features**: ✅ WORKING  
**Ready for Use**: ✅ YES
