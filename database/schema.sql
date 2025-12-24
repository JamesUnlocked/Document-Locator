CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY,
    path TEXT UNIQUE,
    modified INTEGER
);

CREATE VIRTUAL TABLE IF NOT EXISTS documents_fts USING fts5(
    path,
    content
);
