import './components/search-bar.js';
import './components/index-controls.js';
import './components/results-table.js';
import './components/file-preview.js';
import { indexDirectory, searchDocuments, previewFile } from './api.js';

// Get component references
const indexControls = document.querySelector('index-controls') as any;
const searchBar = document.querySelector('search-bar');
const resultsTable = document.querySelector('results-table') as any;
const filePreview = document.querySelector('file-preview') as any;

// Handle directory indexing
document.addEventListener('index-directory', async (e: any) => {
    const { directory } = e.detail;
    console.log('Indexing directory:', directory);
    
    indexControls.setLoading(true);
    indexControls.setStatus('Indexing...');
    
    try {
        const result = await indexDirectory(directory);
        
        if (result.status === 'ok') {
            const message = `Indexed ${result.indexed} files, skipped ${result.skipped}, deleted ${result.deleted}. Total: ${result.total}`;
            indexControls.setStatus(message);
        } else {
            indexControls.setStatus(result.message || 'Indexing failed', true);
        }
    } catch (error) {
        console.error('Indexing error:', error);
        indexControls.setStatus('Error during indexing', true);
    } finally {
        indexControls.setLoading(false);
    }
});

// Handle search
document.addEventListener('search', async (e: any) => {
    const { query } = e.detail;
    console.log('Searching for:', query);
    
    try {
        const results = await searchDocuments(query);
        console.log('Search results:', results);
        resultsTable.setResults(results);
    } catch (error) {
        console.error('Search error:', error);
        resultsTable.setResults([]);
    }
});

// Handle file preview
document.addEventListener('preview-file', async (e: any) => {
    const { path } = e.detail;
    console.log('Previewing file:', path);
    
    try {
        const result = await previewFile(path);
        filePreview.setContent(path, result.content);
    } catch (error) {
        console.error('Preview error:', error);
        filePreview.setContent(path, 'Error loading preview');
    }
});

console.log('Document Search Engine initialized');
