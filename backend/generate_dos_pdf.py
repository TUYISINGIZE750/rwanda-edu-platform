from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.units import inch
from app.core.database import SessionLocal
from app.models.user import User
from app.models.school import School
from datetime import datetime

db = SessionLocal()

# Get all DOS users
dos_users = db.query(User).filter(User.role == 'admin').order_by(User.full_name).all()

print(f"Found {len(dos_users)} DOS accounts")

# Create PDF
pdf_file = "DOS_CREDENTIALS_ALL_SCHOOLS.pdf"
doc = SimpleDocTemplate(pdf_file, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
elements = []

# Styles
styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=16,
    textColor=colors.HexColor('#1e40af'),
    spaceAfter=12,
    alignment=1
)

# Title
elements.append(Paragraph("TSSANYWHERE - DOS CREDENTIALS", title_style))
elements.append(Paragraph(f"All School Administrator Accounts", styles['Normal']))
elements.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
elements.append(Spacer(1, 0.3*inch))

# Table data
data = [['#', 'School Name', 'Email', 'Password', 'District']]

for idx, dos in enumerate(dos_users, 1):
    # Get school info
    school_name = dos.full_name.replace('DOS - ', '').replace('Test Admin (DOS)', 'Main Admin')
    
    # Extract district from email
    email_parts = dos.email.split('.')
    district = email_parts[-1].replace('@iprc.ac.rw', '').upper() if len(email_parts) > 1 else 'N/A'
    
    # Default password
    password = 'dos123' if 'dos@' in dos.email or 'dos.' in dos.email else 'admin123'
    
    data.append([
        str(idx),
        school_name[:40],  # Truncate long names
        dos.email,
        password,
        district
    ])

# Create table
table = Table(data, colWidths=[0.4*inch, 2.2*inch, 2.5*inch, 0.8*inch, 0.8*inch])
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 9),
    ('FONTSIZE', (0, 1), (-1, -1), 7),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
    ('TOPPADDING', (0, 1), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f3f4f6')])
]))

elements.append(table)

# Footer
elements.append(Spacer(1, 0.3*inch))
elements.append(Paragraph("<b>Login URL:</b> https://tssanywhere.pages.dev/login", styles['Normal']))
elements.append(Paragraph("<b>Note:</b> All DOS accounts use password 'dos123' by default", styles['Normal']))
elements.append(Paragraph("<b>Total Schools:</b> " + str(len(dos_users)), styles['Normal']))

# Build PDF
doc.build(elements)

print(f"PDF created: {pdf_file}")
print(f"Total DOS accounts: {len(dos_users)}")

db.close()
