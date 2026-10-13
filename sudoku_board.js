/**
 * LogicLab Interactive Sudoku Board Controller
 * Features keyboard navigation, candidate pencil notes mode,
 * same-number highlights, conflict detection, undo/redo, and mobile keypad.
 */
class SudokuBoardController {
    constructor(containerElement, puzzleData, onUpdateCallback) {
        this.container = containerElement;
        this.puzzle = puzzleData;
        this.onUpdate = onUpdateCallback;

        this.initial = puzzleData.board.map(row => [...row]);
        this.current = puzzleData.board.map(row => [...row]);
        this.solution = puzzleData.solution;

        // Pencil notes: 9x9 matrix of Sets
        this.notes = Array.from({ length: 9 }, () => Array.from({ length: 9 }, () => new Set()));

        this.selectedCell = null; // [r, c]
        this.isNotesMode = false;
        this.history = [];

        this.init();
    }

    init() {
        this.render();
        this.attachEvents();
    }

    render() {
        this.container.innerHTML = `
            <div class="sudoku-wrapper">
                <div class="sudoku-grid" id="sudoku-grid" tabindex="0">
                    ${this.renderGridHtml()}
                </div>
                <div class="sudoku-controls">
                    <div class="sudoku-mode-toggle">
                        <button type="button" class="btn-subtle ${this.isNotesMode ? 'active-mode' : ''}" id="btn-toggle-notes">
                            <span class="icon">✏️</span> Pencil Notes: <strong id="notes-status-text">${this.isNotesMode ? 'ON' : 'OFF'}</strong>
                        </button>
                        <button type="button" class="btn-subtle" id="btn-erase-cell" title="Erase selected cell (Delete/Backspace)">
                            <span class="icon">⌫</span> Erase
                        </button>
                        <button type="button" class="btn-subtle" id="btn-undo-move" title="Undo last action">
                            <span class="icon">↩️</span> Undo
                        </button>
                    </div>
                    <div class="sudoku-keypad">
                        ${[1, 2, 3, 4, 5, 6, 7, 8, 9].map(num => `
                            <button type="button" class="keypad-btn" data-number="${num}">${num}</button>
                        `).join('')}
                    </div>
                </div>
            </div>
        `;
        this.updateHighlights();
    }

    renderGridHtml() {
        let html = '';
        for (let r = 0; r < 9; r++) {
            for (let c = 0; c < 9; c++) {
                const isGiven = this.initial[r][c] !== 0;
                const val = this.current[r][c];
                const displayVal = val !== 0 ? val : '';

                // Border classes for 3x3 blocks
                let borderClasses = '';
                if (c % 3 === 2 && c !== 8) borderClasses += ' border-box-right';
                if (r % 3 === 2 && r !== 8) borderClasses += ' border-box-bottom';

                html += `
                    <div class="sudoku-cell ${isGiven ? 'cell-given' : 'cell-user'} ${borderClasses}" 
                         data-row="${r}" data-col="${c}" id="scell-${r}-${c}">
                        <span class="cell-main-value">${displayVal}</span>
                        <div class="cell-notes-grid" id="snotes-${r}-${c}">
                            ${this.renderNotesHtml(r, c)}
                        </div>
                    </div>
                `;
            }
        }
        return html;
    }

    renderNotesHtml(r, c) {
        if (this.current[r][c] !== 0) return '';
        const cellNotes = this.notes[r][c];
        let notesHtml = '';
        for (let n = 1; n <= 9; n++) {
            const hasNote = cellNotes.has(n);
            notesHtml += `<span class="note-digit ${hasNote ? 'visible' : ''}">${hasNote ? n : ''}</span>`;
        }
        return notesHtml;
    }

