import sqlite3
import os

DB_PATH = os.path.join("database", "documents.db")

# ---------------------------
# Connection + Initialization
# ---------------------------

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    """Create tables if they do not exist."""
    conn = get_connection()
    cursor = conn.cursor()

    schema_path = os.path.join("database", "schema.sql")
    with open(schema_path, "r") as f:
        cursor.executescript(f.read())

    conn.commit()
    conn.close()


# ---------------------------
# Metadata Helpers
# ---------------------------

def get_all_indexed_paths():
    """Return a set of all indexed file paths."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT path FROM documents")
    rows = cursor.fetchall()
    conn.close()
    return {row["path"] for row in rows}


def get_document_modified(path: str):
    """Return last modified timestamp for a file in the index."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT modified FROM documents WHERE path = ?", (path,))
    row = cursor.fetchone()
    conn.close()
    return row["modified"] if row else None


# ---------------------------
# Indexing Helpers
# ---------------------------

def upsert_document(path: str, modified: int, content: str):
    """Insert or update a document and its FTS5 content."""
    conn = get_connection()
    cursor = conn.cursor()

    # Check if document exists
    cursor.execute("SELECT id FROM documents WHERE path = ?", (path,))
    row = cursor.fetchone()

    if row:
        # Update existing document
        doc_id = row["id"]
        cursor.execute("UPDATE documents SET modified = ? WHERE id = ?", (modified, doc_id))
        cursor.execute("DELETE FROM documents_fts WHERE rowid = ?", (doc_id,))
        cursor.execute("INSERT INTO documents_fts (rowid, path, content) VALUES (?, ?, ?)", (doc_id, path, content))
    else:
        # Insert new document
        cursor.execute("INSERT INTO documents (path, modified) VALUES (?, ?)", (path, modified))
        doc_id = cursor.lastrowid
        cursor.execute("INSERT INTO documents_fts (rowid, path, content) VALUES (?, ?, ?)", (doc_id, path, content))

    conn.commit()
    conn.close()


def delete_document(path: str):
    """Remove a document from both metadata and FTS tables."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM documents WHERE path = ?", (path,))
    row = cursor.fetchone()

    if row:
        doc_id = row["id"]
        cursor.execute("DELETE FROM documents WHERE id = ?", (doc_id,))
        cursor.execute("DELETE FROM documents_fts WHERE rowid = ?", (doc_id,))

    conn.commit()
    conn.close()


# ---------------------------
# Search + Preview Helpers
# ---------------------------

def search_documents(query: str):
    """Perform a full-text search and return path + snippet."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT path,
               snippet(documents_fts, 1, '<b>', '</b>', '...', 20) AS snippet
        FROM documents_fts
        WHERE documents_fts MATCH ?
    """, (query,))

    results = cursor.fetchall()
    conn.close()

    return [dict(row) for row in results]


def load_full_content(path: str):
    """Return full extracted text for preview."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT content
        FROM documents_fts
        WHERE path = ?
    """, (path,))

    row = cursor.fetchone()
    conn.close()

    return row["content"] if row else ""
