"""Super Admin API for system-wide management"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..core.database import get_db
from ..models.school import School
from ..models.user import User, UserRole
from ..core.security import get_password_hash
import secrets
import string
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER
from datetime import datetime
import os

router = APIRouter(prefix="/super-admin", tags=["super-admin"])

def generate_password(length=10):
    """Generate a secure password"""
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

def generate_email(school_name, district):
    """Generate DOS email based on school name and district"""
    clean_name = ''.join(c for c in school_name if c.isalnum() or c.isspace())
    words = clean_name.lower().split()[:3]
    name_part = ''.join(words)
    district_part = district.lower().replace(' ', '')
    return f"dos.{name_part}.{district_part}@iprc.ac.rw"

@router.post("/generate-dos-accounts")
def generate_dos_accounts(db: Session = Depends(get_db)):
    """Generate DOS accounts for all TVET/TSS schools"""
    schools = db.query(School).filter(
        School.type.in_(['TVET', 'TSS'])
    ).all()
    
    credentials = []
    created_count = 0
    skipped_count = 0
    
    for school in schools:
        email = generate_email(school.name, school.district)
        
        existing = db.query(User).filter(User.email == email).first()
        if existing:
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
            except:
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
    
    return {
        "success": True,
        "created": created_count,
        "skipped": skipped_count,
        "total": len(credentials),
        "credentials": credentials
    }

@router.get("/download-dos-credentials")
def download_dos_credentials(db: Session = Depends(get_db)):
    """Generate and download PDF with all DOS credentials"""
    schools = db.query(School).filter(
        School.type.in_(['TVET', 'TSS'])
    ).all()
    
    credentials = []
    for school in schools:
        email = generate_email(school.name, school.district)
        user = db.query(User).filter(User.email == email).first()
        password = user.generated_password if user else "NOT_CREATED"
        
        credentials.append({
            'school_name': school.name,
            'province': school.province,
            'district': school.district,
            'type': school.type,
            'email': email,
            'password': password
        })
    
    # Generate PDF
    filename = f"dos_credentials_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = os.path.join("/tmp", filename)
    
    doc = SimpleDocTemplate(filepath, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
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
    
    for province, schools in sorted(provinces.items()):
        prov_header = Paragraph(
            f"<b>{province} Province</b> ({len(schools)} schools)",
            styles['Heading2']
        )
        elements.append(prov_header)
        elements.append(Spacer(1, 0.2*inch))
        
        data = [['#', 'School Name', 'District', 'Email', 'Password']]
        
        for idx, school in enumerate(sorted(schools, key=lambda x: x['district']), 1):
            data.append([
                str(idx),
                Paragraph(school['school_name'][:40], styles['Normal']),
                school['district'],
                Paragraph(school['email'], styles['Normal']),
                school['password']
            ])
        
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
    
    doc.build(elements)
    
    return FileResponse(
        filepath,
        media_type='application/pdf',
        filename=filename
    )
