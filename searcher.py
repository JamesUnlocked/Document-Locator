import logging
from database import search_documents

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_search(query: str):
    """Execute a full-text search query."""
    if not query or not query.strip():
        return []
    
    logger.info(f"Searching for: {query}")
    results = search_documents(query)
    logger.info(f"Found {len(results)} results")
    
    return results
