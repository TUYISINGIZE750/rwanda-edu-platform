<template>
  <div class="enhanced-registration">
    <!-- Header -->
    <div class="registration-header">
      <h2 class="title">Student/Teacher Registration</h2>
      <p class="subtitle">Select your location to see available schools</p>
    </div>

    <!-- Step 1: Location Selection -->
    <div class="location-section">
      <h3 class="section-title">Step 1: Select Your Location</h3>
      
      <div class="location-inputs">
        <div class="input-group">
          <label class="input-label">Province</label>
          <select v-model="selectedProvince" @change="onProvinceChange" class="select-input">
            <option value="">Choose Province</option>
            <option v-for="province in provinces" :key="province.name" :value="province.name">
              {{ province.name }}
            </option>
          </select>
        </div>

        <div class="input-group">
          <label class="input-label">District</label>
          <select v-model="selectedDistrict" @change="onDistrictChange" class="select-input" :disabled="!selectedProvince">
            <option value="">Choose District</option>
            <option v-for="district in availableDistricts" :key="district.name" :value="district.name">
              {{ district.name }}
            </option>
          </select>
        </div>
      </div>
    </div>

    <!-- Step 2: Schools Auto-Display -->
    <div v-if="schools.length > 0" class="schools-section">
      <h3 class="section-title">
        Step 2: Select Your School
        <span class="count-badge">{{ schools.length }} schools in {{ selectedDistrict }}</span>
      </h3>
      
      <div class="schools-grid">
        <div v-for="school in schools" :key="school.id" 
             :class="['school-card', { 'selected': selectedSchool?.id === school.id }]"
             @click="selectSchool(school)">
          <div class="school-header">
            <h4 class="school-name">{{ school.name }}</h4>
            <span class="school-type">{{ school.type }}</span>
          </div>
          <div class="school-info">
            <span class="school-category">{{ school.category }}</span>
            <span class="trades-count">{{ school.trades_count }} trades available</span>
          </div>
          <div v-if="school.trades.length > 0" class="trades-preview">
            <strong>Trades:</strong> {{ school.trades.slice(0, 3).join(', ') }}
            <span v-if="school.trades.length > 3">... (+{{ school.trades.length - 3 }} more)</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Step 3: Trades Auto-Display -->
    <div v-if="selectedSchool && trades.length > 0" class="trades-section">
      <h3 class="section-title">
        Step 3: Select Your Trade
        <span class="count-badge">{{ trades.length }} trades in {{ selectedSchool.name }}</span>
      </h3>
      
      <div class="trades-grid">
        <div v-for="trade in trades" :key="trade.name"
             :class="['trade-card', { 'selected': selectedTrade === trade.name }]"
             @click="selectTrade(trade.name)">
          <div class="trade-icon">🔧</div>
          <div class="trade-info">
            <h4 class="trade-name">{{ trade.name }}</h4>
            <p class="trade-levels">{{ trade.total_levels }} levels available</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Step 4: Levels Auto-Display -->
    <div v-if="selectedTrade && levels.length > 0" class="levels-section">
      <h3 class="section-title">
        Step 4: Select Your Level
        <span class="count-badge">6 levels available</span>
      </h3>
      
      <div class="levels-grid">
        <div v-for="level in levels" :key="level.name"
             :class="['level-card', { 'selected': selectedLevel === level.name, 'recommended': level.is_default }]"
             @click="selectLevel(level.name)">
          <div class="level-number">{{ level.number }}</div>
          <div class="level-info">
            <h4 class="level-name">{{ level.name }}</h4>
            <p class="level-description">{{ level.description }}</p>
            <span v-if="level.is_default" class="recommended-badge">Recommended</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Registration Summary -->
    <div v-if="isRegistrationComplete" class="registration-summary">
      <h3 class="summary-title">Registration Summary</h3>
      <div class="summary-content">
        <div class="summary-item">
          <span class="label">Location:</span>
          <span class="value">{{ selectedDistrict }}, {{ selectedProvince }}</span>
        </div>
        <div class="summary-item">
          <span class="label">School:</span>
          <span class="value">{{ selectedSchool?.name }} ({{ selectedSchool?.type }})</span>
        </div>
        <div class="summary-item">
          <span class="label">Trade:</span>
          <span class="value">{{ selectedTrade }}</span>
        </div>
        <div class="summary-item">
          <span class="label">Level:</span>
          <span class="value">{{ selectedLevel }}</span>
        </div>
      </div>
      
      <button @click="completeRegistration" class="complete-btn" :disabled="loading">
        <span v-if="!loading">Complete Registration →</span>
        <span v-else>Processing...</span>
      </button>
    </div>

    <!-- Loading States -->
    <div v-if="loadingSchools" class="loading-state">
      <div class="spinner"></div>
      <p>Loading schools in {{ selectedDistrict }}...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const emit = defineEmits(['registration-complete'])

