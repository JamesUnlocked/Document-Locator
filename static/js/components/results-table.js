class ResultsTable extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
    }
    connectedCallback() {
        this.render();
    }
    render() {
        this.shadowRoot.innerHTML = `
            <style>
                :host {
                    display: block;
                    margin-bottom: 20px;
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                    background-color: white;
                    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.15);
                    border-radius: 8px;
                    overflow: hidden;
                    table-layout: fixed;
                }
                th {
                    background-color: #007bff;
                    color: white;
                    padding: 12px;
                    text-align: left;
                    font-weight: 600;
                }
                th:last-child {
                    position: relative;
                }
                .help-text {
                    font-size: 11px;
                    font-weight: normal;
                    opacity: 0.9;
                    display: block;
                    margin-top: 3px;
                }
                td {
                    padding: 12px;
                    border-bottom: 2px solid #ccc;
                    border-right: 1px solid #ddd;
                    word-wrap: break-word;
                    overflow-wrap: break-word;
                    max-width: 0;
                }
                td:first-child {
                    width: 40%;
                }
                td:last-child {
                    width: 60%;
                    border-right: none;
                }
                tr {
                    cursor: pointer;
                    border-bottom: 2px solid #ccc;
                }
                tr:hover {
                    background-color: #f5f5f5;
                    box-shadow: inset 0 0 0 1px #007bff;
                }
                .snippet {
                    color: #666;
                    font-size: 14px;
                }
                .no-results {
                    padding: 20px;
                    text-align: center;
                    color: #666;
                }
            </style>
            <table>
                <thead>
                    <tr>
                        <th>File Path <span class="help-text">⬇ Click any row to preview full content</span></th>
                        <th>Match Preview</th>
                    </tr>
                </thead>
                <tbody></tbody>
            </table>
        `;
        this.tbody = this.shadowRoot.querySelector('tbody');
    }
    setResults(results) {
        this.tbody.innerHTML = '';
        if (results.length === 0) {
            const row = this.tbody.insertRow();
            const cell = row.insertCell();
            cell.colSpan = 2;
            cell.className = 'no-results';
            cell.textContent = 'No results found';
            return;
        }
        results.forEach(result => {
            const row = this.tbody.insertRow();
            row.addEventListener('click', () => {
                this.dispatchEvent(new CustomEvent('preview-file', {
                    detail: { path: result.path },
                    bubbles: true,
                    composed: true
                }));
            });
            const pathCell = row.insertCell();
            pathCell.textContent = result.path;
            const snippetCell = row.insertCell();
            snippetCell.className = 'snippet';
            snippetCell.innerHTML = result.snippet;
        });
    }
}
customElements.define('results-table', ResultsTable);
export {};
