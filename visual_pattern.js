/**
 * LogicLab Visual Pattern Recognition Controller
 * Handles progressive matrix display, SVG zooming, and option selection.
 */
class VisualPatternController {
    constructor(containerElement, puzzleData, onAnswerSelectCallback) {
        this.container = containerElement;
        this.puzzle = puzzleData;
        this.onAnswerSelect = onAnswerSelectCallback;
        this.selectedAnswer = null;

        this.init();
    }

    init() {
        this.render();
        this.attachEvents();
    }

    render() {
        this.container.innerHTML = `
            <div class="visual-pattern-wrapper">
                <div class="pattern-intro-banner">
                    <p class="pattern-prompt">
                        <span class="icon">🔍</span> <strong>Objective:</strong> Analyze the horizontal and vertical transformation rules across the matrix cells. Choose the symbol that logically fits in the target cell <strong>?</strong>.
                    </p>
                </div>

                <!-- 3x3 Matrix Grid -->
                <div class="pattern-matrix-card">
                    <div class="pattern-matrix-grid">
                        ${this.renderMatrixCellsHtml()}
                    </div>
                </div>

                <!-- Multiple Choice Options -->
                <div class="pattern-options-container">
                    <h4 class="options-header">Select the Matching Symbol:</h4>
                    <div class="pattern-options-grid">
                        ${this.puzzle.options.map(opt => `
                            <button type="button" class="pattern-option-card" data-label="${opt.label}">
                                <div class="option-badge">${opt.label}</div>
                                <div class="option-svg-wrapper">
                                    ${opt.svg}
                                </div>
                            </button>
                        `).join('')}
                    </div>
                </div>
            </div>
        `;
    }

    renderMatrixCellsHtml() {
        let html = '';
        const grid = this.puzzle.matrix_grid;
        for (let r = 0; r < 3; r++) {
            for (let c = 0; c < 3; c++) {
                const cell = grid[r][c];
                if (cell.is_target) {
                    html += `
                        <div class="pattern-cell pattern-cell-target">
                            <div class="target-indicator">?</div>
                        </div>
                    `;
                } else {
                    html += `
                        <div class="pattern-cell">
                            ${cell.svg}
                        </div>
                    `;
                }
            }
        }
        return html;
    }

    attachEvents() {
        this.container.querySelectorAll('.pattern-option-card').forEach(btn => {
            btn.addEventListener('click', () => {
                this.container.querySelectorAll('.pattern-option-card').forEach(b => b.classList.remove('selected'));
                btn.classList.add('selected');
                this.selectedAnswer = btn.getAttribute('data-label');
                if (this.onAnswerSelect) this.onAnswerSelect(this.selectedAnswer);
                if (window.soundEngine) window.soundEngine.playClick();
            });
        });
    }

    getSelectedAnswer() {
        return this.selectedAnswer;
    }
}

window.VisualPatternController = VisualPatternController;