// Data
const loading = ref(false)
const loadingSchools = ref(false)

// Location data
const provinces = ref([])
const availableDistricts = ref([])
const selectedProvince = ref('')
const selectedDistrict = ref('')

// School data
const schools = ref([])
const selectedSchool = ref(null)

// Trade data
const trades = ref([])
const selectedTrade = ref('')

// Level data
const levels = ref([])
const selectedLevel = ref('')

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8080'

// Computed
const isRegistrationComplete = computed(() => {
  return selectedProvince.value && selectedDistrict.value && 
         selectedSchool.value && selectedTrade.value && selectedLevel.value
})

// Methods
onMounted(async () => {
  await loadProvinces()
})

async function loadProvinces() {
  try {
    const response = await axios.get(`${API_URL}/api/v1/locations/provinces`)
    provinces.value = response.data
  } catch (error) {
    console.error('Error loading provinces:', error)
  }
}

async function onProvinceChange() {
  selectedDistrict.value = ''
  schools.value = []
  selectedSchool.value = null
  resetTradeSelection()
  
  if (selectedProvince.value) {
    try {
      const response = await axios.get(`${API_URL}/api/v1/locations/districts/${selectedProvince.value}`)
      availableDistricts.value = response.data
    } catch (error) {
      console.error('Error loading districts:', error)
      availableDistricts.value = []
    }
  } else {
    availableDistricts.value = []
  }
}

async function onDistrictChange() {
  schools.value = []
  selectedSchool.value = null
  resetTradeSelection()
  
  if (selectedProvince.value && selectedDistrict.value) {
    await loadSchoolsInDistrict()
  }
}

async function loadSchoolsInDistrict() {
  loadingSchools.value = true
  
  try {
    // Map province names to match database format
    let apiProvince = selectedProvince.value
    if (apiProvince === 'Southern Province') apiProvince = 'South'
    if (apiProvince === 'Western Province') apiProvince = 'West'
    if (apiProvince === 'Northern Province') apiProvince = 'North'
    if (apiProvince === 'Eastern Province') apiProvince = 'East'
    if (apiProvince === 'Kigali City') apiProvince = 'Kigali city'
    
    const response = await axios.get(
      `${API_URL}/api/v1/schools-by-district/district/${apiProvince}/${selectedDistrict.value}`
    )
    
    schools.value = response.data.schools || []
    console.log(`✅ Loaded ${schools.value.length} schools in ${selectedDistrict.value}`)
  } catch (error) {
    console.error('Error loading schools:', error)
    schools.value = []
  } finally {
    loadingSchools.value = false
  }
}

function selectSchool(school) {
  selectedSchool.value = school
  resetTradeSelection()
  loadTrades(school.id)
}

async function loadTrades(schoolId) {
  try {
    const response = await axios.get(`${API_URL}/api/v1/registration/trades/${schoolId}`)
    
    if (response.data.success) {
      trades.value = response.data.trades
      console.log(`✅ Loaded ${trades.value.length} trades`)
    } else {
      trades.value = []
    }
  } catch (error) {
    console.error('Error loading trades:', error)
    trades.value = []
  }
}

function selectTrade(tradeName) {
  selectedTrade.value = tradeName
  selectedLevel.value = ''
  loadLevels()
}

async function loadLevels() {
  try {
    const response = await axios.get(`${API_URL}/api/v1/registration/levels`)
    
    if (response.data.success) {
      levels.value = response.data.levels
      console.log(`✅ Loaded ${levels.value.length} levels`)
    }
  } catch (error) {
    console.error('Error loading levels:', error)
  }
}

function selectLevel(levelName) {
  selectedLevel.value = levelName
}

function resetTradeSelection() {
  trades.value = []
  selectedTrade.value = ''
  levels.value = []
  selectedLevel.value = ''
}

