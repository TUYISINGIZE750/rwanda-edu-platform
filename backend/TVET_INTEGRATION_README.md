# TVET Schools and Trades Integration

## Overview
This integration adds support for TVET (Technical and Vocational Education and Training) schools and their available trades during student/teacher registration.

## Changes Made

### 1. Database Models Updated

#### School Model (`app/models/school.py`)
- Added `trades` field (JSON) to store list of available trades/programs

#### User Model (`app/models/user.py`)
- Added `selected_trade` field (String) to store student's chosen trade

### 2. API Schemas Updated

#### User Schema (`app/schemas/user.py`)
- Added `selected_trade: Optional[str]` to UserBase

#### Location API (`app/api/locations.py`)
- Updated SchoolResponse to include `trades: List[str]`

### 3. Registration Flow

#### Auth API (`app/api/auth.py`)
- Registration now accepts `selected_trade` parameter
- Students can specify their chosen trade during registration

### 4. Database Migration

#### Migration File (`alembic/versions/add_trades_fields.py`)
- Adds `trades` column to schools table
- Adds `selected_trade` column to users table

### 5. Excel Parser

#### Parse Script (`parse_tvet_excel.py`)
- Parses the official TVET schools Excel file
- Extracts school information and available trades
- Outputs to JSON format for easy import

## Usage

### 1. Run Database Migration
```bash
cd backend
alembic upgrade head
```

### 2. Parse Excel File (Optional)
```bash
python parse_tvet_excel.py
```
This will create `official_tvet_schools.json` with parsed data.

### 3. Seed TVET Schools
```bash
python seed_tvet_schools.py
```

### 4. API Endpoints

#### Get Schools by District
```
GET /locations/schools/district/{province_name}/{district_name}
```
Returns all TVET/TSS schools in a district with their available trades.

#### Get All Schools
```
GET /locations/schools
```
Returns all TVET/TSS schools.

#### Register Student with Trade
```
POST /auth/register
{
  "email": "student@example.com",
  "password": "password123",
  "full_name": "John Doe",
  "role": "student",
  "school_id": 1,
  "province": "Umujyi wa Kigali",
  "district": "Gasabo",
  "grade": 10,
  "selected_trade": "ICT",
  "locale": "rw"
}
```

## Registration Flow for Students

1. **Select Location**: Student selects Province → District
2. **Select School**: System shows TVET/TSS schools in selected district
3. **View Available Trades**: System displays trades offered by selected school
4. **Select Trade**: Student chooses their desired trade
5. **Complete Registration**: Student fills remaining details and submits

## Frontend Integration

### Example Flow:

```javascript
// 1. Get schools by district
const schools = await fetch(`/api/locations/schools/district/${province}/${district}`);

// 2. Display schools with their trades
schools.forEach(school => {
  console.log(school.name);
  console.log('Available trades:', school.trades);
});

// 3. Register with selected trade
await fetch('/api/auth/register', {
  method: 'POST',
  body: JSON.stringify({
    ...userData,
    school_id: selectedSchool.id,
    selected_trade: selectedTrade
  })
});
```

## Data Structure

### School Object
```json
{
  "id": 1,
  "name": "IPRC Kigali",
  "type": "TVET",
  "category": "Public",
  "province": "Umujyi wa Kigali",
  "district": "Gasabo",
  "trades": [
    "Construction",
    "Electrical Installation",
    "Plumbing",
    "Automotive",
    "ICT",
    "Hospitality"
  ]
}
```

### User Object (with trade)
```json
{
  "id": 1,
  "email": "student@example.com",
  "full_name": "John Doe",
  "role": "student",
  "school_id": 1,
  "province": "Umujyi wa Kigali",
  "district": "Gasabo",
  "grade": 10,
  "selected_trade": "ICT",
  "locale": "rw"
}
```

## Notes

- The `selected_trade` field is optional and primarily for TVET students
- Teachers don't need to select a trade
- The trades list is stored as JSON array in the database
- Schools can have multiple trades available
- Students can only select one trade during registration
