"use strict";
class FilePreview extends HTMLElement {
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
                }
                .preview-container {
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    background-color: white;
                }
                .preview-title {
                    padding: 15px;
                    background-color: #f8f9fa;
                    border-bottom: 1px solid #ddd;
                    font-weight: bold;
                }
                .preview-content {
                    padding: 20px;
                    max-height: 400px;
                    overflow-y: auto;
                    white-space: pre-wrap;
                    font-family: monospace;
                    font-size: 14px;
                    line-height: 1.5;
                }
                .empty-state {
                    padding: 40px;
                    text-align: center;
                    color: #666;
                }
                .empty-state strong {
                    color: #333;
                    display: block;
                    margin-bottom: 10px;
                    font-size: 16px;
                }
            </style>
            <div class="preview-container">
                <div class="preview-title">File Preview</div>
                <div class="preview-content">
                    <div class="empty-state">
                        <strong>👆 Click any result above to preview</strong>
                        Click on a row in the results table to view the full file content here
                    </div>
                </div>
            </div>
        `;
        this.titleDiv = this.shadowRoot.querySelector('.preview-title');
        this.contentDiv = this.shadowRoot.querySelector('.preview-content');
    }
    setContent(path, content) {
        this.titleDiv.textContent = `File Preview: ${path}`;
        this.contentDiv.textContent = content;
    }
    clear() {
        this.titleDiv.textContent = 'File Preview';
        this.contentDiv.innerHTML = '<div class="empty-state"><strong>👆 Click any result above to preview</strong>Click on a row in the results table to view the full file content here</div>';
    }
}
customElements.define('file-preview', FilePreview);
