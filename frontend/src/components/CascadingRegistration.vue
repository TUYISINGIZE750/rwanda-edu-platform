<template>
  <div class="cascading-registration">
    <!-- Progress Indicator -->
    <div class="progress-steps mb-8">
      <div class="flex items-center justify-between">
        <div v-for="(step, index) in steps" :key="index" 
             :class="['step', { 'active': currentStep >= index, 'completed': currentStep > index }]">
          <div class="step-circle">
            <span v-if="currentStep > index">✓</span>
            <span v-else>{{ index + 1 }}</span>
          </div>
          <span class="step-label">{{ step.label }}</span>
        </div>
      </div>
    </div>



    <!-- Debug Info -->
    <div v-if="selectedProvince && selectedDistrict" class="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-4">
      <p class="text-sm text-blue-800">
        <strong>Debug:</strong> Province: {{ selectedProvince }}, District: {{ selectedDistrict }}, 
        Schools loaded: {{ schools.length }}, Current step: {{ currentStep }}, Loading: {{ loadingSchools }}
      </p>
    </div>

    <!-- Step 1: School Auto-Display -->
    <div v-if="currentStep >= 0 && schools.length > 0" class="step-content animate-slide-up">
      <h3 class="step-title">
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
        </svg>
        TVET/TSS Schools in {{ selectedDistrict }}
        <span class="count-badge">{{ schools.length }} schools found</span>
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
            <span class="trades-count">{{ school.total_trades }} trades</span>
          </div>
          <div class="school-location">📍 {{ school.location }}</div>
        </div>
      </div>
    </div>

    <!-- Step 2: Trades Auto-Display -->
    <div v-if="currentStep >= 1 && trades.length > 0" class="step-content animate-slide-up">
      <h3 class="step-title">
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2-2v2m8 0V6a2 2 0 012 2v6a2 2 0 01-2 2H8a2 2 0 01-2-2V8a2 2 0 012-2V6"/>
        </svg>
        Available Trades in {{ selectedSchool?.name }}
        <span class="count-badge">{{ trades.length }} trades</span>
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

    <!-- Step 3: Levels Auto-Display -->
    <div v-if="currentStep >= 2 && levels.length > 0" class="step-content animate-slide-up">
      <h3 class="step-title">
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
        </svg>
        Select Level for {{ selectedTrade }}
        <span class="count-badge">6 levels (Default: Level 1-6)</span>
      </h3>
      
      <div class="levels-grid">
        <div v-for="level in levels" :key="level.name"
             :class="['level-card', { 'selected': selectedLevel === level.name, 'default': level.is_default }]"
             @click="selectLevel(level.name)">
          <div class="level-number">{{ level.number }}</div>
          <div class="level-info">
            <h4 class="level-name">{{ level.name }}</h4>
            <p class="level-description">{{ level.description }}</p>
            <span v-if="level.is_default" class="default-badge">Recommended</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Registration Summary -->
    <div v-if="currentStep >= 3" class="registration-summary animate-fade-in">
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
      <p>Loading TVET/TSS schools in {{ selectedDistrict }}...</p>
    </div>

    <div v-if="loadingTrades" class="loading-state">
      <div class="spinner"></div>
      <p>Loading trades for {{ selectedSchool?.name }}...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import axios from 'axios'

const props = defineProps({
  province: String,
  district: String
})

const emit = defineEmits(['registration-complete'])

// Data
const currentStep = ref(0)
const loading = ref(false)
const loadingSchools = ref(false)
const loadingTrades = ref(false)

// Location data (from parent)
const selectedProvince = ref(props.province || '')
const selectedDistrict = ref(props.district || '')

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

const steps = [
  { label: 'School', icon: '🏫' },
  { label: 'Trade', icon: '🔧' },
  { label: 'Level', icon: '⚡' },
  { label: 'Complete', icon: '✅' }
]

// Methods
onMounted(async () => {
  // Auto-load schools when component mounts with province and district
  if (props.province && props.district) {
    selectedProvince.value = props.province
    selectedDistrict.value = props.district
    currentStep.value = 0
    await loadSchools()
  }
})

// Watch for prop changes
watch(() => [props.province, props.district], async ([newProvince, newDistrict]) => {
  if (newProvince && newDistrict) {
    selectedProvince.value = newProvince
    selectedDistrict.value = newDistrict
    resetSchoolSelection()
    currentStep.value = 0
    await loadSchools()
  }
})

