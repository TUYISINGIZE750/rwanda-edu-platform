"""Generate DOS admin accounts for all TVET/TSS schools"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models.school import School
from app.models.user import User, UserRole
from app.core.security import get_password_hash
import secrets
import string
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime

def generate_password(length=10):
    """Generate a secure password"""
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

def generate_email(school_name, district):
    """Generate DOS email based on school name and district"""
    # Clean school name: remove special chars, take first 3 words
    clean_name = ''.join(c for c in school_name if c.isalnum() or c.isspace())
    words = clean_name.lower().split()[:3]
    name_part = ''.join(words)
    
    # Clean district
    district_part = district.lower().replace(' ', '')
    
    return f"dos.{name_part}.{district_part}@iprc.ac.rw"

def create_dos_accounts(db: Session):
    """Create DOS accounts for all schools"""
    schools = db.query(School).filter(
        School.type.in_(['TVET', 'TSS'])
    ).all()
    
    credentials = []
    created_count = 0
    skipped_count = 0
    
    print(f"Found {len(schools)} TVET/TSS schools")
    
    for school in schools:
        email = generate_email(school.name, school.district)
        
        # Check if DOS already exists
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            print(f"DOS already exists for {school.name}")
            password = existing.generated_password or "CONTACT_ADMIN"
            skipped_count += 1
        else:
            password = generate_password()
            
            dos_user = User(
                email=email,
                hashed_password=get_password_hash(password),
                full_name=f"DOS - {school.name}",
                role=UserRole.ADMIN,
                school_id=school.id,
                province=school.province,
                district=school.district,
                generated_password=password,
                is_active=1
            )
            
            try:
                db.add(dos_user)
                db.flush()
                created_count += 1
                print(f"Created DOS for {school.name}")
            except Exception as e:
                print(f"Skipped {school.name} - duplicate email")
                db.rollback()
                skipped_count += 1
                existing = db.query(User).filter(User.email == email).first()
                password = existing.generated_password if existing else "CONTACT_ADMIN"
        
        credentials.append({
            'school_id': school.id,
            'school_name': school.name,
            'province': school.province,
            'district': school.district,
            'type': school.type,
            'trades': ', '.join(school.trades) if school.trades else 'N/A',
            'email': email,
            'password': password
        })
    
    db.commit()
    
    print(f"\nCreated: {created_count} new DOS accounts")
    print(f"Skipped: {skipped_count} existing accounts")
    print(f"Total: {len(credentials)} schools")
    
    return credentials

def generate_pdf(credentials, filename="dos_credentials.pdf"):
    """Generate PDF document with all DOS credentials"""
    doc = SimpleDocTemplate(filename, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    
    # Title style
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    # Header
    title = Paragraph("TVET/TSS Schools - DOS Admin Credentials", title_style)
    elements.append(title)
    
    date_text = Paragraph(
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br/>Total Schools: {len(credentials)}",
        styles['Normal']
    )
    elements.append(date_text)
    elements.append(Spacer(1, 0.3*inch))
    
    # Group by province
    provinces = {}
    for cred in credentials:
        prov = cred['province']
        if prov not in provinces:
            provinces[prov] = []
        provinces[prov].append(cred)
    
    # Create tables for each province
    for province, schools in sorted(provinces.items()):
        # Province header
        prov_header = Paragraph(
            f"<b>{province} Province</b> ({len(schools)} schools)",
            styles['Heading2']
        )
        elements.append(prov_header)
        elements.append(Spacer(1, 0.2*inch))
        
        # Table data
        data = [['#', 'School Name', 'District', 'Email', 'Password']]
        
        for idx, school in enumerate(sorted(schools, key=lambda x: x['district']), 1):
            data.append([
                str(idx),
                Paragraph(school['school_name'][:40], styles['Normal']),
                school['district'],
                Paragraph(school['email'], styles['Normal']),
                school['password']
            ])
        
        # Create table
        table = Table(data, colWidths=[0.4*inch, 2.5*inch, 1.2*inch, 2*inch, 1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        
        elements.append(table)
        elements.append(PageBreak())
    
    # Build PDF
    doc.build(elements)
    print(f"\nPDF generated: {filename}")

def main():
    db = SessionLocal()
    try:
        print("Generating DOS accounts for all TVET/TSS schools...\n")
        credentials = create_dos_accounts(db)
        
        print("\nGenerating PDF document...")
        generate_pdf(credentials)
        
        print("\nDone! Check 'dos_credentials.pdf' for all credentials")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
