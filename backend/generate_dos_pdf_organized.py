import json
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT

# Load credentials
with open('dos_credentials_from_excel.json', 'r', encoding='utf-8') as f:
    credentials = json.load(f)

# Create PDF
pdf_file = "DOS_CREDENTIALS_BY_PROVINCE_DISTRICT_SCHOOL.pdf"
doc = SimpleDocTemplate(pdf_file, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
elements = []

# Styles
styles = getSampleStyleSheet()
title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=16, textColor=colors.HexColor('#1e40af'), alignment=TA_CENTER, spaceAfter=12)
heading_style = ParagraphStyle('CustomHeading', parent=styles['Heading2'], fontSize=12, textColor=colors.HexColor('#3b82f6'), spaceAfter=6)
normal_style = styles['Normal']

# Title
elements.append(Paragraph("TSSANYWHERE - DOS Admin Credentials", title_style))
elements.append(Paragraph("Ministry of Education, Rwanda", ParagraphStyle('Subtitle', parent=styles['Normal'], fontSize=10, alignment=TA_CENTER, textColor=colors.grey)))
elements.append(Spacer(1, 0.3*inch))

# Group by Province
provinces = {}
for cred in credentials:
    province = cred['province']
    if province not in provinces:
        provinces[province] = {}
    
    district = cred['district']
    if district not in provinces[province]:
        provinces[province][district] = []
    
    provinces[province][district].append(cred)

# Generate content
for province, districts in sorted(provinces.items()):
    # Province header
    elements.append(Paragraph(f"<b>{province.upper()} PROVINCE</b>", heading_style))
    elements.append(Spacer(1, 0.1*inch))
    
    for district, schools in sorted(districts.items()):
        # District subheader
        elements.append(Paragraph(f"District: {district}", ParagraphStyle('District', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#6366f1'), leftIndent=10)))
        elements.append(Spacer(1, 0.05*inch))
        
        # Table data
        data = [['#', 'School Name', 'Username', 'Password', 'School Code']]
        
        for idx, school in enumerate(schools, 1):
            data.append([
                str(idx),
                school['school_name'][:35],
                school['username'],
                school['password'],
                school['school_code']
            ])
        
        # Create table
        table = Table(data, colWidths=[0.4*inch, 2.5*inch, 1.8*inch, 1.2*inch, 0.9*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f9ff')])
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.2*inch))
    
    elements.append(PageBreak())

# Build PDF
doc.build(elements)
print(f"PDF generated: {pdf_file}")
print(f"Total schools: {len(credentials)}")
print(f"Provinces covered: {len(provinces)}")
