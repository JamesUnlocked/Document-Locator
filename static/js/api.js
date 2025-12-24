// API functions
export async function indexDirectory(directory) {
    const response = await fetch('/index', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ directory }),
    });
    return await response.json();
}
export async function searchDocuments(query) {
    const response = await fetch('/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
    });
    return await response.json();
}
export async function previewFile(path) {
    const response = await fetch(`/preview?file=${encodeURIComponent(path)}`);
    return await response.json();
}
