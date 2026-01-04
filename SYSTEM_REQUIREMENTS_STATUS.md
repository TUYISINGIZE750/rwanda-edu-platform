# TSSANYWHERE SYSTEM REQUIREMENTS & IMPLEMENTATION STATUS

## 🎯 SYSTEM OVERVIEW
165 TVET/TSS Schools across Rwanda with automated real-time synchronization

---

## ✅ CURRENT IMPLEMENTATION STATUS

### 1. SCHOOL INFRASTRUCTURE ✅ COMPLETE
- ✅ 185 schools seeded in database with real trades from Ministry Excel
- ✅ School codes as unique identifiers
- ✅ Trades properly stored in PostgreSQL arrays
- ✅ API endpoints for school/trade retrieval working

### 2. DOS/ADMIN ACCOUNTS ✅ COMPLETE
- ✅ 165 DOS accounts created from PDF credentials
- ✅ Each DOS assigned to specific school
- ✅ DOS can login with provided credentials
- ✅ DOS dashboard with school statistics

### 3. STUDENT REGISTRATION ✅ COMPLETE
- ✅ Public registration page (anyone can register)
- ✅ Students specify: Province, District, School during registration
- ✅ Auto-assignment to school_id based on selection
- ✅ Student can login after registration

### 4. TEACHER CREATION BY DOS ✅ COMPLETE
- ✅ DOS can create teacher accounts via Admin Users page
- ✅ DOS provides: email, password, full_name, role=TEACHER
- ✅ Teacher auto-assigned to DOS's school_id
- ✅ DOS can provide credentials to teacher

### 5. TEACHER LOGIN ✅ COMPLETE
- ✅ Teacher logs in with DOS-provided credentials
- ✅ Teacher dashboard loads successfully
- ✅ Teacher sees their school information

### 6. REAL-TIME NOTIFICATIONS ✅ COMPLETE
- ✅ WebSocket-based instant notifications
- ✅ Browser push notifications
- ✅ Auto-reconnect on disconnect
- ✅ Multi-device support

### 7. RWANDA TIMEZONE ✅ COMPLETE
- ✅ All timestamps in CAT (UTC+2)
- ✅ Backend uses Rwanda time
- ✅ Frontend displays Rwanda time

---

## 🔧 MISSING FEATURES (TO IMPLEMENT)

### 1. TEACHER-STUDENT FILTERING BY DEPARTMENT/TRADE ❌ NOT IMPLEMENTED
**Requirement:** Teacher should see ONLY students from their school filtered by department/trade

**Current Issue:** 
- Teacher sees all students from school, not filtered by department
- No automatic department assignment for teachers

**Solution Needed:**
```python
# Add to User model
department = Column(String(100), nullable=True)  # Teacher's department

# Teacher dashboard should filter:
students = db.query(User).filter(
    User.school_id == teacher.school_id,
    User.role == UserRole.STUDENT,
    User.department == teacher.department  # Filter by same department
).all()
```

### 2. TEACHER DEPARTMENT ASSIGNMENT ❌ NOT IMPLEMENTED
**Requirement:** When DOS creates teacher, specify which department/trade they teach

**Current Issue:**
- DOS creates teacher but doesn't assign department
- Teacher has no department field

**Solution Needed:**
- Add "Department" dropdown when DOS creates teacher
- Populate from school's trades list
- Store in teacher.department field

### 3. CLASS TEACHER vs NON-CLASS TEACHER PRIVILEGES ⚠️ PARTIALLY IMPLEMENTED
**Current Status:**
- ✅ is_class_teacher flag exists
- ✅ managed_class_id field exists
- ❌ DOS cannot specify during teacher creation
- ❌ Privileges not fully enforced

**Solution Needed:**
- Add checkbox "Is Class Teacher?" when DOS creates teacher
- If checked, show dropdown to select which class/group to manage
- Enforce privileges:
  - Class Teacher: Can create modules, manage students, full access
  - Non-Class Teacher: Can only view, participate in assigned groups

### 4. STUDENT DEPARTMENT ASSIGNMENT ❌ NOT IMPLEMENTED
**Requirement:** Students should be assigned to department/trade during registration

**Current Issue:**
- Students register but don't select department/trade
- No department field for students

**Solution Needed:**
- Add "Department/Trade" dropdown in registration form
- Populate from selected school's trades
- Store in student.department field

