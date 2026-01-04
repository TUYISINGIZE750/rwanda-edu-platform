# Privileged Access System for Teachers

## Overview
TSSANYWHERE now implements a **privileged access control system** where teachers must be explicitly granted permission to create classes and groups.

---

## 🔐 Permission Levels

### 1. **Regular Teacher** (Default)
- ❌ Cannot create classes/groups
- ✅ Can be assigned to existing classes by admin
- ✅ Can add lessons to assigned classes
- ✅ Can upload resources to assigned classes
- ✅ Can view students in their department

### 2. **Teacher with Create Permission**
- ✅ Can create classes/groups
- ✅ Can add lessons to their classes
- ✅ Can upload resources
- ✅ All regular teacher permissions

### 3. **Class Teacher**
- ✅ Automatically gets create permission
- ✅ Manages a specific class
- ✅ Full control over their assigned class
- ✅ All teacher permissions

---

## 🎯 How It Works

### Database Schema

New column added to `users` table:
```sql
ALTER TABLE users ADD COLUMN can_create_groups INTEGER DEFAULT 0;
```

- `can_create_groups = 0` → No permission (default)
- `can_create_groups = 1` → Has permission
- `is_class_teacher = 1` → Automatically gets permission

### Backend Logic

**Permission Check** (in `/teacher/groups` endpoint):
```python
if not current_user.is_class_teacher and not current_user.can_create_groups:
    raise HTTPException(
        status_code=403, 
        detail="You don't have permission to create classes/groups. Please contact your administrator."
    )
```

**Dashboard Response** (includes permission status):
```json
{
  "teacher_info": {
    "name": "Jean Paul",
    "email": "jean@school.rw",
    "can_create_groups": true
  }
}
```

---

## 👨‍💼 Admin Controls

### 1. Grant Permission When Creating Teacher

In **Admin Users View** → **Add User**:
- Select Role: Teacher
- ☑️ **Can create classes/groups?** (checkbox)
- ☑️ **Is Class Teacher?** (auto-grants permission)

### 2. Grant/Revoke Permission for Existing Teachers

In **Admin Users View** → **Users Table**:
- Find teacher in list
- Click **🔒 Grant** or **🔓 Revoke** button
- Confirmation dialog appears
- Permission updated instantly

### 3. API Endpoint

**POST** `/admin/grant-permission`
```json
{
  "teacher_id": 123,
  "can_create_groups": true
}
```

**Response**:
```json
{
  "status": "success",
  "message": "Permission granted to Jean Paul",
  "teacher": "Jean Paul",
  "can_create_groups": true
}
```

---

## 🎨 Frontend UI Changes

### Teacher Dashboard

**Before Permission Granted**:
```
┌─────────────────────────────────────┐
│ Welcome back, Jean                  │
│                                     │
│ ⏳ Waiting for permission from     │
│    administrator to create classes  │
│    or group assignment              │
└─────────────────────────────────────┘
```

**After Permission Granted**:
```
┌─────────────────────────────────────┐
│ Welcome back, Jean                  │
│                                     │
│ [Create Class] [Create Group]       │
└─────────────────────────────────────┘
```

### Admin Users View

**Teacher Row Actions**:
```
Edit | 🔒 Grant | Assign | Deactivate
```

After granting:
```
Edit | 🔓 Revoke | Assign | Deactivate
```

---

## 🔄 Migration

**Automatic Migration** on deployment:
```python
# Add column
ALTER TABLE users ADD COLUMN IF NOT EXISTS can_create_groups INTEGER DEFAULT 0

# Auto-grant to existing class teachers
UPDATE users SET can_create_groups = 1 WHERE is_class_teacher = 1
```

---

## 📊 Use Cases

### Use Case 1: New Teacher Joins
1. Admin creates teacher account
2. Admin checks **"Can create classes/groups?"**
3. Teacher logs in → sees Create buttons
4. Teacher creates classes immediately

### Use Case 2: Restrict Teacher
1. Admin creates teacher account
2. Admin leaves permission unchecked
3. Teacher logs in → sees waiting message
4. Admin assigns teacher to existing classes
5. Teacher can only work in assigned classes

### Use Case 3: Promote Teacher
1. Regular teacher working in assigned classes
2. Admin clicks **🔒 Grant** button
3. Teacher refreshes dashboard
4. Teacher now sees Create buttons
5. Teacher can create new classes

### Use Case 4: Class Teacher
1. Admin creates teacher with **"Is Class Teacher"** checked
2. Permission automatically granted
3. Teacher manages their specific class
4. Full control over class content

---

## 🛡️ Security Benefits

1. **Controlled Growth**: Prevents unauthorized class creation
2. **Quality Control**: Only trusted teachers can create classes
3. **Accountability**: Clear audit trail of who created what
4. **Flexibility**: Admin can grant/revoke anytime
5. **Scalability**: Works across 165 TVET schools

---

## 🔧 Technical Implementation

### Backend Files Modified
- `backend/app/models/user.py` - Added `can_create_groups` column
- `backend/app/api/teacher_dashboard.py` - Added permission check
- `backend/app/api/admin.py` - Added grant/revoke endpoint
- `backend/alembic/versions/add_can_create_groups.py` - Migration

### Frontend Files Modified
- `frontend/src/views/TeacherDashboard.vue` - Permission-based UI
- `frontend/src/views/AdminUsersView.vue` - Grant/revoke controls

---

## 📝 API Reference

### Check Permission
```http
GET /teacher/dashboard
```
Response includes `can_create_groups` in `teacher_info`

### Grant Permission
```http
POST /admin/grant-permission
Content-Type: application/json

{
  "teacher_id": 123,
  "can_create_groups": true
}
```

### Create Class (Requires Permission)
```http
POST /teacher/groups
Content-Type: application/json

{
  "name": "L5 Software Development",
  "type": "CLASS",
  "department": "Software Development",
  "grade": 5
}
```

Returns 403 if no permission:
```json
{
  "detail": "You don't have permission to create classes/groups. Please contact your administrator."
}
```

---

## 🎓 Best Practices

### For Administrators
1. Grant permission to experienced teachers first
2. Monitor class creation activity
3. Revoke if misuse detected
4. Use class teacher designation for department heads
5. Assign new teachers to existing classes initially

### For Teachers
1. Request permission from admin if needed
2. Create classes with clear naming (e.g., "L5 Software Dev")
3. Always select department for auto-assignment
4. Add lessons after class creation
5. Upload resources regularly

---

## 🚀 Deployment

1. **Run Migration**:
   ```bash
   alembic upgrade head
   ```

2. **Verify Column**:
   ```sql
   SELECT id, full_name, role, can_create_groups 
   FROM users 
   WHERE role = 'TEACHER';
   ```

3. **Grant to Existing Class Teachers**:
   ```sql
   UPDATE users 
   SET can_create_groups = 1 
   WHERE is_class_teacher = 1;
   ```

4. **Deploy Frontend**:
   - Frontend automatically detects permission from API
   - No additional configuration needed

---

## ✅ Testing Checklist

- [ ] Regular teacher cannot see Create buttons
- [ ] Teacher with permission sees Create buttons
- [ ] Class teacher automatically has permission
- [ ] Admin can grant permission
- [ ] Admin can revoke permission
- [ ] Permission check works on API
- [ ] Error message shows when no permission
- [ ] Migration runs successfully
- [ ] Existing class teachers keep permission

---

**TSSANYWHERE - Secure, Scalable, Student-Focused** 🔐
