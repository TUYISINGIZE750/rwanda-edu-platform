# TVET Student Registration Flow - Complete Guide

## 🎯 Registration Flow Logic

### Step-by-Step Process:

1. **Student selects Province & District** → System auto-displays TVET/TSS schools
2. **Student selects School** → System auto-displays trades for that school
3. **Student selects Trade** → System auto-displays levels (Level 1-6)
4. **Student selects Level** → Complete registration

---

## 📡 API Endpoints

### Option 1: Single Endpoint (Recommended - Cascading Data)

```http
GET /api/v1/registration/data?province={province}&district={district}&school_id={id}&trade={trade}
```

**Progressive Loading:**

#### Step 1: Get Schools
```http
GET /api/v1/registration/data?province=Umujyi wa Kigali&district=Gasabo
```
Response:
```json
{
  "schools": [
    {
      "id": 1,
      "name": "IPRC Kigali",
      "type": "TVET",
      "category": "Public",
      "trades": ["Construction", "ICT", "Hospitality"]
    }
  ],
  "trades": null,
  "levels": null
}
```

#### Step 2: Get Schools + Trades
```http
GET /api/v1/registration/data?province=Umujyi wa Kigali&district=Gasabo&school_id=1
```
Response:
```json
{
  "schools": [...],
  "trades": ["Construction", "ICT", "Hospitality"],
  "levels": null
}
```

#### Step 3: Get Schools + Trades + Levels
```http
GET /api/v1/registration/data?province=Umujyi wa Kigali&district=Gasabo&school_id=1&trade=ICT
```
Response:
```json
{
  "schools": [...],
  "trades": ["Construction", "ICT", "Hospitality"],
  "levels": ["Level 1", "Level 2", "Level 3", "Level 4", "Level 5", "Level 6"]
}
```

---

### Option 2: Separate Endpoints

#### Get Schools by District
```http
GET /api/v1/registration/schools/{province}/{district}
```

#### Get Trades by School
```http
GET /api/v1/registration/trades/{school_id}
```

#### Get All Levels
```http
GET /api/v1/registration/levels
```

---

## 💻 Frontend Implementation

### React/Vue/Angular Example:

```javascript
// State Management
const [province, setProvince] = useState('');
const [district, setDistrict] = useState('');
const [schools, setSchools] = useState([]);
const [selectedSchool, setSelectedSchool] = useState(null);
const [trades, setTrades] = useState([]);
const [selectedTrade, setSelectedTrade] = useState('');
const [levels, setLevels] = useState([]);
const [selectedLevel, setSelectedLevel] = useState('');

// Step 1: When province & district selected
const handleLocationChange = async (prov, dist) => {
  setProvince(prov);
  setDistrict(dist);
  
  // Auto-fetch schools
  const response = await fetch(
    `/api/v1/registration/schools/${prov}/${dist}`
  );
  const data = await response.json();
  setSchools(data.schools);
  
  // Reset downstream selections
  setSelectedSchool(null);
  setTrades([]);
  setSelectedTrade('');
  setLevels([]);
  setSelectedLevel('');
};

// Step 2: When school selected
const handleSchoolChange = async (schoolId) => {
  const school = schools.find(s => s.id === schoolId);
  setSelectedSchool(school);
  
  // Auto-display trades
  setTrades(school.trades);
  
  // Reset downstream selections
  setSelectedTrade('');
  setLevels([]);
  setSelectedLevel('');
};

// Step 3: When trade selected
const handleTradeChange = async (trade) => {
  setSelectedTrade(trade);
  
  // Auto-display levels
  const response = await fetch('/api/v1/registration/levels');
  const data = await response.json();
  setLevels(data.levels);
  
  // Reset level selection
  setSelectedLevel('');
};

// Step 4: Submit registration
const handleSubmit = async () => {
  const registrationData = {
    email: email,
    password: password,
    full_name: fullName,
    role: "student",
    school_id: selectedSchool.id,
    province: province,
    district: district,
    selected_trade: selectedTrade,
    selected_level: selectedLevel,
    locale: "rw"
  };
  
  await fetch('/api/v1/auth/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(registrationData)
  });
};
```

---

## 🎨 HTML Form Example

