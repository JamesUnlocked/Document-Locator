"use strict";
class IndexControls extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
    }
    connectedCallback() {
        this.render();
        this.setupEventListeners();
    }
    render() {
        this.shadowRoot.innerHTML = `
            <style>
                :host {
                    display: block;
                    margin-bottom: 20px;
                    padding: 15px;
                    background-color: #f8f9fa;
                    border-radius: 4px;
                }
                .index-container {
                    display: flex;
                    gap: 10px;
                    margin-bottom: 10px;
                }
                input {
                    flex: 1;
                    padding: 10px;
                    font-size: 14px;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                }
                button {
                    padding: 10px 20px;
                    font-size: 14px;
                    background-color: #28a745;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                }
                button:hover {
                    background-color: #218838;
                }
                button:disabled {
                    background-color: #6c757d;
                    cursor: not-allowed;
                }
                .status {
                    font-size: 14px;
                    color: #666;
                }
                .status.success {
                    color: #28a745;
                }
                .status.error {
                    color: #dc3545;
                }
                .progress-container {
                    width: 100%;
                    height: 4px;
                    background-color: #e0e0e0;
                    border-radius: 2px;
                    margin-top: 10px;
                    overflow: hidden;
                    display: none;
                }
                .progress-container.active {
                    display: block;
                }
                .progress-bar {
                    height: 100%;
                    background: linear-gradient(90deg, #007bff, #0056b3);
                    animation: progress 2s ease-in-out infinite;
                }
                @keyframes progress {
                    0% { width: 0%; }
                    50% { width: 70%; }
                    100% { width: 100%; }
                }
            </style>
            <div class="index-container">
                <input type="text" placeholder="Enter directory path to index..." />
                <button>Index Directory</button>
            </div>
            <div class="progress-container">
                <div class="progress-bar"></div>
            </div>
            <div class="status"></div>
        `;
        this.input = this.shadowRoot.querySelector('input');
        this.button = this.shadowRoot.querySelector('button');
        this.statusDiv = this.shadowRoot.querySelector('.status');
        this.progressContainer = this.shadowRoot.querySelector('.progress-container');
    }
    setupEventListeners() {
        this.button.addEventListener('click', () => this.handleIndex());
    }
    handleIndex() {
        const directory = this.input.value.trim();
        if (directory) {
            this.dispatchEvent(new CustomEvent('index-directory', {
                detail: { directory },
                bubbles: true,
                composed: true
            }));
        }
    }
    setStatus(message, isError = false) {
        this.statusDiv.textContent = message;
        this.statusDiv.className = isError ? 'status error' : 'status success';
    }
    setLoading(loading) {
        this.button.disabled = loading;
        if (loading) {
            this.progressContainer.classList.add('active');
        }
        else {
            this.progressContainer.classList.remove('active');
        }
        this.button.textContent = loading ? 'Indexing...' : 'Index Directory';
    }
}
customElements.define('index-controls', IndexControls);
