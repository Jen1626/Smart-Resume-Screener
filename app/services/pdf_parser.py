import fitz

def extract_text_from_pdf(file_path: str) -> str:
    doc = fitz.open(file_path)
    pages = [page.get_text("text") for page in doc]
    text = "\n".join(pages).strip()
    doc.close()
    if not text:
        raise ValueError("No readable text was found in the PDF.")
    return text
