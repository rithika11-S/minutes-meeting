from xhtml2pdf import pisa
import markdown
import io

def convert_markdown_to_pdf(markdown_text, title="Meeting Minutes"):
    """
    Converts markdown text to a PDF file object (bytes).
    """
    # 1. Convert Markdown to HTML
    html_body = markdown.markdown(markdown_text, extensions=['tables', 'fenced_code'])
    
    # 2. Add minimal CSS for styling
    full_html = f"""
    <html>
    <head>
        <style>
            @page {{
                size: A4;
                margin: 2cm;
            }}
            body {{
                font-family: Helvetica, sans-serif;
                font-size: 11pt;
                color: #333;
            }}
            h1 {{ font-size: 18pt; color: #1f2937; margin-bottom: 20px; }}
            h2 {{ font-size: 14pt; color: #10b981; margin-top: 15px; border-bottom: 1px solid #ddd; }}
            h3 {{ font-size: 12pt; color: #374151; margin-top: 10px; }}
            p {{ line-height: 1.5; text-align: justify; }}
            table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f3f4f6; color: #111827; }}
            ul {{ margin-left: 20px; }}
            li {{ margin-bottom: 5px; }}
        </style>
    </head>
    <body>
        <h1>{title}</h1>
        {html_body}
    </body>
    </html>
    """
    
    # 3. Convert HTML to PDF
    pdf_buffer = io.BytesIO()
    pisa_status = pisa.CreatePDF(
        src=full_html,
        dest=pdf_buffer
    )
    
    if pisa_status.err:
        return None
    
    return pdf_buffer.getvalue()
