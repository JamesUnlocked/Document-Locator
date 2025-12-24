"use strict";
class SearchBar extends HTMLElement {
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
                }
                .search-container {
                    display: flex;
                    gap: 10px;
                }
                input {
                    flex: 1;
                    padding: 10px;
                    font-size: 16px;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                }
                button {
                    padding: 10px 20px;
                    font-size: 16px;
                    background-color: #007bff;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                }
                button:hover {
                    background-color: #0056b3;
                }
            </style>
            <div class="search-container">
                <input type="text" placeholder="Enter search terms..." />
                <button>Search</button>
            </div>
        `;
        this.input = this.shadowRoot.querySelector('input');
        this.button = this.shadowRoot.querySelector('button');
    }
    setupEventListeners() {
        this.button.addEventListener('click', () => this.handleSearch());
        this.input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.handleSearch();
            }
        });
    }
    handleSearch() {
        const query = this.input.value.trim();
        if (query) {
            this.dispatchEvent(new CustomEvent('search', {
                detail: { query },
                bubbles: true,
                composed: true
            }));
        }
    }
}
customElements.define('search-bar', SearchBar);
