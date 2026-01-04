# COMPLETE IMPLEMENTATION GUIDE
## Department-Based Filtering & Auto-Assignment System

## DATABASE STATUS
- User.selected_trade: EXISTS ✓
- User.selected_level: EXISTS ✓
- User.is_class_teacher: EXISTS ✓
- User.managed_class_id: EXISTS ✓
- Group.department: EXISTS ✓
- Schools with trades: 185 ✓

## IMPLEMENTATION CHECKLIST

### BACKEND CHANGES

#### 1. admin.py - DOS Creates Teacher with Department
File: `backend/app/api/admin.py`

Add to CreateUserRequest:
```python
selected_trade: Optional[str] = None
is_class_teacher: bool = False
managed_class_id: Optional[int] = None
```

Update create_user function to use these fields.

#### 2. registration.py - Student Selects Department
File: `backend/app/api/registration.py`

Add selected_trade and selected_level to registration.

#### 3. teacher_dashboard.py - Filter Students by Department
File: `backend/app/api/teacher_dashboard.py`

Filter students WHERE selected_trade = teacher.selected_trade

#### 4. modules.py - Auto-Add Students to Matching Modules
File: `backend/app/api/teacher.py` or relevant module creation endpoint

When teacher creates module with department:
- Find all students: same school + same department
- Auto-add to group_members
- Send notifications

### FRONTEND CHANGES

#### 1. AdminUsersView.vue - Add Department Selection
Add:
- Department dropdown (load from school trades)
- "Is Class Teacher?" checkbox
- "Managed Class" dropdown

#### 2. RegisterView.vue - Add Department Selection
Add:
- Department dropdown after school selection
- Level dropdown (L1-L6)

#### 3. TeacherDashboard.vue - Show Filtered Students
Display only students in teacher's department

## PRIORITY: IMPLEMENT NOW
1. Update admin.py create_user
2. Update registration.py
3. Update teacher_dashboard filtering
4. Update frontend forms
5. Test complete flow
