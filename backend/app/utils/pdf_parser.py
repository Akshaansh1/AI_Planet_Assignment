import fitz  # PyMuPDF

def parse_pdf(file_path: str) -> str:
    """
    Parses a PDF file and extracts text content.
    """
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        print(f"Error parsing PDF {file_path}: {e}")
        return ""
