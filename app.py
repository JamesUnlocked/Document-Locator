from flask import Flask, request, jsonify, render_template
import logging
from indexer import run_indexing
from searcher import run_search
from previewer import get_preview
from database import initialize_database

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Initialize SQLite FTS5 database on startup
initialize_database()
logger.info("Database initialized")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/index", methods=["POST"])
def index_route():
    """Index a directory."""
    data = request.json
    directory = data.get("directory")
    logger.info(f"Indexing request for directory: {directory}")
    result = run_indexing(directory)
    return jsonify(result)

@app.route("/search", methods=["POST"])
def search_route():
    """Search indexed documents."""
    data = request.json
    query = data.get("query")
    logger.info(f"Search request for query: {query}")
    results = run_search(query)
    return jsonify(results)

@app.route("/preview", methods=["GET"])
def preview_route():
    """Get full content of a file."""
    file_path = request.args.get("file")
    logger.info(f"Preview request for file: {file_path}")
    content = get_preview(file_path)
    return jsonify({"content": content})

if __name__ == "__main__":
    logger.info("Starting Flask server on http://127.0.0.1:5000")
    app.run(debug=True, host="127.0.0.1", port=5000)
