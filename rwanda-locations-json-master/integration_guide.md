# Rwanda Locations Integration Guide

## Files to Add to Your System

### 1. Core Files
- `locations.json` - Complete Rwanda administrative data
- `rwanda_locations.js` - JavaScript module for location handling
- `rwanda_locations.css` - Styling for location dropdowns

### 2. Integration Steps

#### Step 1: Copy Core Files
```bash
# Copy these files to your project:
cp locations.json /path/to/your/project/assets/data/
cp rwanda_locations.js /path/to/your/project/js/
cp rwanda_locations.css /path/to/your/project/css/
```

#### Step 2: Include in HTML
```html
<link rel="stylesheet" href="css/rwanda_locations.css">
<script src="js/rwanda_locations.js"></script>
```

#### Step 3: Add HTML Structure
```html
<div class="rwanda-locations">
    <select id="province" name="province" required>
        <option value="">Select Province</option>
    </select>
    <select id="district" name="district" required disabled>
        <option value="">Select District</option>
    </select>
    <select id="sector" name="sector" required disabled>
        <option value="">Select Sector</option>
    </select>
    <select id="cell" name="cell" required disabled>
        <option value="">Select Cell</option>
    </select>
    <select id="village" name="village" required disabled>
        <option value="">Select Village</option>
    </select>
</div>
```

#### Step 4: Initialize
```javascript
// Initialize Rwanda locations
RwandaLocations.init();
```

## API Usage

### Get Selected Location
```javascript
const location = RwandaLocations.getSelectedLocation();
// Returns: { province, district, sector, cell, village }
```

### Search Locations
```javascript
const results = RwandaLocations.search("Kigali");
// Returns array of matching locations
```

### Validate Location
```javascript
const isValid = RwandaLocations.validate(province, district, sector, cell, village);
// Returns: true/false
```