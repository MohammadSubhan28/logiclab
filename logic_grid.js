/**
 * LogicLab Interactive Zebra / Logic Grid Matrix Controller
 * Allows puzzle solvers to toggle elimination states (· -> ✕ -> ✓)
 * across multi-category deduction tables and track completed clues.
 */
class LogicGridController {
    constructor(containerElement, puzzleData, onAnswerSelectCallback) {
        this.container = containerElement;
        this.puzzle = puzzleData;
        this.onAnswerSelect = onAnswerSelectCallback;

        this.people = puzzleData.people || ["Alex", "Blake", "Casey"];
        this.pets = puzzleData.pets || ["Cat", "Dog", "Parrot"];
        this.drinks = puzzleData.drinks || ["Coffee", "Tea", "Lemonade"];
        this.clues = puzzleData.clues || [];

        // Matrix state: { 'person_pet_Alex_Cat': 'empty' | 'no' | 'yes' }
        this.matrixState = {};
        this.checkedClues = new Set();
        this.selectedAnswer = null;

        this.init();
    }

    init() {
        this.render();
        this.attachEvents();
    }

    render() {
        this.container.innerHTML = `
            <div class="logic-grid-container">
                <!-- Clues Checklist -->
                <div class="logic-clues-panel">
                    <div class="panel-header">
                        <h4><span class="icon">📜</span> Clues & Deductions</h4>
                        <span class="clue-tracker-badge" id="clue-tracker">0/${this.clues.length} checked</span>
                    </div>
                    <ul class="clues-list">
                        ${this.clues.map((clue, idx) => `
                            <li class="clue-item" data-clue-index="${idx}">
                                <label class="clue-label">
                                    <input type="checkbox" class="clue-checkbox" data-index="${idx}">
                                    <span class="clue-text">${clue}</span>
                                </label>
                            </li>
                        `).join('')}
                    </ul>
                </div>

                <!-- Interactive Elimination Matrix -->
                <div class="logic-matrix-panel">
                    <div class="panel-header">
                        <h4><span class="icon">📊</span> Deduction Matrix</h4>
                        <div class="matrix-legend">
                            <span class="legend-item"><span class="matrix-badge cell-no">✕</span> Impossible</span>
                            <span class="legend-item"><span class="matrix-badge cell-yes">✓</span> Match</span>
                            <button type="button" class="btn-micro" id="btn-reset-matrix">Clear Grid</button>
                        </div>
                    </div>
                    <div class="matrix-scroll-wrapper">
                        ${this.renderMatrixTableHtml()}
                    </div>
                </div>

                <!-- Final Answer Selection -->
                <div class="logic-answer-selection">
                    <div class="question-callout">
                        <strong>Target Deduction:</strong> ${this.puzzle.question}
                    </div>
                    <div class="answer-options-grid">
                        ${this.puzzle.options.map(opt => `
                            <button type="button" class="btn-option-pill" data-option="${opt}">
                                ${opt}
                            </button>
                        `).join('')}
                    </div>
                </div>
            </div>
        `;
    }

    renderMatrixTableHtml() {
        let html = '<table class="deduction-table"><thead><tr><th class="corner-header">Entity</th>';

        // Header for Pets
        this.pets.forEach(pet => {
            html += `<th class="col-header header-pet">${pet}</th>`;
        });
        // Header for Drinks
        this.drinks.forEach(drink => {
            html += `<th class="col-header header-drink">${drink}</th>`;
        });
        html += '</tr></thead><tbody>';

        // Rows for People
        this.people.forEach(person => {
            html += `<tr><th class="row-header header-person">${person}</th>`;

            // People vs Pets
            this.pets.forEach(pet => {
                const key = `person_pet_${person}_${pet}`;
                const state = this.matrixState[key] || 'empty';
                html += `<td class="matrix-cell ${state !== 'empty' ? 'cell-' + state : ''}" data-key="${key}">
                    ${state === 'yes' ? '✓' : (state === 'no' ? '✕' : '·')}
                </td>`;
            });

            // People vs Drinks
            this.drinks.forEach(drink => {
                const key = `person_drink_${person}_${drink}`;
                const state = this.matrixState[key] || 'empty';
                html += `<td class="matrix-cell ${state !== 'empty' ? 'cell-' + state : ''}" data-key="${key}">
                    ${state === 'yes' ? '✓' : (state === 'no' ? '✕' : '·')}
                </td>`;
            });

            html += '</tr>';
        });

        html += '</tbody></table>';
        return html;
    }

