import os
import logging
from extractor import extract_text_from_file
from database import upsert_document, delete_document, get_connection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SUPPORTED_EXTENSIONS = {
    ".txt", ".md", ".csv", ".log",
    ".doc", ".docx",
    ".odt", ".ods", ".odp", ".ott", ".fodt",
    ".pdf",
    ".rtf",
    ".html", ".htm"
}

def run_indexing(directory: str):
    """Index all supported files in a directory."""
    logger.info(f"Starting indexing for directory: {directory}")
    
    if not os.path.isdir(directory):
        logger.error(f"Invalid directory: {directory}")
        return {"status": "error", "message": "Invalid directory"}

    try:
        indexed_paths = set()
        conn = get_connection()
        cursor = conn.cursor()

        # Load existing indexed paths
        cursor.execute("SELECT path FROM documents")
        for row in cursor.fetchall():
            indexed_paths.add(row["path"])

        conn.close()
        logger.info(f"Found {len(indexed_paths)} previously indexed files")
    except Exception as e:
        logger.error(f"Error loading existing index: {e}")
        indexed_paths = set()

    found_paths = set()
    indexed_count = 0
    skipped_count = 0

    # Walk directory tree
    for root, dirs, files in os.walk(directory):
        for filename in files:
            ext = os.path.splitext(filename)[1].lower()
            if ext not in SUPPORTED_EXTENSIONS:
                continue

            full_path = os.path.join(root, filename)
            found_paths.add(full_path)

            try:
                modified = int(os.path.getmtime(full_path))

                # Check if file is new or modified
                if full_path not in indexed_paths:
                    logger.info(f"Indexing new file: {full_path}")
                    _index_file(full_path, modified)
                    indexed_count += 1
                else:
                    # Check if modified timestamp changed
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute("SELECT modified FROM documents WHERE path = ?", (full_path,))
                    row = cursor.fetchone()
                    conn.close()

                    if row and row["modified"] != modified:
                        logger.info(f"Re-indexing modified file: {full_path}")
                        _index_file(full_path, modified)
                        indexed_count += 1
                    else:
                        skipped_count += 1
            except Exception as e:
                logger.error(f"Error processing {full_path}: {e}")

    # Remove deleted files from index
    deleted_files = indexed_paths - found_paths
    for path in deleted_files:
        logger.info(f"Removing deleted file from index: {path}")
        delete_document(path)

    return {
        "status": "ok",
        "indexed": indexed_count,
        "skipped": skipped_count,
        "deleted": len(deleted_files),
        "total": len(found_paths)
    }


def _index_file(path: str, modified: int):
    """Extract text and update database."""
    try:
        text = extract_text_from_file(path)
        upsert_document(path, modified, text)
    except Exception as e:
        logger.error(f"Error indexing {path}: {e}")
