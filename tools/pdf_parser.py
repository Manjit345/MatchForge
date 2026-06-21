"""
PDF Parser: Extracts text from uploaded resumes using the PyPDF2 library.
"""

import PyPDF2

def extract_resume_text(pdf_file) -> str:
    """
    Extract texts from a PDF file object.

    Args:
        pdf_file: A file-like object representing the PDF file.

    Returns:
        A string containing the extracted text from the PDF.
    """
    try:
        reader = PyPDF2.PdfReader(pdf_file)
    except Exception as e:
        raise ValueError(f"Could not read PDF file. It may be corrupted or not a valid PDF : {e}")

    full_text = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text
    
    if not full_text.strip():
        raise ValueError("No extractable text found in the PDF. This file may be a scanned image or contain non-standard fonts.")

    return full_text

#Code for unit testing the function
if __name__ == "__main__":
    with open("sample_resume.pdf", "rb") as pdf_file:
        resume_text = extract_resume_text(pdf_file)
        print(resume_text)