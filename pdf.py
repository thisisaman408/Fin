import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

def parse_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    sections = []
    section = []
    is_weights_section = False

    for line in lines:
        line = line.strip()

        # Start a new section based on the iteration or portfolio results
        if "Iteration" in line or "Portfolio Optimization Results" in line:
            if section:
                sections.append(section)
            section = [line]
            is_weights_section = False
        elif "Optimal Portfolio Weights:" in line:
            section.append(line)
            is_weights_section = True
        elif line and is_weights_section:
            section.append(line)
        elif line:
            section.append(line)

    if section:
        sections.append(section)
    
    return sections

def create_pdf(data_sections, output_pdf):
    pdf = SimpleDocTemplate(output_pdf, pagesize=A4)
    content = []
    styles = getSampleStyleSheet()

    for section in data_sections:
        # Extracting the header for each section
        header = section[0]
        content.append(Paragraph(f"<b>{header}</b>", styles['Heading2']))
        content.append(Spacer(1, 12))

        # Extracting data and creating tables if "Optimal Portfolio Weights" is present
        data_rows = []
        weights_started = False
        for line in section:
            if "Weight" in line:
                weights_started = True
            elif weights_started and line:
                parts = line.split()
                if len(parts) > 1:
                    asset = ' '.join(parts[:-1])
                    weight = parts[-1]
                    data_rows.append([asset, weight])
        
        # Add table to PDF if data_rows has content
        if data_rows:
            df = pd.DataFrame(data_rows, columns=["Asset", "Weight"])
            table_data = [df.columns.to_list()] + df.values.tolist()
            table = Table(table_data)

            # Adding styles to the table
            style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ])
            table.setStyle(style)

            content.append(table)
            content.append(Spacer(1, 24))
        else:
            # If no weights section, add a message
            content.append(Paragraph("No optimal portfolio weights available.", styles['BodyText']))
            content.append(Spacer(1, 24))

    pdf.build(content)

# Usage
file_path = 'data.txt'  # Ensure data.txt is in the same folder
output_pdf = 'portfolio_report.pdf'

# Parse the data and generate the PDF
sections = parse_data(file_path)
create_pdf(sections, output_pdf)

print(f"PDF generated: {output_pdf}")