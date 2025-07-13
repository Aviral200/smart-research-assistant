import logging
import PyPDF2
import pdfplumber

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_text_from_pdf(file) -> str:
    text = ""
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    except Exception as e:
        logger.warning(f"pdfplumber failed: {e}, using PyPDF2 fallback.")
        try:
            file.seek(0)
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() or ""
        except Exception as e2:
            logger.error(f"PyPDF2 also failed: {e2}")
    return text or ""
