import os
import subprocess
from bs4 import BeautifulSoup
from striprtf.striprtf import rtf_to_text
from docx import Document
from PyPDF2 import PdfReader

# ---------------------------
# Main entry point
# ---------------------------

def extract_text_from_file(path: str) -> str:
    """Extract text from any supported file format."""
    ext = os.path.splitext(path)[1].lower()
    try:
        if ext in [".txt", ".md", ".csv", ".log"]:
            return _extract_text_plain(path)

        elif ext == ".docx":
            return _extract_docx(path)

        elif ext == ".doc":
            return _extract_doc(path)

        elif ext in [".odt", ".ods", ".odp", ".ott", ".fodt"]:
            return _extract_libreoffice(path)

        elif ext == ".pdf":
            return _extract_pdf(path)

        elif ext == ".rtf":
            return _extract_rtf(path)

        elif ext in [".html", ".htm"]:
            return _extract_html(path)

        else:
            return ""
    except Exception as e:
        print(f"Extraction error for {path}: {e}")
        return ""


# ---------------------------
# Plain text formats
# ---------------------------

def _extract_text_plain(path: str) -> str:
    """Extract plain text files."""
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


# ---------------------------
# DOCX
# ---------------------------

def _extract_docx(path: str) -> str:
    """Extract text from .docx files."""
    doc = Document(path)
    return "\n".join([p.text for p in doc.paragraphs])


# ---------------------------
# DOC (via antiword or catdoc)
# ---------------------------

def _extract_doc(path: str) -> str:
    """Extract text from .doc files using antiword or catdoc."""
    try:
        result = subprocess.run(
            ["antiword", path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.stdout:
            return result.stdout
    except FileNotFoundError:
        pass

    try:
        result = subprocess.run(
            ["catdoc", path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.stdout:
            return result.stdout
    except FileNotFoundError:
        pass

    return ""


# ---------------------------
# LibreOffice formats (ODT, ODS, ODP, etc.)
# ---------------------------

def _extract_libreoffice(path: str) -> str:
    """Extract text from LibreOffice formats using headless conversion."""
    temp_dir = os.path.join(os.getcwd(), "temp")
    os.makedirs(temp_dir, exist_ok=True)
    
    # Try soffice first (Windows), then libreoffice (Linux/Mac)
    soffice_cmd = r"C:\Program Files\LibreOffice\program\soffice.exe"
    
    try:
        subprocess.run(
            [soffice_cmd, "--headless", "--convert-to", "txt", "--outdir", temp_dir, path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30
        )
        base = os.path.splitext(os.path.basename(path))[0]
        txt_path = os.path.join(temp_dir, base + ".txt")

        if os.path.exists(txt_path):
            with open(txt_path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
            os.remove(txt_path)
            return text
    except Exception as e:
        print(f"LibreOffice extraction error for {path}: {e}")

    return ""


# ---------------------------
# PDF
# ---------------------------

def _extract_pdf(path: str) -> str:
    """Extract text from PDF files."""
    try:
        reader = PdfReader(path)
        text = []
        for page in reader.pages:
            text.append(page.extract_text() or "")
        return "\n".join(text)
    except Exception as e:
        print(f"PDF extraction error for {path}: {e}")
        return ""


# ---------------------------
# RTF
# ---------------------------

def _extract_rtf(path: str) -> str:
    """Extract text from RTF files."""
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return rtf_to_text(f.read())


# ---------------------------
# HTML
# ---------------------------

def _extract_html(path: str) -> str:
    """Extract text from HTML files."""
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
        return soup.get_text(separator="\n")
