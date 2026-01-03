import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.units import inch
import psycopg2

# Read database to get actual schools
DB_CONFIG = {
    'host': 'dpg-d57rkov5r7bs738b03pg-a.oregon-postgres.render.com',
    'port': 5432,
    'database': 'rwanda_edu_db',
    'user': 'rwanda_edu_db_user',
    'password': 'NJmoQ8ze9kV53DT6OB6AAMsa7qetokba'
}

print("Fetching DOS users from database...")
conn = psycopg2.connect(**DB_CONFIG)
cursor = conn.cursor()

cursor.execute("""
    SELECT email, full_name, province, district, school_id 
    FROM users 
    WHERE role = 'ADMIN' 
    ORDER BY province, district, email
""")

dos_users = cursor.fetchall()
cursor.close()
conn.close()

print(f"Found {len(dos_users)} DOS users")

# Create PDF
pdf_file = "FINAL_DOS_CREDENTIALS_ALL_SCHOOLS.pdf"
doc = SimpleDocTemplate(pdf_file, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
elements = []

# Styles
styles = getSampleStyleSheet()
title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=16, textColor=colors.HexColor('#DC2626'), alignment=1)
subtitle_style = ParagraphStyle('CustomSubtitle', parent=styles['Normal'], fontSize=10, textColor=colors.grey, alignment=1)

# Title
elements.append(Paragraph("TSSANYWHERE - DOS LOGIN CREDENTIALS", title_style))
elements.append(Paragraph("Deputy of Studies Access - All TVET/TSS Schools", subtitle_style))
elements.append(Paragraph("Rwanda Ministry of Education", subtitle_style))
elements.append(Spacer(1, 0.3*inch))

# Group by province
current_province = None
for email, full_name, province, district, school_id in dos_users:
    if province != current_province:
        if current_province is not None:
            elements.append(PageBreak())
        
        current_province = province
        elements.append(Paragraph(f"<b>{province.upper()}</b>", styles['Heading2']))
        elements.append(Spacer(1, 0.1*inch))
    
    # Create table for each school
    data = [
        ['School:', full_name],
        ['District:', district],
        ['Email:', email],
        ['Password:', 'dos12024'],
        ['Login URL:', 'https://tssanywhere.pages.dev/admin-login']
    ]
    
    t = Table(data, colWidths=[1.5*inch, 4*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#FEE2E2')),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#DC2626')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    elements.append(t)
    elements.append(Spacer(1, 0.15*inch))

# Footer
elements.append(Spacer(1, 0.3*inch))
elements.append(Paragraph("<i>© 2024 TSSANYWHERE - Ministry of Education, Rwanda</i>", subtitle_style))

# Build PDF
doc.build(elements)
print(f"\nPDF created: {pdf_file}")
print(f"Total DOS users: {len(dos_users)}")
print("\nAll credentials use password: dos12024")
