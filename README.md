# Document Search Engine - Beta Test Version

## ✅ Setup Complete!

All dependencies are installed and the project structure is ready.

## 📁 Project Structure
```
DocSearch/
├── app.py                 # Flask server
├── database.py           # SQLite FTS5 helpers
├── extractor.py          # Multi-format text extraction
├── indexer.py            # Directory scanning & indexing
├── searcher.py           # Search functionality
├── previewer.py          # File preview
├── launcher.py           # Auto-launch browser
├── requirements.txt      # Python dependencies
├── tsconfig.json         # TypeScript config
│
├── database/
│   ├── schema.sql        # Database schema
│   └── documents.db      # (created on first run)
│
├── static/
│   ├── ts/               # TypeScript source
│   ├── js/               # Compiled JavaScript
│   └── style.css         # Styles
│
└── templates/
    └── index.html        # Main UI
```

## 🚀 How to Run

### Method 1: Using the Launcher (Recommended)
```powershell
python launcher.py
```
This will:
- Start the Flask server
- Automatically open your browser to http://127.0.0.1:5000

### Method 2: Manual Start
```powershell
python app.py
```
Then open your browser to: http://127.0.0.1:5000

## 📝 How to Test
 ### First make a ``` test_documents``` dir and make three plain text files that have sentences that include the following words:
  -Flask
  -Search
  -Python
1. **Index Documents:**
   - In the "Index Directory" field, enter: `C:\test_documents`
   - Click "Index Directory"
   - Wait for confirmation (should show files indexed)

2. **Search:**
   - Type a search term like "Python" or "Flask" or "search"
   - Press Enter or click Search
   - Results will appear in the table

3. **Preview:**
   - Click any row in the results table
   - Full file content appears in the preview pane

## 🧪 Test Documents

Sample test documents were created in `C:\test_documents\`:
- test1.txt - Contains: Python, programming
- test2.txt - Contains: Flask, SQLite, databases
- test3.txt - Contains: search engines, information

## 📋 Supported File Formats

✅ Currently Working:
- .txt, .md, .csv, .log (plain text)
- .pdf (via PyPDF2)
- .docx (via python-docx)
- .rtf (via striprtf)
- .html, .htm (via BeautifulSoup)

⚠️ Partially Working:
- .doc (requires antiword or catdoc - not installed)
- .odt, .ods, .odp (requires LibreOffice - not installed)

## 🔧 If You Need to Recompile TypeScript

```powershell
tsc
```

## 🐛 Troubleshooting

### Port Already in Use
If port 5000 is busy, edit `app.py` and change:
```python
app.run(debug=True, host="127.0.0.1", port=5001)
```

### Database Locked
If you get a database locked error:
1. Close the app
2. Delete `database/documents.db`
3. Restart the app (it will recreate the database)

### No Results Found
- Make sure you indexed the directory first
- Check that the directory path is correct
- Try a different search term

## 📊 What to Test

1. ✅ Indexing a directory
2. ✅ Searching for keywords
3. ✅ Previewing files
4. ✅ Re-indexing (should skip unchanged files)
5. ✅ Searching for multiple words
6. ✅ Different file formats (.txt, .pdf, .docx if you have them)

## 🎯 Next Steps

If the beta test goes well, potential enhancements:
- Add .doc support (install antiword)
- Add LibreOffice format support (install LibreOffice)
- Advanced search syntax
- Highlight matches in preview
- Export results
- Dark mode
- Multi-directory indexing

---

**Ready to test!** Just run `python launcher.py`
