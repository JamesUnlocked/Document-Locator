import logging
from database import load_full_content

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_preview(file_path: str):
    """Load full extracted text for a file."""
    if not file_path:
        return ""
    
    logger.info(f"Loading preview for: {file_path}")
    content = load_full_content(file_path)
    
    return content