async function loadSchools() {
  loadingSchools.value = true
  console.log('🔍 Loading schools for:', selectedProvince.value, selectedDistrict.value)
  console.log('🔍 API URL:', `${API_URL}/api/v1/registration/schools/${selectedProvince.value}/${selectedDistrict.value}`)
  
  try {
    const response = await axios.get(
      `${API_URL}/api/v1/registration/schools/${selectedProvince.value}/${selectedDistrict.value}`
    )
    
    console.log('📦 API Response:', response.data)
    
    if (response.data.success) {
      schools.value = response.data.schools
      console.log(`✅ Auto-displayed ${schools.value.length} TVET/TSS schools`, schools.value)
      console.log('📊 Current step:', currentStep.value)
    } else {
      schools.value = []
      console.log('❌ No schools found in this district')
    }
  } catch (error) {
    console.error('❌ Error loading schools:', error)
    console.error('Error details:', error.response?.data)
    schools.value = []
  } finally {
    loadingSchools.value = false
  }
}

function selectSchool(school) {
  selectedSchool.value = school
  currentStep.value = 1
  loadTrades(school.id)
}

async function loadTrades(schoolId) {
  loadingTrades.value = true
  try {
    const response = await axios.get(`${API_URL}/api/v1/registration/trades/${schoolId}`)
    
    if (response.data.success) {
      trades.value = response.data.trades
      console.log(`✅ Auto-displayed ${trades.value.length} trades`)
    } else {
      trades.value = []
    }
  } catch (error) {
    console.error('Error loading trades:', error)
    trades.value = []
  } finally {
    loadingTrades.value = false
  }
}

function selectTrade(tradeName) {
  selectedTrade.value = tradeName
  currentStep.value = 2
  loadLevels()
}

async function loadLevels() {
  try {
    const response = await axios.get(`${API_URL}/api/v1/registration/levels`)
    
    if (response.data.success) {
      levels.value = response.data.levels
      console.log(`✅ Auto-displayed ${levels.value.length} levels (Level 1-6)`)
    }
  } catch (error) {
    console.error('Error loading levels:', error)
  }
}

function selectLevel(levelName) {
  selectedLevel.value = levelName
  currentStep.value = 3
}

function resetSchoolSelection() {
  schools.value = []
  selectedSchool.value = null
  trades.value = []
  selectedTrade.value = ''
  levels.value = []
  selectedLevel.value = ''
  currentStep.value = 0
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
  
  console.log('🎯 Complete Registration Flow:', registrationData)
  
  emit('registration-complete', registrationData)
  loading.value = false
}
</script>

<style scoped>
.cascading-registration {
  max-width: 4xl;
  margin: 0 auto;
  padding: 2rem;
}

.progress-steps {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
}

.step-circle {
  width: 3rem;
  height: 3rem;
  border-radius: 50%;
  background: #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  transition: all 0.3s ease;
}

.step.active .step-circle {
  background: #3b82f6;
  color: white;
}

.step.completed .step-circle {
  background: #10b981;
  color: white;
}

.step-label {
  margin-top: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: #6b7280;
}

.step.active .step-label {
  color: #3b82f6;
}

.step-content {
  background: white;
  border-radius: 1rem;
  padding: 2rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.step-title {
  display: flex;
  align-items: center;
  font-size: 1.25rem;
  font-weight: bold;
  color: #1f2937;
  margin-bottom: 1.5rem;
}

.count-badge {
  background: #dbeafe;
  color: #1d4ed8;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
  margin-left: auto;
}

.input-label {
  display: block;
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.5rem;
}

.select-input {
  width: 100%;
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

.schools-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
}

.school-card {
  border: 2px solid #e5e7eb;
  border-radius: 0.75rem;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.school-card:hover {
  border-color: #3b82f6;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
}

.school-card.selected {
  border-color: #10b981;
  background: #f0fdf4;
}

.school-name {
  font-size: 1.125rem;
  font-weight: bold;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.school-type {
  background: #fef3c7;
  color: #92400e;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 500;
}

.trades-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
}

.trade-card {
  display: flex;
  align-items: center;
  border: 2px solid #e5e7eb;
  border-radius: 0.75rem;
  padding: 1rem;
  cursor: pointer;
  transition: all 0.2s ease;
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
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
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
}

.level-card.default {
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
}

.default-badge {
  background: #fbbf24;
  color: #92400e;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 500;
}

.registration-summary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 1rem;
  padding: 2rem;
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

.loading-state {
  text-align: center;
  padding: 2rem;
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

@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slide-up {
  from { 
    opacity: 0;
    transform: translateY(20px);
  }
  to { 
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in {
  animation: fade-in 0.5s ease-out;
}

.animate-slide-up {
  animation: slide-up 0.5s ease-out;
}
</style>