```html
<form id="registrationForm">
  <!-- Step 1: Location Selection -->
  <div class="form-group">
    <label>Province</label>
    <select id="province" onchange="loadDistricts()" required>
      <option value="">Select Province</option>
      <option value="Umujyi wa Kigali">Kigali City</option>
      <option value="Amajyepfo">Southern Province</option>
      <!-- ... -->
    </select>
  </div>

  <div class="form-group">
    <label>District</label>
    <select id="district" onchange="loadSchools()" required>
      <option value="">Select District</option>
    </select>
  </div>

  <!-- Step 2: School Selection (Auto-populated) -->
  <div class="form-group" id="schoolGroup" style="display:none;">
    <label>TVET/TSS School</label>
    <select id="school" onchange="loadTrades()" required>
      <option value="">Select School</option>
    </select>
  </div>

  <!-- Step 3: Trade Selection (Auto-populated) -->
  <div class="form-group" id="tradeGroup" style="display:none;">
    <label>Trade/Program</label>
    <select id="trade" onchange="loadLevels()" required>
      <option value="">Select Trade</option>
    </select>
  </div>

  <!-- Step 4: Level Selection (Auto-populated) -->
  <div class="form-group" id="levelGroup" style="display:none;">
    <label>Level</label>
    <select id="level" required>
      <option value="">Select Level</option>
    </select>
  </div>

  <!-- Other fields -->
  <div class="form-group">
    <label>Full Name</label>
    <input type="text" id="fullName" required>
  </div>

  <div class="form-group">
    <label>Email</label>
    <input type="email" id="email" required>
  </div>

  <div class="form-group">
    <label>Password</label>
    <input type="password" id="password" required>
  </div>

  <button type="submit">Register</button>
</form>

<script>
// Load schools when district selected
async function loadSchools() {
  const province = document.getElementById('province').value;
  const district = document.getElementById('district').value;
  
  if (!province || !district) return;
  
  const response = await fetch(
    `/api/v1/registration/schools/${province}/${district}`
  );
  const data = await response.json();
  
  const schoolSelect = document.getElementById('school');
  schoolSelect.innerHTML = '<option value="">Select School</option>';
  
  data.schools.forEach(school => {
    const option = document.createElement('option');
    option.value = school.id;
    option.textContent = `${school.name} (${school.type})`;
    option.dataset.trades = JSON.stringify(school.trades);
    schoolSelect.appendChild(option);
  });
  
  document.getElementById('schoolGroup').style.display = 'block';
  document.getElementById('tradeGroup').style.display = 'none';
  document.getElementById('levelGroup').style.display = 'none';
}

// Load trades when school selected
function loadTrades() {
  const schoolSelect = document.getElementById('school');
  const selectedOption = schoolSelect.options[schoolSelect.selectedIndex];
  
  if (!selectedOption.value) return;
  
  const trades = JSON.parse(selectedOption.dataset.trades || '[]');
  
  const tradeSelect = document.getElementById('trade');
  tradeSelect.innerHTML = '<option value="">Select Trade</option>';
  
  trades.forEach(trade => {
    const option = document.createElement('option');
    option.value = trade;
    option.textContent = trade;
    tradeSelect.appendChild(option);
  });
  
  document.getElementById('tradeGroup').style.display = 'block';
  document.getElementById('levelGroup').style.display = 'none';
}

// Load levels when trade selected
async function loadLevels() {
  const trade = document.getElementById('trade').value;
  
  if (!trade) return;
  
  const response = await fetch('/api/v1/registration/levels');
  const data = await response.json();
  
  const levelSelect = document.getElementById('level');
  levelSelect.innerHTML = '<option value="">Select Level</option>';
  
  data.levels.forEach(level => {
    const option = document.createElement('option');
    option.value = level;
    option.textContent = level;
    levelSelect.appendChild(option);
  });
  
  document.getElementById('levelGroup').style.display = 'block';
}

// Submit registration
document.getElementById('registrationForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const formData = {
    email: document.getElementById('email').value,
    password: document.getElementById('password').value,
    full_name: document.getElementById('fullName').value,
    role: "student",
    school_id: parseInt(document.getElementById('school').value),
    province: document.getElementById('province').value,
    district: document.getElementById('district').value,
    selected_trade: document.getElementById('trade').value,
    selected_level: document.getElementById('level').value,
    locale: "rw"
  };
  
  const response = await fetch('/api/v1/auth/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(formData)
  });
  
  if (response.ok) {
    alert('Registration successful!');
  } else {
    const error = await response.json();
    alert('Error: ' + error.detail);
  }
});
</script>
```

---

## ✅ Complete Registration Request

```json
POST /api/v1/auth/register

{
  "email": "student@example.com",
  "password": "securePassword123",
  "full_name": "Jean Claude Mugabo",
  "role": "student",
  "school_id": 1,
  "province": "Umujyi wa Kigali",
  "district": "Gasabo",
  "selected_trade": "ICT",
  "selected_level": "Level 3",
  "locale": "rw"
}
```

---

## 🔄 Auto-Display Flow Summary

```
User Action                    → System Response
─────────────────────────────────────────────────────────
Select Province + District     → Auto-display TVET/TSS Schools
Select School                  → Auto-display Trades for that school
Select Trade                   → Auto-display Levels (1-6)
Select Level + Submit          → Complete Registration
```

---

## 📊 Database Schema

```sql
-- Users table includes:
- selected_trade (VARCHAR)
- selected_level (VARCHAR)

-- Schools table includes:
- trades (JSON array)
```

---

## 🚀 Quick Test

```bash
# 1. Get schools
curl "http://localhost:8000/api/v1/registration/schools/Umujyi%20wa%20Kigali/Gasabo"

# 2. Get trades for school ID 1
curl "http://localhost:8000/api/v1/registration/trades/1"

# 3. Get levels
curl "http://localhost:8000/api/v1/registration/levels"

# 4. Register
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "full_name": "Test Student",
    "role": "student",
    "school_id": 1,
    "province": "Umujyi wa Kigali",
    "district": "Gasabo",
    "selected_trade": "ICT",
    "selected_level": "Level 1",
    "locale": "rw"
  }'
```
