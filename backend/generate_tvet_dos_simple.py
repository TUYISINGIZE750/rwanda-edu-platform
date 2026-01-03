#!/usr/bin/env python3
"""
TVET DOS Credentials Generator (Simplified)
Creates a comprehensive PDF with DOS credentials for all TVET schools
Based on the existing excel_data.json file
"""

import json
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.units import inch
from datetime import datetime
import os
import re

def load_tvet_schools():
    """Load TVET schools data from JSON file"""
    try:
        if os.path.exists('excel_data.json'):
            with open('excel_data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"Loaded {len(data)} records from excel_data.json")
            return data
        else:
            print("excel_data.json not found!")
            return []
    except Exception as e:
        print(f"Error loading data: {e}")
        return []

def clean_text(text):
    """Clean text for use in emails and usernames"""
    if not text:
        return ""
    # Remove special characters and spaces, keep only alphanumeric
    cleaned = re.sub(r'[^a-zA-Z0-9]', '', text.lower())
    return cleaned

def process_schools_data(raw_data):
    """Process raw Excel data into structured school information"""
    schools = {}
    
    for row in raw_data:
        # Skip header row
        if row.get('Unnamed: 0') == 'Province':
            continue
            
        # Extract school information
        province = str(row.get('Unnamed: 0', '')).strip()
        district = str(row.get('LIST OF TVET BOARDING SCHOOLS TO BE CHOSEN BY S3 CANDIDATES, 2022', '')).strip()
        school_code = str(row.get('Unnamed: 2', '')).strip()
        school_name = str(row.get('Unnamed: 3', '')).strip()
        trade_full = str(row.get('Unnamed: 4', '')).strip()
        trade_code = str(row.get('Unnamed: 5', '')).strip()
        gender = str(row.get('Unnamed: 6', '')).strip()
        
        # Skip empty rows
        if not school_name or not school_code or school_code == 'nan':
            continue
            
        # Create unique school identifier
        school_key = f"{school_code}_{school_name}"
        
        if school_key not in schools:
            schools[school_key] = {
                'province': province,
                'district': district,
                'school_code': school_code,
                'school_name': school_name,
                'trades': [],
                'gender': gender
            }
        
        # Add trade information
        if trade_full and trade_code and trade_full != 'nan' and trade_code != 'nan':
            schools[school_key]['trades'].append({
                'trade_full': trade_full,
                'trade_code': trade_code
            })
    
    return list(schools.values())

def generate_dos_credentials(school):
    """Generate DOS credentials for a school"""
    # Clean school name for email
    clean_name = clean_text(school['school_name'])
    if len(clean_name) > 15:
        clean_name = clean_name[:15]
    
    # Generate email
    district_clean = clean_text(school['district'])
    if len(district_clean) > 10:
        district_clean = district_clean[:10]
    
    email = f"dos.{clean_name}@{district_clean}.tvet.rw"
    
    # Generate username
    username = f"dos_{school['school_code']}"
    
    # Default password
    password = "dos123"
    
    # Full name
    full_name = f"DOS - {school['school_name']}"
    
    return {
        'username': username,
        'email': email,
        'password': password,
        'full_name': full_name,
        'school_code': school['school_code'],
        'school_name': school['school_name'],
        'district': school['district'],
        'province': school['province'],
        'trades_count': len(school['trades']),
        'trades': ', '.join([t['trade_code'] for t in school['trades'][:3]]) + ('...' if len(school['trades']) > 3 else '')
    }

def create_dos_credentials_pdf():
    """Create comprehensive DOS credentials PDF"""
    
    # Load and process data
    print("Loading TVET schools data...")
    raw_data = load_tvet_schools()
    if not raw_data:
        print("No data available!")
        return
    
    schools = process_schools_data(raw_data)
    print(f"Processed {len(schools)} unique schools")
    
    if not schools:
        print("No valid schools found!")
        return
    
    # Generate credentials for all schools
    credentials = []
    for school in schools:
        cred = generate_dos_credentials(school)
        credentials.append(cred)
    
    # Sort by province, then district, then school name
    credentials.sort(key=lambda x: (x['province'], x['district'], x['school_name']))
    
    # Create PDF
    pdf_file = "TVET_DOS_CREDENTIALS_ALL_SCHOOLS.pdf"
    doc = SimpleDocTemplate(pdf_file, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=12,
        alignment=1
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#374151'),
        spaceAfter=8,
        alignment=1
    )
    
    # Title page
    elements.append(Paragraph("TVET SCHOOLS - DOS CREDENTIALS", title_style))
    elements.append(Paragraph("Directory of Studies Administrator Accounts", subtitle_style))
    elements.append(Paragraph(f"All TVET Boarding Schools - S3 Candidates 2022", styles['Normal']))
    elements.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    elements.append(Paragraph(f"Total Schools: {len(credentials)}", styles['Normal']))
    elements.append(Spacer(1, 0.5*inch))
    
    # Summary by province
    province_summary = {}
    for cred in credentials:
        province = cred['province']
        if province not in province_summary:
            province_summary[province] = 0
        province_summary[province] += 1
    
    elements.append(Paragraph("Schools by Province:", styles['Heading2']))
    for province, count in sorted(province_summary.items()):
        if province and province != 'nan':
            elements.append(Paragraph(f"• {province}: {count} schools", styles['Normal']))
    
    elements.append(PageBreak())
    
    # Main credentials table
    elements.append(Paragraph("DOS Credentials - All Schools", styles['Heading1']))
    elements.append(Spacer(1, 0.2*inch))
    
    # Table headers
    data = [['#', 'School Name', 'Code', 'District', 'Username', 'Email', 'Password', 'Trades']]
    
    # Add credentials data
    for idx, cred in enumerate(credentials, 1):
        school_name_display = cred['school_name'][:25] + ('...' if len(cred['school_name']) > 25 else '')
        district_display = cred['district'][:12] + ('...' if len(cred['district']) > 12 else '')
        email_display = cred['email'][:35] + ('...' if len(cred['email']) > 35 else '')
        
        data.append([
            str(idx),
            school_name_display,
            cred['school_code'],
            district_display,
            cred['username'],
            email_display,
            cred['password'],
            cred['trades'][:15] + ('...' if len(cred['trades']) > 15 else '')
        ])
    
    # Create table with appropriate column widths
    table = Table(data, colWidths=[0.3*inch, 1.8*inch, 0.6*inch, 0.8*inch, 0.8*inch, 2.2*inch, 0.6*inch, 0.8*inch])
    
    # Table styling
    table.setStyle(TableStyle([
        # Header styling
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('FONTSIZE', (0, 1), (-1, -1), 6),
        
        # Cell padding
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 2),
        ('RIGHTPADDING', (0, 0), (-1, -1), 2),
        
        # Grid and alternating colors
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')])
    ]))
    
    elements.append(table)
    
    # Footer information
    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph("<b>Login Information:</b>", styles['Heading2']))
    elements.append(Paragraph("• <b>Login URL:</b> https://tssanywhere.pages.dev/login", styles['Normal']))
    elements.append(Paragraph("• <b>Default Password:</b> dos123 (for all DOS accounts)", styles['Normal']))
    elements.append(Paragraph("• <b>Role:</b> Administrator (DOS)", styles['Normal']))
    elements.append(Paragraph("• <b>Access Level:</b> School-level administration", styles['Normal']))
    
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("<b>Notes:</b>", styles['Heading2']))
    elements.append(Paragraph("• Each school has one DOS (Directory of Studies) administrator account", styles['Normal']))
    elements.append(Paragraph("• DOS accounts can manage students, teachers, and school-specific content", styles['Normal']))
    elements.append(Paragraph("• Usernames follow the pattern: dos_[school_code]", styles['Normal']))
    elements.append(Paragraph("• Email addresses follow the pattern: dos.[schoolname]@[district].tvet.rw", styles['Normal']))
    elements.append(Paragraph("• Change default passwords after first login for security", styles['Normal']))
    
    # Build PDF
    try:
        doc.build(elements)
        print(f"PDF created successfully: {pdf_file}")
        print(f"Total schools processed: {len(credentials)}")
        print(f"Schools by province:")
        for province, count in sorted(province_summary.items()):
            if province and province != 'nan':
                print(f"   • {province}: {count} schools")
        
        return pdf_file
        
    except Exception as e:
        print(f"Error creating PDF: {e}")
        return None

def main():
    """Main function"""
    print("TVET DOS Credentials Generator")
    print("=" * 50)
    
    pdf_file = create_dos_credentials_pdf()
    
    if pdf_file:
        print(f"\nSuccess! DOS credentials PDF created: {pdf_file}")
        print("\nNext steps:")
        print("1. Review the generated credentials")
        print("2. Distribute to school administrators")
        print("3. Ensure schools change default passwords")
        print("4. Set up proper access controls")
    else:
        print("\nFailed to create DOS credentials PDF")

if __name__ == "__main__":
    main()