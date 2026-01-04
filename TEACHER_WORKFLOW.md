# TSSANYWHERE Teacher Workflow

## Overview
This document explains how teachers create and manage classes in TSSANYWHERE platform.

---

## 🎯 Who Creates Classes?

**TEACHERS create their own classes** - This is the standard workflow in education platforms.

### Two Types of Teachers:

1. **Class Teachers** (DOS-assigned)
   - Assigned by admin via `is_class_teacher` flag
   - Can create classes and groups
   - Manage their assigned class

2. **Regular Teachers**
   - Can be assigned to classes by admin
   - Can also create their own classes
   - Add lessons to classes they have access to

---

## 📚 Complete Workflow

### Step 1: Teacher Creates a Class

**Endpoint**: `POST /teacher/groups`

**Request**:
```json
{
  "name": "L5 Software Development",
  "type": "CLASS",
  "department": "Software Development",
  "grade": 5
}
```

**What Happens**:
1. Class is created in the database
2. Default channels are created (Announcements, Discussion, Resources)
3. **AUTO-ASSIGNMENT**: All students with matching department are automatically added
4. Students receive notifications about being added to the class

**Response**:
```json
{
  "id": 123,
  "name": "L5 Software Development",
  "type": "CLASS",
  "department": "Software Development",
  "students_assigned": 25,
  "message": "Group created successfully! 25 students auto-assigned from Software Development department."
}
```

---

### Step 2: Teacher Adds Lessons to the Class

**Endpoint**: `POST /teacher/modules`

**Request**:
```json
{
  "group_id": 123,
  "title": "Introduction to Python",
  "description": "Learn Python basics, variables, and data types"
}
```

**What Happens**:
1. Lesson is created as a channel in the class
2. All students in the class receive notifications
3. Lesson appears in the class hub

**Response**:
```json
{
  "id": 456,
  "title": "Introduction to Python",
  "group_id": 123,
  "message": "Lesson created successfully! 25 students notified."
}
```

---

### Step 3: Teacher Uploads Resources

**Endpoint**: `POST /teacher/resources`

Teachers can upload:
- PDFs, Word documents
- Videos, images
- Code files
- Any educational material

Resources are linked to specific classes and all students get notified.

---

## 🔄 Alternative: Admin Assignment

Admins can also assign teachers to existing classes:

**Endpoint**: `POST /admin/assign-teacher`

**Request**:
```json
{
  "teacher_id": 789,
  "group_id": 123,
  "is_class_teacher": false
}
```

This is useful when:
- Multiple teachers teach the same class
- Admin wants to assign a teacher to an existing class
- Co-teaching scenarios

---

## 💡 Key Features

### Auto-Assignment Logic
When a teacher creates a class with a department:
```sql
SELECT * FROM users 
WHERE school_id = teacher.school_id 
  AND role = 'STUDENT' 
  AND selected_trade = class.department
```

All matching students are automatically added to the class.

### Notifications
Students receive instant notifications when:
- ✅ Added to a class
- ✅ New lesson is created
- ✅ New resource is uploaded
- ✅ Teacher posts an announcement

### Permissions
- Teachers can only create classes in their own school
- Teachers can only add lessons to classes they have access to
- Teachers can only upload resources to their classes

---

## 🎨 Frontend UI

### Teacher Dashboard
- **Create Class** button (for class teachers)
- **Create Group** button (for clubs/discussion groups)
- **Add Lesson/Module** button (when teacher has classes)
- **Upload Resource** button

### Modals
1. **Create Class Modal**
   - Class name input
   - Department dropdown (loaded from school trades)
   - Level selector (L1-L6)

2. **Add Lesson Modal**
   - Class selector (shows teacher's classes)
   - Lesson title input
   - Description textarea

---

## 📊 Database Schema

### Groups Table
```sql
CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    school_id INTEGER,
    name VARCHAR,
    type VARCHAR,  -- 'CLASS', 'CLUB', 'GROUP'
    department VARCHAR,  -- For auto-assignment
    grade INTEGER
);
```

### Channels Table (Lessons)
```sql
CREATE TABLE channels (
    id SERIAL PRIMARY KEY,
    group_id INTEGER,
    name VARCHAR,  -- Lesson title
    type VARCHAR,  -- 'DISCUSSION', 'ANNOUNCEMENTS', 'RESOURCES'
    description TEXT
);
```

### Group Members Table
```sql
CREATE TABLE group_members (
    id SERIAL PRIMARY KEY,
    group_id INTEGER,
    user_id INTEGER
);
```

---

## 🚀 Benefits of This Approach

1. **Teacher Autonomy**: Teachers can create classes without waiting for admin
2. **Auto-Assignment**: Students are automatically added based on department
3. **Scalability**: Works for 165 TVET schools across Rwanda
4. **Flexibility**: Both teacher-created and admin-assigned classes work seamlessly
5. **Real-time Notifications**: Students know immediately when added to classes

---

## 🔧 Technical Implementation

### Backend (FastAPI)
- `/teacher/groups` - Create class with auto-assignment
- `/teacher/modules` - Add lessons to classes
- `/teacher/resources` - Upload resources
- `/teacher/school-info` - Get school trades for dropdown

### Frontend (Vue 3)
- `TeacherDashboard.vue` - Main dashboard with modals
- Auto-loads school trades from `/teacher/school-info`
- Shows Quick Actions only when teacher has classes
- Real-time updates via WebSocket notifications

---

## 📝 Example Scenario

**Teacher: Jean Paul (Software Development Department)**

1. Jean logs in to TSSANYWHERE
2. Clicks "Create Class"
3. Enters: "L5 Software Development"
4. Selects: Department = "Software Development", Level = 5
5. Clicks "Create Class"
6. **Result**: 25 students in Software Development L5 are auto-added
7. Jean clicks "Add Lesson/Module"
8. Selects: "L5 Software Development" class
9. Enters: "Introduction to Python"
10. Clicks "Create Lesson"
11. **Result**: All 25 students receive notification about new lesson

---

## 🎓 Alignment with TSSANYWHERE Vision

This workflow supports:
- ✅ **165 TVET Schools**: Scalable across all schools
- ✅ **Continuous Learning**: Teachers can add content anytime
- ✅ **Real-time Communication**: Instant notifications
- ✅ **Department-based**: Respects TVET trade structure
- ✅ **Teacher Empowerment**: Teachers control their classes

---

**TSSANYWHERE - Where Technical Education Never Stops** 🚀
