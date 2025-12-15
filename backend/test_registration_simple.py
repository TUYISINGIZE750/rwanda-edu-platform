#!/usr/bin/env python3
"""
COMPREHENSIVE TEST FOR CASCADING REGISTRATION SYSTEM
Tests all the innovative logic you suggested:
1. Province + District -> Auto-display TVET/TSS schools
2. School Selection -> Auto-display trades in that school  
3. Trade Selection -> Auto-display levels (Level 1-6)
4. Complete validation flow
"""

import requests
import json
import sys
from urllib.parse import quote

BASE_URL = "http://127.0.0.1:8080/api/v1"

def test_endpoint(url, description):
    """Test an endpoint and return the response"""
    print(f"\nTesting: {description}")
    print(f"URL: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response preview: {str(data)[:200]}...")
            return data
        else:
            print(f"Error: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Connection Error: {e}")
        return None

def main():
    print("TESTING CASCADING REGISTRATION SYSTEM")
    print("=" * 60)
    
    # Test 1: Get all provinces
    print("\nSTEP 1: Testing Province Endpoint")
    provinces_data = test_endpoint(f"{BASE_URL}/locations/provinces", "Get all provinces")
    
    if not provinces_data:
        print("Cannot proceed - provinces endpoint failed")
        return
    
    # Test 2: Get districts for Southern Province
    print("\nSTEP 2: Testing District Cascade")
    province = "Southern Province"
    districts_data = test_endpoint(
        f"{BASE_URL}/locations/districts/{quote(province)}", 
        f"Get districts for {province}"
    )
    
    if not districts_data:
        print("Cannot proceed - districts endpoint failed")
        return
    
    # Test 3: Get sectors for Kamonyi district
    print("\nSTEP 3: Testing Sector Cascade")
    district = "Kamonyi"
    sectors_data = test_endpoint(
        f"{BASE_URL}/locations/sectors/{quote(province)}/{quote(district)}", 
        f"Get sectors for {district}, {province}"
    )
    
    # Test 4: INNOVATIVE CASCADING - Get schools by location
    print("\nSTEP 4: CASCADING SCHOOLS (Your Innovation)")
    schools_data = test_endpoint(
        f"{BASE_URL}/registration/schools/{quote(province)}/{quote(district)}", 
        f"Auto-display TVET/TSS schools in {district}, {province}"
    )
    
    if not schools_data or not schools_data.get('success'):
        print("Cannot proceed - no schools found")
        return
    
    schools = schools_data.get('schools', [])
    if not schools:
        print("No schools available for testing")
        return
    
    # Test 5: INNOVATIVE CASCADING - Get trades by school
    print("\nSTEP 5: CASCADING TRADES (Your Innovation)")
    test_school = schools[0]  # Use first school
    school_id = test_school['id']
    school_name = test_school['name']
    
    trades_data = test_endpoint(
        f"{BASE_URL}/registration/trades/{school_id}", 
        f"Auto-display trades for {school_name}"
    )
    
    if not trades_data or not trades_data.get('success'):
        print("Cannot proceed - no trades found")
        return
    
    trades = trades_data.get('trades', [])
    if not trades:
        print("No trades available for testing")
        return
    
    # Test 6: INNOVATIVE CASCADING - Get levels
    print("\nSTEP 6: CASCADING LEVELS (Your Innovation)")
    levels_data = test_endpoint(
        f"{BASE_URL}/registration/levels", 
        "Auto-display all TVET levels (Level 1-6)"
    )
    
    # Test 7: Complete flow validation
    print("\nSTEP 7: COMPLETE FLOW VALIDATION")
    test_trade = trades[0]['name']
    
    complete_flow_data = test_endpoint(
        f"{BASE_URL}/registration/complete-flow/{quote(province)}/{quote(district)}/{school_id}/{quote(test_trade)}", 
        f"Validate complete registration flow"
    )
    
    # Test 8: Advanced cascading endpoint
    print("\nSTEP 8: ADVANCED CASCADING API")
    cascade_data = test_endpoint(
        f"{BASE_URL}/registration/cascade?province={quote(province)}&district={quote(district)}&school_id={school_id}&trade={quote(test_trade)}", 
        "Test advanced cascading with all parameters"
    )
    
    # Summary
    print("\n" + "=" * 60)
    print("CASCADING REGISTRATION TEST SUMMARY")
    print("=" * 60)
    
    print(f"Provinces loaded: {len(provinces_data) if provinces_data else 0}")
    print(f"Districts loaded: {len(districts_data) if districts_data else 0}")
    print(f"Sectors loaded: {len(sectors_data) if sectors_data else 0}")
    print(f"Schools found: {schools_data.get('total', 0) if schools_data else 0}")
    print(f"Trades found: {trades_data.get('total', 0) if trades_data else 0}")
    print(f"Levels available: {levels_data.get('total', 0) if levels_data else 0}")
    
    if complete_flow_data and complete_flow_data.get('success'):
        print("Complete flow validation: PASSED")
        print(f"   Location: {province} -> {district}")
        print(f"   School: {school_name}")
        print(f"   Trade: {test_trade}")
        print(f"   Levels: Level 1-6 available")
    else:
        print("Complete flow validation: FAILED")
    
    print("\nCASCADING REGISTRATION SYSTEM TEST COMPLETE!")
    
    # Test the actual registration endpoint
    print("\nTESTING ACTUAL REGISTRATION")
    test_registration_data = {
        "email": "test.student@example.com",
        "password": "testpass123",
        "full_name": "Test Student",
        "role": "STUDENT",
        "school_id": school_id,
        "province": province,
        "district": district,
        "grade": 12,
        "selected_trade": test_trade,
        "selected_level": "Level 1",
        "locale": "rw"
    }
    
    try:
        reg_response = requests.post(
            f"{BASE_URL}/auth/register",
            json=test_registration_data,
            timeout=10
        )
        print(f"Registration Status: {reg_response.status_code}")
        if reg_response.status_code == 200:
            print("Registration successful with cascading data!")
        else:
            print(f"Registration response: {reg_response.text[:200]}")
    except Exception as e:
        print(f"Registration test: {e}")

if __name__ == "__main__":
    main()