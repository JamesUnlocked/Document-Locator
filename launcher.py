import webbrowser
from threading import Timer
from app import app

def open_browser():
    """Open browser after server starts."""
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == "__main__":
    print("Starting Document Search Engine...")
    print("Opening browser at http://127.0.0.1:5000")
    Timer(1.5, open_browser).start()
    app.run(host="127.0.0.1", port=5000)