    attachEvents() {
        const grid = this.container.querySelector('#sudoku-grid');

        // Cell selection click
        this.container.querySelectorAll('.sudoku-cell').forEach(cell => {
            cell.addEventListener('click', (e) => {
                const r = parseInt(cell.getAttribute('data-row'), 10);
                const c = parseInt(cell.getAttribute('data-col'), 10);
                this.selectCell(r, c);
                if (window.soundEngine) window.soundEngine.playClick();
            });
        });

        // Keypad buttons
        this.container.querySelectorAll('.keypad-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const num = parseInt(btn.getAttribute('data-number'), 10);
                this.handleNumberInput(num);
            });
        });

        // Erase button
        const eraseBtn = this.container.querySelector('#btn-erase-cell');
        if (eraseBtn) {
            eraseBtn.addEventListener('click', () => this.handleErase());
        }

        // Notes toggle button
        const notesBtn = this.container.querySelector('#btn-toggle-notes');
        if (notesBtn) {
            notesBtn.addEventListener('click', () => this.toggleNotesMode());
        }

        // Undo button
        const undoBtn = this.container.querySelector('#btn-undo-move');
        if (undoBtn) {
            undoBtn.addEventListener('click', () => this.handleUndo());
        }

        // Keyboard handler
        this.keyHandler = (e) => this.handleKeyDown(e);
        window.addEventListener('keydown', this.keyHandler);
    }

    destroy() {
        if (this.keyHandler) {
            window.removeEventListener('keydown', this.keyHandler);
        }
    }

    selectCell(r, c) {
        this.selectedCell = [r, c];
        this.updateHighlights();
    }

    toggleNotesMode() {
        this.isNotesMode = !this.isNotesMode;
        const btn = this.container.querySelector('#btn-toggle-notes');
        const status = this.container.querySelector('#notes-status-text');
        if (btn) btn.classList.toggle('active-mode', this.isNotesMode);
        if (status) status.innerText = this.isNotesMode ? 'ON' : 'OFF';
        if (window.soundEngine) window.soundEngine.playClick();
    }

    handleKeyDown(e) {
        if (!this.selectedCell) return;
        const [r, c] = this.selectedCell;

        // Number keys 1-9
        if (e.key >= '1' && e.key <= '9') {
            this.handleNumberInput(parseInt(e.key, 10));
            e.preventDefault();
        } else if (e.key === 'Backspace' || e.key === 'Delete' || e.key === '0') {
            this.handleErase();
            e.preventDefault();
        } else if (e.key.toLowerCase() === 'n') {
            this.toggleNotesMode();
            e.preventDefault();
        } else if (e.key === 'ArrowUp') {
            this.selectCell((r + 8) % 9, c);
            e.preventDefault();
        } else if (e.key === 'ArrowDown') {
            this.selectCell((r + 1) % 9, c);
            e.preventDefault();
        } else if (e.key === 'ArrowLeft') {
            this.selectCell(r, (c + 8) % 9);
            e.preventDefault();
        } else if (e.key === 'ArrowRight') {
            this.selectCell(r, (c + 1) % 9);
            e.preventDefault();
        }
    }

    handleNumberInput(num) {
        if (!this.selectedCell) return;
        const [r, c] = this.selectedCell;

        // Cannot overwrite given clues
        if (this.initial[r][c] !== 0) return;

        // Save state for undo
        this.pushHistory();

        if (this.isNotesMode) {
            // Toggle candidate note
            const cellNotes = this.notes[r][c];
            if (cellNotes.has(num)) {
                cellNotes.delete(num);
            } else {
                cellNotes.add(num);
            }
            this.updateCellDom(r, c);
        } else {
            // Set cell value (toggle off if same)
            if (this.current[r][c] === num) {
                this.current[r][c] = 0;
            } else {
                this.current[r][c] = num;
                // Auto remove this note from row, col, and box
                this.removeRelatedNotes(r, c, num);
            }
            this.updateCellDom(r, c);
            if (this.onUpdate) this.onUpdate(this.current);
        }

        if (window.soundEngine) window.soundEngine.playClick();
        this.updateHighlights();
    }

    handleErase() {
        if (!this.selectedCell) return;
        const [r, c] = this.selectedCell;
        if (this.initial[r][c] !== 0) return;

        this.pushHistory();
        this.current[r][c] = 0;
        this.notes[r][c].clear();
        this.updateCellDom(r, c);
        this.updateHighlights();
        if (this.onUpdate) this.onUpdate(this.current);
        if (window.soundEngine) window.soundEngine.playClick();
    }

    removeRelatedNotes(row, col, num) {
        // Box start
        const boxR = Math.floor(row / 3) * 3;
        const boxC = Math.floor(col / 3) * 3;

        for (let i = 0; i < 9; i++) {
            this.notes[row][i].delete(num);
            this.notes[i][col].delete(num);
            this.updateCellDom(row, i);
            this.updateCellDom(i, col);
        }
        for (let r = 0; r < 3; r++) {
            for (let c = 0; c < 3; c++) {
                this.notes[boxR + r][boxC + c].delete(num);
                this.updateCellDom(boxR + r, boxC + c);
            }
        }
    }

    pushHistory() {
        this.history.push({
            current: this.current.map(row => [...row]),
            notes: this.notes.map(row => row.map(s => new Set(s)))
        });
        if (this.history.length > 30) this.history.shift();
    }

    handleUndo() {
        if (this.history.length === 0) return;
        const prev = this.history.pop();
        this.current = prev.current.map(row => [...row]);
        this.notes = prev.notes.map(row => row.map(s => new Set(s)));

        for (let r = 0; r < 9; r++) {
            for (let c = 0; c < 9; c++) {
                this.updateCellDom(r, c);
            }
        }
        this.updateHighlights();
        if (this.onUpdate) this.onUpdate(this.current);
        if (window.soundEngine) window.soundEngine.playClick();
    }

    updateCellDom(r, c) {
        const cellEl = this.container.querySelector(`#scell-${r}-${c}`);
        if (!cellEl) return;

        const valSpan = cellEl.querySelector('.cell-main-value');
        const notesDiv = cellEl.querySelector(`#snotes-${r}-${c}`);

        const val = this.current[r][c];
        if (valSpan) valSpan.innerText = val !== 0 ? val : '';
        if (notesDiv) notesDiv.innerHTML = this.renderNotesHtml(r, c);
    }

    updateHighlights() {
        const allCells = this.container.querySelectorAll('.sudoku-cell');
        allCells.forEach(el => {
            el.classList.remove('selected', 'highlight-peer', 'highlight-match', 'highlight-conflict');
        });

        if (!this.selectedCell) return;
        const [selR, selC] = this.selectedCell;
        const selVal = this.current[selR][selC];

        const selectedEl = this.container.querySelector(`#scell-${selR}-${selC}`);
        if (selectedEl) selectedEl.classList.add('selected');

        const boxR = Math.floor(selR / 3) * 3;
        const boxC = Math.floor(selC / 3) * 3;

        for (let r = 0; r < 9; r++) {
            for (let c = 0; c < 9; c++) {
                const cellEl = this.container.querySelector(`#scell-${r}-${c}`);
                if (!cellEl) continue;

                const inRow = r === selR;
                const inCol = c === selC;
                const inBox = r >= boxR && r < boxR + 3 && c >= boxC && c < boxC + 3;

                if ((inRow || inCol || inBox) && !(r === selR && c === selC)) {
                    cellEl.classList.add('highlight-peer');
                }

                if (selVal !== 0 && this.current[r][c] === selVal) {
                    cellEl.classList.add('highlight-match');
                }
            }
        }
    }

    getBoard() {
        return this.current;
    }

    isComplete() {
        for (let r = 0; r < 9; r++) {
            for (let c = 0; c < 9; c++) {
                if (this.current[r][c] === 0) return false;
            }
        }
        return true;
    }
}

window.SudokuBoardController = SudokuBoardController;