    attachEvents() {
        // Clue checkboxes
        this.container.querySelectorAll('.clue-checkbox').forEach(cb => {
            cb.addEventListener('change', (e) => {
                const idx = parseInt(cb.getAttribute('data-index'), 10);
                const clueItem = cb.closest('.clue-item');
                if (cb.checked) {
                    this.checkedClues.add(idx);
                    clueItem.classList.add('clue-completed');
                } else {
                    this.checkedClues.delete(idx);
                    clueItem.classList.remove('clue-completed');
                }
                const tracker = this.container.querySelector('#clue-tracker');
                if (tracker) tracker.innerText = `${this.checkedClues.size}/${this.clues.length} checked`;
                if (window.soundEngine) window.soundEngine.playClick();
            });
        });

        // Matrix cells click
        this.container.querySelectorAll('.matrix-cell').forEach(cell => {
            cell.addEventListener('click', () => {
                const key = cell.getAttribute('data-key');
                this.cycleCell(key, cell);
            });
        });

        // Reset matrix button
        const resetBtn = this.container.querySelector('#btn-reset-matrix');
        if (resetBtn) {
            resetBtn.addEventListener('click', () => {
                this.matrixState = {};
                this.render();
                this.attachEvents();
                if (window.soundEngine) window.soundEngine.playClick();
            });
        }

        // Option pills
        this.container.querySelectorAll('.btn-option-pill').forEach(btn => {
            btn.addEventListener('click', () => {
                this.container.querySelectorAll('.btn-option-pill').forEach(b => b.classList.remove('selected'));
                btn.classList.add('selected');
                this.selectedAnswer = btn.getAttribute('data-option');
                if (this.onAnswerSelect) this.onAnswerSelect(this.selectedAnswer);
                if (window.soundEngine) window.soundEngine.playClick();
            });
        });
    }

    cycleCell(key, cellEl) {
        // States: empty -> no (✕) -> yes (✓) -> empty
        const current = this.matrixState[key] || 'empty';
        let next = 'no';
        if (current === 'no') next = 'yes';
        else if (current === 'yes') next = 'empty';

        this.matrixState[key] = next;

        // Auto-elimination feature: if 'yes', auto-set peers to 'no'
        if (next === 'yes') {
            const parts = key.split('_'); // ['person', 'pet', personName, petName]
            const categoryA = parts[0];
            const categoryB = parts[1];
            const itemA = parts[2];
            const itemB = parts[3];

            // In this row and column within this category pair:
            // All other items in categoryB for itemA become 'no'
            const targets = categoryB === 'pet' ? this.pets : this.drinks;
            targets.forEach(t => {
                if (t !== itemB) {
                    const peerKey = `${categoryA}_${categoryB}_${itemA}_${t}`;
                    if (this.matrixState[peerKey] !== 'yes') {
                        this.matrixState[peerKey] = 'no';
                    }
                }
            });

            // All other items in categoryA for itemB become 'no'
            this.people.forEach(p => {
                if (p !== itemA) {
                    const peerKey = `${categoryA}_${categoryB}_${p}_${itemB}`;
                    if (this.matrixState[peerKey] !== 'yes') {
                        this.matrixState[peerKey] = 'no';
                    }
                }
            });
        }

        // Re-render table cells
        const wrapper = this.container.querySelector('.matrix-scroll-wrapper');
        if (wrapper) {
            wrapper.innerHTML = this.renderMatrixTableHtml();
            wrapper.querySelectorAll('.matrix-cell').forEach(c => {
                c.addEventListener('click', () => {
                    const k = c.getAttribute('data-key');
                    this.cycleCell(k, c);
                });
            });
        }

        if (window.soundEngine) window.soundEngine.playClick();
    }

    getSelectedAnswer() {
        return this.selectedAnswer;
    }
}

window.LogicGridController = LogicGridController;