async function completeRegistration() {
  loading.value = true
  
  const registrationData = {
    province: selectedProvince.value,
    district: selectedDistrict.value,
    school_id: selectedSchool.value.id,
    school_name: selectedSchool.value.name,
    selected_trade: selectedTrade.value,
    selected_level: selectedLevel.value
  }
  
  console.log('🎯 Registration Complete:', registrationData)
  
  emit('registration-complete', registrationData)
  loading.value = false
}
</script>

<style scoped>
.enhanced-registration {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  background: #f8fafc;
  min-height: 100vh;
}

.registration-header {
  text-align: center;
  margin-bottom: 3rem;
}

.title {
  font-size: 2.5rem;
  font-weight: bold;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.subtitle {
  font-size: 1.125rem;
  color: #6b7280;
}

.location-section, .schools-section, .trades-section, .levels-section {
  background: white;
  border-radius: 1rem;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.section-title {
  display: flex;
  align-items: center;
  font-size: 1.5rem;
  font-weight: bold;
  color: #1f2937;
  margin-bottom: 1.5rem;
}

.count-badge {
  background: #dbeafe;
  color: #1d4ed8;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 500;
  margin-left: auto;
}

.location-inputs {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.input-group {
  display: flex;
  flex-direction: column;
}

.input-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.5rem;
}

.select-input {
  padding: 0.75rem;
  border: 2px solid #e5e7eb;
  border-radius: 0.5rem;
  font-size: 1rem;
  transition: all 0.2s ease;
}

.select-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.select-input:disabled {
  background: #f9fafb;
  color: #9ca3af;
}

.schools-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.school-card {
  border: 2px solid #e5e7eb;
  border-radius: 0.75rem;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
  background: white;
}

.school-card:hover {
  border-color: #3b82f6;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
}

.school-card.selected {
  border-color: #10b981;
  background: #f0fdf4;
}

.school-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.school-name {
  font-size: 1.125rem;
  font-weight: bold;
  color: #1f2937;
  flex: 1;
  margin-right: 1rem;
}

.school-type {
  background: #fef3c7;
  color: #92400e;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 500;
  white-space: nowrap;
}

.school-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.school-category {
  color: #6b7280;
  font-size: 0.875rem;
}

.trades-count {
  color: #059669;
  font-size: 0.875rem;
  font-weight: 500;
}

.trades-preview {
  font-size: 0.875rem;
  color: #4b5563;
  line-height: 1.4;
}

.trades-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
}

.trade-card {
  display: flex;
  align-items: center;
  border: 2px solid #e5e7eb;
  border-radius: 0.75rem;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
  background: white;
}

.trade-card:hover {
  border-color: #3b82f6;
}

.trade-card.selected {
  border-color: #10b981;
  background: #f0fdf4;
}

.trade-icon {
  font-size: 2rem;
  margin-right: 1rem;
}

.levels-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
}

.level-card {
  display: flex;
  align-items: center;
  border: 2px solid #e5e7eb;
  border-radius: 0.75rem;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
  background: white;
}

.level-card.recommended {
  border-color: #f59e0b;
  background: #fffbeb;
}

.level-card:hover {
  border-color: #3b82f6;
}

.level-card.selected {
  border-color: #10b981;
  background: #f0fdf4;
}

.level-number {
  width: 3rem;
  height: 3rem;
  border-radius: 50%;
  background: #3b82f6;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  margin-right: 1rem;
  flex-shrink: 0;
}

.recommended-badge {
  background: #fbbf24;
  color: #92400e;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 500;
  margin-top: 0.5rem;
  display: inline-block;
}

.registration-summary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 1rem;
  padding: 2rem;
  margin-top: 2rem;
}

.summary-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 1.5rem;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.summary-item:last-child {
  border-bottom: none;
  margin-bottom: 0;
}

.complete-btn {
  width: 100%;
  background: white;
  color: #667eea;
  padding: 1rem 2rem;
  border-radius: 0.5rem;
  font-weight: bold;
  font-size: 1.125rem;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-top: 1.5rem;
}

.complete-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.complete-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.loading-state {
  text-align: center;
  padding: 2rem;
  background: white;
  border-radius: 1rem;
  margin-top: 1rem;
}

.spinner {
  width: 2rem;
  height: 2rem;
  border: 3px solid #e5e7eb;
  border-top: 3px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .location-inputs {
    grid-template-columns: 1fr;
  }
  
  .schools-grid, .trades-grid, .levels-grid {
    grid-template-columns: 1fr;
  }
}
</style>