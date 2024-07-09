from docx import Document
from io import BytesIO

class Report:
    def __init__(self):
        self.doc = Document()

    def add_content(self,heading,content):
        self.doc.add_heading(heading,level=1)
        self.doc.add_paragraph(content)

    def return_doc(self):
        return self.doc
    
    def convert_bytes(self):
        f=BytesIO()
        self.doc.save(f)
        f.seek(0)
        return f

