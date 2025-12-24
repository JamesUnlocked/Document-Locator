// API interface definitions
export interface SearchResult {
    path: string;
    snippet: string;
}

export interface IndexResponse {
    status: string;
    indexed: number;
    skipped: number;
    deleted: number;
    total: number;
    message?: string;
}

export interface PreviewResponse {
    content: string;
}

// API functions
export async function indexDirectory(directory: string): Promise<IndexResponse> {
    const response = await fetch('/index', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ directory }),
    });
    return await response.json();
}

export async function searchDocuments(query: string): Promise<SearchResult[]> {
    const response = await fetch('/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
    });
    return await response.json();
}

export async function previewFile(path: string): Promise<PreviewResponse> {
    const response = await fetch(`/preview?file=${encodeURIComponent(path)}`);
    return await response.json();
}