### 5. MODULE CREATION WITH DEPARTMENT FILTERING ⚠️ PARTIALLY IMPLEMENTED
**Current Status:**
- ✅ Teacher can create modules/classes
- ✅ Department field exists in Group model
- ❌ Students not auto-assigned based on department match

**Solution Needed:**
- When teacher creates module with department "Software Development"
- Auto-add all students from same school + same department
- Real-time sync: New students with matching department auto-join

---

## 🚀 IMPLEMENTATION PLAN

### PHASE 1: DATABASE SCHEMA UPDATES
```sql
-- Add department to users table
ALTER TABLE users ADD COLUMN department VARCHAR(100);

-- Update existing students/teachers to have departments
-- (Manual or via migration script)
```

### PHASE 2: DOS TEACHER CREATION ENHANCEMENT
**File:** `frontend/src/views/AdminUsersView.vue`
- Add "Department" dropdown (populated from school trades)
- Add "Is Class Teacher?" checkbox
- If class teacher, show "Managed Class" dropdown

**File:** `backend/app/api/admin.py`
- Update create_user endpoint to accept department
- Update to accept is_class_teacher and managed_class_id

### PHASE 3: STUDENT REGISTRATION ENHANCEMENT
**File:** `frontend/src/views/RegisterView.vue`
- After school selection, load school trades
- Add "Department/Trade" dropdown
- Submit department with registration

**File:** `backend/app/api/registration.py`
- Accept department in registration
- Store in user.department

### PHASE 4: TEACHER DASHBOARD FILTERING
**File:** `backend/app/api/teacher_dashboard.py`
- Filter students by school_id AND department
- Return only students in teacher's department

**File:** `frontend/src/views/TeacherDashboard.vue`
- Display filtered students by department
- Show department-specific statistics

### PHASE 5: AUTO-ASSIGNMENT TO MODULES
**File:** `backend/app/api/modules.py` or `teacher_dashboard.py`
- When teacher creates module with department
- Query all students: same school + same department
- Auto-add as group members
- Send notifications to all added students

### PHASE 6: REAL-TIME SYNC
- When new student registers with department
- Find all modules/classes with matching school + department
- Auto-add student to those modules
- Notify teachers via WebSocket

---

## 📊 CURRENT SYSTEM CAPABILITIES

### ✅ WORKING FEATURES:
1. 165 DOS accounts with school assignments
2. DOS can create teachers
3. Students can self-register
4. Real-time WebSocket notifications
5. Rwanda timezone (CAT/UTC+2)
6. Department dropdown in module creation (22 TVET trades)
7. School-based filtering
8. Teacher can create modules/classes
9. Live chat in modules
10. Resource upload/download

### ❌ MISSING FEATURES:
1. Department assignment during teacher creation
2. Department assignment during student registration
3. Teacher-student filtering by department
4. Auto-assignment to modules based on department
5. Class teacher vs non-class teacher privilege enforcement
6. Real-time student sync to matching modules

---

## 🎯 PRIORITY IMPLEMENTATION ORDER

### HIGH PRIORITY (Critical for system logic):
1. ✅ Add department field to User model
2. ✅ Update DOS teacher creation to include department
3. ✅ Update student registration to include department
4. ✅ Filter teacher dashboard students by department
5. ✅ Auto-assign students to modules based on department match

### MEDIUM PRIORITY (Enhanced functionality):
6. ✅ Class teacher privilege enforcement
7. ✅ Real-time sync when new student joins
8. ✅ Department-based statistics on dashboards

### LOW PRIORITY (Nice to have):
9. Department change functionality
10. Transfer student between departments
11. Department-specific announcements

---

## 📝 NOTES

- All 165 schools already have trades in database
- DOS credentials already exist in system
- WebSocket infrastructure ready for real-time sync
- Need to add department field and implement filtering logic
- System architecture supports all requirements, just needs implementation

---

## 🔗 KEY FILES TO MODIFY

### Backend:
1. `backend/app/models/user.py` - Add department field
2. `backend/app/api/admin.py` - Update teacher creation
3. `backend/app/api/registration.py` - Update student registration
4. `backend/app/api/teacher_dashboard.py` - Add department filtering
5. `backend/app/api/modules.py` - Auto-assignment logic

### Frontend:
1. `frontend/src/views/AdminUsersView.vue` - Teacher creation form
2. `frontend/src/views/RegisterView.vue` - Student registration form
3. `frontend/src/views/TeacherDashboard.vue` - Filtered student display

---

**STATUS:** System is 70% complete. Core infrastructure ready. Need department-based filtering and auto-assignment logic.
