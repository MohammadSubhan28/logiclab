/**
 * LogicLab Core Single-Page Application Controller
 * Manages view routing, puzzle lifecycle, API queries, hint reveals,
 * challenge modes (Daily & Sprint), achievement notifications, and analytics.
 */
class LogicLabApp {
    constructor() {
        this.currentView = 'home';
        this.currentPuzzle = null;
        this.activeController = null;
        this.timer = null;
        this.revealedHintsCount = 0;
        this.userSelectedOption = null;
        this.isVerifying = false;

        // Timed Sprint Challenge state
        this.sprintState = {
            isActive: false,
            score: 0,
            solvedCount: 0,
            currentQuestion: 0,
            timer: null,
            puzzles: []
        };

        this.init();
    }

    async init() {
        this.applySettingsTheme();
        this.attachNavigation();
        this.initHomeView();
        this.initArenaControls();
        this.initSprintControls();
        this.initSettingsView();
        this.updateStreakBadge();

        // Academy initialization
        const academyContainer = document.getElementById('academy-container');
        if (academyContainer) {
            this.academy = new AcademyController(academyContainer, (cat, diff) => {
                this.navigate('arena');
                this.generateAndPlay(cat, diff);
            });
        }
    }

    applySettingsTheme() {
        const theme = window.storageManager.settings.theme || 'dark';
        document.documentElement.setAttribute('data-theme', theme);

        const themeSelector = document.getElementById('settings-theme-select');
        if (themeSelector) themeSelector.value = theme;

        const soundToggle = document.getElementById('nav-sound-toggle');
        if (soundToggle) {
            soundToggle.innerText = window.storageManager.settings.soundEnabled ? '🔊' : '🔇';
        }
        window.soundEngine.setEnabled(window.storageManager.settings.soundEnabled);
        window.soundEngine.setVolume(window.storageManager.settings.soundVolume);
    }

    attachNavigation() {
        // Nav link buttons
        document.querySelectorAll('[data-nav-target]').forEach(el => {
            el.addEventListener('click', (e) => {
                const target = el.getAttribute('data-nav-target');
                this.navigate(target);
                if (window.soundEngine) window.soundEngine.playClick();
            });
        });

        // Quick sound toggle in header
        const soundBtn = document.getElementById('nav-sound-toggle');
        if (soundBtn) {
            soundBtn.addEventListener('click', () => {
                const isEnabled = !window.storageManager.settings.soundEnabled;
                window.storageManager.settings.soundEnabled = isEnabled;
                window.storageManager.saveSettings();
                window.soundEngine.setEnabled(isEnabled);
                soundBtn.innerText = isEnabled ? '🔊' : '🔇';
            });
        }

        // Quick theme toggle in header
        const themeBtn = document.getElementById('nav-theme-toggle');
        if (themeBtn) {
            themeBtn.addEventListener('click', () => {
                const current = window.storageManager.settings.theme;
                const next = current === 'dark' ? 'light' : (current === 'light' ? 'cyberpunk' : 'dark');
                window.storageManager.settings.theme = next;
                window.storageManager.saveSettings();
                this.applySettingsTheme();
            });
        }
    }

    navigate(viewName) {
        this.currentView = viewName;

        // Hide all views, show target view
        document.querySelectorAll('.app-view').forEach(view => {
            view.classList.add('hidden');
        });

        const activeView = document.getElementById(`view-${viewName}`);
        if (activeView) activeView.classList.remove('hidden');

        // Update nav active state
        document.querySelectorAll('.nav-link').forEach(link => {
            if (link.getAttribute('data-nav-target') === viewName) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });

        // View-specific initializations
        if (viewName === 'home') {
            this.updateHomeStats();
        } else if (viewName === 'daily') {
            this.initDailyView();
        } else if (viewName === 'stats') {
            this.renderStatsView();
        }

        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    updateStreakBadge() {
        const streakEl = document.getElementById('header-streak-count');
        if (streakEl) {
            streakEl.innerText = window.storageManager.data.currentStreak || 0;
        }
    }

    initHomeView() {
        this.updateHomeStats();

        // CTA buttons
        const btnPlayDaily = document.getElementById('home-btn-play-daily');
        if (btnPlayDaily) {
            btnPlayDaily.addEventListener('click', () => {
                this.navigate('daily');
            });
        }

        const btnPlayRandom = document.getElementById('home-btn-play-random');
        if (btnPlayRandom) {
            btnPlayRandom.addEventListener('click', () => {
                this.navigate('arena');
                this.generateAndPlay('random', 'medium');
            });
        }

        const btnLaunchSprint = document.getElementById('home-btn-launch-sprint');
        if (btnLaunchSprint) {
            btnLaunchSprint.addEventListener('click', () => {
                this.navigate('sprint');
                this.startSprintChallenge();
            });
        }

        // Category Cards on Home
        document.querySelectorAll('.home-category-card').forEach(card => {
            card.addEventListener('click', () => {
                const cat = card.getAttribute('data-category');
                this.navigate('arena');
                this.generateAndPlay(cat, 'medium');
            });
        });
    }

    updateHomeStats() {
        const stats = window.storageManager.data;
        const totalSolvedEl = document.getElementById('home-stat-solved');
        const streakEl = document.getElementById('home-stat-streak');
        const accuracyEl = document.getElementById('home-stat-accuracy');
        const avgTimeEl = document.getElementById('home-stat-avgtime');

        if (totalSolvedEl) totalSolvedEl.innerText = stats.totalSolved;
        if (streakEl) streakEl.innerText = `${stats.currentStreak} Days`;

        const accuracy = stats.totalAttempted > 0 ? Math.round((stats.totalSolved / stats.totalAttempted) * 100) : 100;
        if (accuracyEl) accuracyEl.innerText = `${accuracy}%`;

        const avgSecs = stats.totalSolved > 0 ? Math.round(stats.totalTimeSeconds / stats.totalSolved) : 0;
        const mins = Math.floor(avgSecs / 60);
        const remSecs = avgSecs % 60;
        if (avgTimeEl) avgTimeEl.innerText = `${mins}m ${remSecs}s`;

        this.updateStreakBadge();
    }

    initArenaControls() {
        // Generate button in arena
        const genBtn = document.getElementById('arena-btn-generate');
        if (genBtn) {
            genBtn.addEventListener('click', () => {
                const cat = document.getElementById('arena-select-category').value;
                const diff = document.getElementById('arena-select-difficulty').value;
                const seedInput = document.getElementById('arena-input-seed').value.trim();
                this.generateAndPlay(cat, diff, seedInput || null);
            });
        }

        // Hints button
        const hintBtn = document.getElementById('btn-request-hint');
        if (hintBtn) {
            hintBtn.addEventListener('click', () => this.revealNextHint());
        }

        // Step-by-step solver button
        const solverBtn = document.getElementById('btn-open-solver');
        if (solverBtn) {
            solverBtn.addEventListener('click', () => this.openSolutionDrawer());
        }

        // Check Answer button
        const checkBtn = document.getElementById('btn-submit-answer');
        if (checkBtn) {
            checkBtn.addEventListener('click', () => this.checkCurrentAnswer());
        }

        // Reset Board button
        const resetBtn = document.getElementById('btn-reset-board');
        if (resetBtn) {
            resetBtn.addEventListener('click', () => {
                if (this.currentPuzzle) this.renderPuzzleBoard(this.currentPuzzle);
            });
        }

        // Close solution drawer
        const closeDrawerBtn = document.getElementById('btn-close-drawer');
        const drawerOverlay = document.getElementById('solution-drawer-overlay');
        if (closeDrawerBtn && drawerOverlay) {
            closeDrawerBtn.addEventListener('click', () => drawerOverlay.classList.add('hidden'));
            drawerOverlay.addEventListener('click', (e) => {
                if (e.target === drawerOverlay) drawerOverlay.classList.add('hidden');
            });
        }
    }

    async generateAndPlay(category, difficulty, seed = null) {
        const boardWrapper = document.getElementById('arena-board-container');
        boardWrapper.innerHTML = `
            <div class="board-loading">
                <div class="spinner"></div>
                <p>Synthesizing algorithmic logic puzzle...</p>
            </div>
        `;

        // Update selects if match
        const catSelect = document.getElementById('arena-select-category');
        const diffSelect = document.getElementById('arena-select-difficulty');
        if (catSelect) catSelect.value = category;
        if (diffSelect) diffSelect.value = difficulty;

        try {
            let url = `/api/puzzle/generate?category=${encodeURIComponent(category)}&difficulty=${encodeURIComponent(difficulty)}`;
            if (seed) url += `&seed=${encodeURIComponent(seed)}`;

            const res = await fetch(url);
            const data = await res.json();
            if (data.success && data.puzzle) {
                this.loadPuzzle(data.puzzle);
            } else {
                boardWrapper.innerHTML = '<p class="error-msg">Failed to generate puzzle. Please retry.</p>';
            }
        } catch (e) {
            boardWrapper.innerHTML = `<p class="error-msg">Connection error: ${e.message}</p>`;
        }
    }

    loadPuzzle(puzzle) {
        this.currentPuzzle = puzzle;
        this.revealedHintsCount = 0;
        this.userSelectedOption = null;

        // Cleanup prior controller
        if (this.activeController && typeof this.activeController.destroy === 'function') {
            this.activeController.destroy();
        }
        this.activeController = null;

        // Update header badges
        const titleEl = document.getElementById('arena-puzzle-title');
        const catBadge = document.getElementById('arena-badge-category');
        const diffBadge = document.getElementById('arena-badge-difficulty');
        const seedBadge = document.getElementById('arena-badge-seed');

        if (titleEl) titleEl.innerText = puzzle.title;
        if (catBadge) catBadge.innerText = puzzle.category.replace('_', ' ').toUpperCase();
        if (diffBadge) {
            diffBadge.innerText = puzzle.difficulty.toUpperCase();
            diffBadge.className = `badge badge-${puzzle.difficulty}`;
        }
        if (seedBadge) seedBadge.innerText = puzzle.id;

        // Reset timer
        const timerDisplay = document.getElementById('arena-timer-display');
        if (this.timer) this.timer.reset();
        this.timer = new PuzzleTimer(timerDisplay, { mode: 'stopwatch' });
        this.timer.start();

        // Reset hints UI
        this.updateHintsDisplay();

        // Render board
        this.renderPuzzleBoard(puzzle);

        // Record attempt in storage
        window.storageManager.recordAttempt(puzzle.category, puzzle.difficulty);
    }

    renderPuzzleBoard(puzzle) {
        const container = document.getElementById('arena-board-container');
        container.innerHTML = '';

        if (puzzle.category === 'sudoku') {
            this.activeController = new SudokuBoardController(container, puzzle, (updatedBoard) => {
                // board change listener
            });
        } else if (puzzle.category === 'grid_puzzle') {
            this.activeController = new LogicGridController(container, puzzle, (chosenOption) => {
                this.userSelectedOption = chosenOption;
            });
        } else if (puzzle.category === 'pattern_recognition') {
            this.activeController = new VisualPatternController(container, puzzle, (chosenOption) => {
                this.userSelectedOption = chosenOption;
            });
        } else {
            // General Question & Multiple Choice / Free Input
            this.renderStandardQuestionBoard(container, puzzle);
        }
    }

    renderStandardQuestionBoard(container, puzzle) {
        let optionsHtml = '';
        if (puzzle.options && puzzle.options.length > 0) {
            optionsHtml = `
                <div class="standard-options-grid">
                    ${puzzle.options.map(opt => `
                        <button type="button" class="btn-quiz-option" data-option="${opt}">
                            ${opt}
                        </button>
                    `).join('')}
                </div>
            `;
        } else {
            optionsHtml = `
                <div class="standard-input-wrapper">
                    <input type="text" id="standard-free-input" class="form-input" placeholder="Type your answer here...">
                </div>
            `;
        }

        let sequenceVisual = '';
        if (puzzle.category === 'number_sequence' && puzzle.terms) {
            sequenceVisual = `
                <div class="sequence-chips-row">
                    ${puzzle.terms.map(t => `
                        <div class="sequence-chip ${t === '?' ? 'chip-target' : ''}">
                            ${t}
                        </div>
                    `).join('')}
                </div>
            `;
        }

        container.innerHTML = `
            <div class="standard-puzzle-card">
                <div class="puzzle-question-text">
                    ${puzzle.question.replace(/\n/g, '<br>')}
                </div>
                ${sequenceVisual}
                <div class="puzzle-input-section">
                    ${optionsHtml}
                </div>
            </div>
        `;

        // Attach option click events
        container.querySelectorAll('.btn-quiz-option').forEach(btn => {
            btn.addEventListener('click', () => {
                container.querySelectorAll('.btn-quiz-option').forEach(b => b.classList.remove('selected'));
                btn.classList.add('selected');
                this.userSelectedOption = btn.getAttribute('data-option');
                if (window.soundEngine) window.soundEngine.playClick();
            });
        });

        // Input enter key
        const textInput = container.querySelector('#standard-free-input');
        if (textInput) {
            textInput.addEventListener('keydown', (e) => {
                if (e.key === 'Enter') {
                    this.checkCurrentAnswer();
                }
            });
        }
    }

    updateHintsDisplay() {
        const hintCard = document.getElementById('arena-hint-box');
        const hintBtn = document.getElementById('btn-request-hint');

        if (!hintCard || !this.currentPuzzle) return;

        const totalHints = (this.currentPuzzle.hints && this.currentPuzzle.hints.length) || 3;

        if (this.revealedHintsCount === 0) {
            hintCard.innerHTML = `<p class="hint-placeholder">Need inspiration? Reveal up to ${totalHints} progressive logical hints.</p>`;
            if (hintBtn) hintBtn.innerText = `💡 Reveal Hint 1/${totalHints}`;
        } else {
            let hintsListHtml = '';
            for (let i = 0; i < this.revealedHintsCount; i++) {
                hintsListHtml += `<div class="revealed-hint-item">${this.currentPuzzle.hints[i]}</div>`;
            }
            hintCard.innerHTML = hintsListHtml;

            if (this.revealedHintsCount < totalHints) {
                if (hintBtn) hintBtn.innerText = `💡 Reveal Hint ${this.revealedHintsCount + 1}/${totalHints}`;
            } else {
                if (hintBtn) hintBtn.innerText = `💡 All Hints Revealed`;
            }
        }
    }

    revealNextHint() {
        if (!this.currentPuzzle || !this.currentPuzzle.hints) return;
        if (this.revealedHintsCount < this.currentPuzzle.hints.length) {
            this.revealedHintsCount++;
            this.updateHintsDisplay();
            if (window.soundEngine) window.soundEngine.playHint();
        }
    }

    openSolutionDrawer() {
        if (!this.currentPuzzle) return;
        const drawer = document.getElementById('solution-drawer-overlay');
        const content = document.getElementById('solution-steps-container');
        if (!drawer || !content) return;

        const p = this.currentPuzzle;
        let stepsHtml = `
            <div class="solution-summary">
                <h4><span class="icon">💡</span> Complete Deductive Reasoning</h4>
                <p>${p.explanation || ''}</p>
                ${p.formula ? `<div class="formula-box"><strong>Formula:</strong> <code>${p.formula}</code></div>` : ''}
            </div>
            <div class="solution-steps-timeline">
        `;

        if (p.step_by_step_solution) {
            p.step_by_step_solution.forEach(s => {
                stepsHtml += `
                    <div class="timeline-step">
                        <div class="step-badge">Step ${s.step || ''}</div>
                        <div class="step-body">
                            ${s.technique ? `<strong>${s.technique}:</strong> ` : ''}
                            ${s.description}
                        </div>
                    </div>
                `;
            });
        }
        stepsHtml += '</div>';

        content.innerHTML = stepsHtml;
        drawer.classList.remove('hidden');
        if (window.soundEngine) window.soundEngine.playClick();
    }

    async checkCurrentAnswer() {
        if (!this.currentPuzzle || this.isVerifying) return;
        this.isVerifying = true;

        let userAnswer = null;

        if (this.currentPuzzle.category === 'sudoku') {
            userAnswer = this.activeController.getBoard();
            if (!this.activeController.isComplete()) {
                this.showToast('Please fill all 81 cells of the Sudoku board before submitting.', 'warning');
                this.isVerifying = false;
                return;
            }
        } else if (this.activeController && typeof this.activeController.getSelectedAnswer === 'function') {
            userAnswer = this.activeController.getSelectedAnswer();
        } else if (this.userSelectedOption) {
            userAnswer = this.userSelectedOption;
        } else {
            const input = document.getElementById('standard-free-input');
            if (input) userAnswer = input.value.trim();
        }

        if (userAnswer === null || userAnswer === '') {
            this.showToast('Please select or enter an answer first!', 'warning');
            this.isVerifying = false;
            return;
        }

        try {
            const res = await fetch('/api/puzzle/verify', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    category: this.currentPuzzle.category,
                    user_answer: userAnswer,
                    correct_answer: this.currentPuzzle.answer || this.currentPuzzle.solution
                })
            });

            const data = await res.json();
            this.handleVerificationResult(data.is_correct, data.message);
        } catch (e) {
            this.showToast(`Verification failed: ${e.message}`, 'error');
        } finally {
            this.isVerifying = false;
        }
    }

    handleVerificationResult(isCorrect, message) {
        if (isCorrect) {
            if (this.timer) this.timer.pause();
            const timeElapsed = this.timer ? this.timer.getTimeSeconds() : 0;

            // Trigger sound & confetti
            if (window.soundEngine) window.soundEngine.playSuccess();
            if (window.confettiEngine) window.confettiEngine.trigger(120);

            // Record in storage
            const newBadges = window.storageManager.recordSolved(
                this.currentPuzzle,
                timeElapsed,
                this.revealedHintsCount
            );

            this.updateStreakBadge();

            // Display celebration modal
            this.showCelebrationModal(timeElapsed, newBadges);
        } else {
            if (window.soundEngine) window.soundEngine.playError();
            this.showToast(message || 'Incorrect. Review the clues or try a hint!', 'error');
        }
    }

    showCelebrationModal(timeElapsed, newBadges) {
        const modal = document.getElementById('celebration-modal');
        const timeEl = document.getElementById('celeb-time-stat');
        const hintsEl = document.getElementById('celeb-hints-stat');
        const badgesContainer = document.getElementById('celeb-badges-unlocked');

        const mins = Math.floor(timeElapsed / 60);
        const secs = timeElapsed % 60;
        if (timeEl) timeEl.innerText = `${mins}m ${secs}s`;
        if (hintsEl) hintsEl.innerText = `${this.revealedHintsCount} used`;

        if (badgesContainer) {
            if (newBadges && newBadges.length > 0) {
                badgesContainer.innerHTML = `
                    <div class="new-badges-alert">
                        <h5>🏆 New Achievement Unlocked!</h5>
                        ${newBadges.map(b => `
                            <div class="badge-item-unlocked">
                                <span class="badge-icon">${b.icon}</span>
                                <div><strong>${b.title}</strong>: ${b.desc}</div>
                            </div>
                        `).join('')}
                    </div>
                `;
            } else {
                badgesContainer.innerHTML = '';
            }
        }

        modal.classList.remove('hidden');

        // Play next button
        const btnNext = document.getElementById('celeb-btn-next');
        if (btnNext) {
            btnNext.onclick = () => {
                modal.classList.add('hidden');
                const cat = this.currentPuzzle.category;
                const diff = this.currentPuzzle.difficulty;
                this.generateAndPlay(cat, diff);
            };
        }

        const btnClose = document.getElementById('celeb-btn-close');
        if (btnClose) {
            btnClose.onclick = () => modal.classList.add('hidden');
        }
    }

    showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast-notification toast-${type}`;
        toast.innerHTML = `<span class="toast-icon">${type === 'error' ? '⚠️' : (type === 'warning' ? '🔔' : '✨')}</span> ${message}`;
        document.body.appendChild(toast);

        setTimeout(() => {
            toast.classList.add('toast-fadeout');
            setTimeout(() => toast.remove(), 400);
        }, 3200);
    }

    // Daily Challenge
    async initDailyView() {
        const todayStr = new Date().toISOString().split('T')[0];
        const dateHeader = document.getElementById('daily-date-header');
        if (dateHeader) {
            const formatted = new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
            dateHeader.innerText = formatted;
        }

        const container = document.getElementById('daily-board-container');
        container.innerHTML = '<div class="board-loading"><div class="spinner"></div><p>Retrieving today’s synchronized logic challenge...</p></div>';

        try {
            const res = await fetch(`/api/puzzle/daily?date=${todayStr}`);
            const data = await res.json();
            if (data.success && data.puzzle) {
                // If already solved today, show status
                const isSolved = window.storageManager.data.dailyHistory[todayStr];
                const statusBadge = document.getElementById('daily-status-badge');
                if (statusBadge) {
                    statusBadge.innerText = isSolved ? '✓ Solved Today' : 'Pending Solution';
                    statusBadge.className = isSolved ? 'status-pill status-solved' : 'status-pill status-pending';
                }

                // Render into arena
                this.currentPuzzle = data.puzzle;
                this.renderPuzzleBoard(data.puzzle);
            }
        } catch (e) {
            container.innerHTML = `<p class="error-msg">Failed to load daily puzzle: ${e.message}</p>`;
        }
    }

    // 3-Minute Sprint Timed Challenge
    initSprintControls() {
        const btnStart = document.getElementById('sprint-btn-start');
        if (btnStart) {
            btnStart.addEventListener('click', () => this.startSprintChallenge());
        }

        const btnSubmit = document.getElementById('sprint-btn-submit');
        if (btnSubmit) {
            btnSubmit.addEventListener('click', () => this.checkSprintAnswer());
        }

        const btnPass = document.getElementById('sprint-btn-pass');
        if (btnPass) {
            btnPass.addEventListener('click', () => this.nextSprintPuzzle(false));
        }
    }

    async startSprintChallenge() {
        this.sprintState.isActive = true;
        this.sprintState.score = 0;
        this.sprintState.solvedCount = 0;
        this.sprintState.currentQuestion = 0;

        document.getElementById('sprint-intro-card').classList.add('hidden');
        document.getElementById('sprint-arena-card').classList.remove('hidden');
        document.getElementById('sprint-results-card').classList.add('hidden');

        const scoreEl = document.getElementById('sprint-live-score');
        if (scoreEl) scoreEl.innerText = '0';

        // Timer 180 seconds
        const timerEl = document.getElementById('sprint-timer-display');
        if (this.sprintState.timer) this.sprintState.timer.reset();
        this.sprintState.timer = new PuzzleTimer(timerEl, {
            mode: 'countdown',
            duration: 180,
            onExpire: () => this.finishSprintChallenge()
        });
        this.sprintState.timer.start();

        await this.loadNextSprintQuestion();
    }

    async loadNextSprintQuestion() {
        const container = document.getElementById('sprint-question-container');
        container.innerHTML = '<div class="board-loading"><div class="spinner"></div><p>Loading sprint puzzle...</p></div>';

        const quickCategories = ['number_sequence', 'riddles', 'brain_teasers', 'mathematical_logic'];
        const cat = quickCategories[Math.floor(Math.random() * quickCategories.length)];
        const diff = this.sprintState.solvedCount < 2 ? 'easy' : (this.sprintState.solvedCount < 4 ? 'medium' : 'hard');

        try {
            const res = await fetch(`/api/puzzle/generate?category=${cat}&difficulty=${diff}`);
            const data = await res.json();
            if (data.success) {
                this.sprintState.currentPuzzle = data.puzzle;
                this.renderStandardQuestionBoard(container, data.puzzle);
            }
        } catch (e) {
            container.innerHTML = `<p class="error-msg">Sprint load error: ${e.message}</p>`;
        }
    }

    async checkSprintAnswer() {
        if (!this.sprintState.currentPuzzle) return;
        let ans = this.userSelectedOption;
        if (!ans) {
            const input = document.getElementById('standard-free-input');
            if (input) ans = input.value.trim();
        }

        if (!ans) {
            this.showToast('Select an answer first!', 'warning');
            return;
        }

        const res = await fetch('/api/puzzle/verify', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                category: this.sprintState.currentPuzzle.category,
                user_answer: ans,
                correct_answer: this.sprintState.currentPuzzle.answer
            })
        });

        const data = await res.json();
        if (data.is_correct) {
            this.sprintState.score += 500;
            this.sprintState.solvedCount++;
            if (window.soundEngine) window.soundEngine.playSuccess();
            this.showToast('+500 Points! Correct!', 'info');
        } else {
            this.sprintState.score = Math.max(0, this.sprintState.score - 100);
            if (window.soundEngine) window.soundEngine.playError();
            this.showToast('-100 Points. Keep moving!', 'error');
        }

        const scoreEl = document.getElementById('sprint-live-score');
        if (scoreEl) scoreEl.innerText = this.sprintState.score;

        this.userSelectedOption = null;
        await this.loadNextSprintQuestion();
    }

    nextSprintPuzzle(skipped = true) {
        if (skipped) {
            this.sprintState.score = Math.max(0, this.sprintState.score - 50);
            const scoreEl = document.getElementById('sprint-live-score');
            if (scoreEl) scoreEl.innerText = this.sprintState.score;
        }
        this.userSelectedOption = null;
        this.loadNextSprintQuestion();
    }

    finishSprintChallenge() {
        this.sprintState.isActive = false;
        if (this.sprintState.timer) this.sprintState.timer.pause();

        document.getElementById('sprint-arena-card').classList.add('hidden');
        document.getElementById('sprint-results-card').classList.remove('hidden');

        const finalScoreEl = document.getElementById('sprint-final-score');
        const finalSolvedEl = document.getElementById('sprint-final-solved');

        if (finalScoreEl) finalScoreEl.innerText = this.sprintState.score;
        if (finalSolvedEl) finalSolvedEl.innerText = this.sprintState.solvedCount;

        if (window.soundEngine) window.soundEngine.playVictory();
        if (window.confettiEngine) window.confettiEngine.trigger(150);
    }

    // Stats & Achievements
    renderStatsView() {
        const stats = window.storageManager.data;
        const totalPuzzles = stats.totalSolved;

        // Big summary cards
        document.getElementById('stats-total-solved').innerText = stats.totalSolved;
        document.getElementById('stats-accuracy').innerText = stats.totalAttempted > 0 ? `${Math.round((stats.totalSolved / stats.totalAttempted) * 100)}%` : '100%';
        document.getElementById('stats-best-streak').innerText = `${stats.bestStreak} Days`;

        const avgSecs = stats.totalSolved > 0 ? Math.round(stats.totalTimeSeconds / stats.totalSolved) : 0;
        document.getElementById('stats-avg-time').innerText = `${Math.floor(avgSecs / 60)}m ${avgSecs % 60}s`;

        // Render Category Progress Bars
        const catContainer = document.getElementById('stats-category-bars');
        if (catContainer) {
            let catBarsHtml = '';
            for (const [key, val] of Object.entries(stats.categoryStats)) {
                const displayName = key.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
                const pct = totalPuzzles > 0 ? Math.round((val.solved / totalPuzzles) * 100) : 0;
                catBarsHtml += `
                    <div class="category-stat-row">
                        <div class="row-labels">
                            <span class="category-name">${displayName}</span>
                            <span class="category-count">${val.solved} solved (${pct}%)</span>
                        </div>
                        <div class="progress-bar-track">
                            <div class="progress-bar-fill" style="width: ${pct}%"></div>
                        </div>
                    </div>
                `;
            }
            catContainer.innerHTML = catBarsHtml;
        }

        // Render 16 Achievement Badges
        const badgesContainer = document.getElementById('stats-badges-grid');
        if (badgesContainer) {
            const allBadges = window.storageManager.getAchievementsList();
            let badgesHtml = '';
            allBadges.forEach(b => {
                const isUnlocked = !!stats.unlockedAchievements[b.id];
                badgesHtml += `
                    <div class="badge-card ${isUnlocked ? 'badge-unlocked tier-' + b.tier : 'badge-locked'}">
                        <div class="badge-icon-bubble">${b.icon}</div>
                        <h4 class="badge-title">${b.title}</h4>
                        <p class="badge-desc">${b.desc}</p>
                        <span class="badge-status-tag">${isUnlocked ? 'UNLOCKED' : 'LOCKED'}</span>
                    </div>
                `;
            });
            badgesContainer.innerHTML = badgesHtml;
        }

        // Render History Log
        const historyContainer = document.getElementById('stats-history-tbody');
        if (historyContainer) {
            if (stats.history.length === 0) {
                historyContainer.innerHTML = '<tr><td colspan="5" class="empty-table-msg">No puzzle records yet. Go solve some challenges!</td></tr>';
            } else {
                historyContainer.innerHTML = stats.history.slice(0, 15).map(h => {
                    const mins = Math.floor(h.time / 60);
                    const secs = h.time % 60;
                    return `
                        <tr>
                            <td><strong>${h.title}</strong></td>
                            <td><span class="badge badge-subtle">${h.category.replace('_', ' ')}</span></td>
                            <td><span class="badge badge-${h.difficulty}">${h.difficulty}</span></td>
                            <td>${mins}m ${secs}s</td>
                            <td>${h.hintsUsed === 0 ? '✨ 0 (Flawless)' : h.hintsUsed}</td>
                        </tr>
                    `;
                }).join('');
            }
        }
    }

    initSettingsView() {
        const themeSelect = document.getElementById('settings-theme-select');
        if (themeSelect) {
            themeSelect.value = window.storageManager.settings.theme;
            themeSelect.addEventListener('change', (e) => {
                window.storageManager.settings.theme = e.target.value;
                window.storageManager.saveSettings();
                this.applySettingsTheme();
            });
        }

        const soundToggle = document.getElementById('settings-sound-checkbox');
        if (soundToggle) {
            soundToggle.checked = window.storageManager.settings.soundEnabled;
            soundToggle.addEventListener('change', (e) => {
                window.storageManager.settings.soundEnabled = e.target.checked;
                window.storageManager.saveSettings();
                this.applySettingsTheme();
            });
        }

        const volumeSlider = document.getElementById('settings-volume-slider');
        if (volumeSlider) {
            volumeSlider.value = window.storageManager.settings.soundVolume;
            volumeSlider.addEventListener('input', (e) => {
                const vol = parseFloat(e.target.value);
                window.storageManager.settings.soundVolume = vol;
                window.storageManager.saveSettings();
                window.soundEngine.setVolume(vol);
            });
        }

        // Export data
        const exportBtn = document.getElementById('settings-btn-export');
        if (exportBtn) {
            exportBtn.addEventListener('click', () => {
                const json = window.storageManager.exportJSON();
                const blob = new Blob([json], { type: 'application/json' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `logiclab_backup_${new Date().toISOString().split('T')[0]}.json`;
                a.click();
                URL.revokeObjectURL(url);
                this.showToast('Progress data exported successfully!', 'info');
            });
        }

        // Import data
        const importInput = document.getElementById('settings-file-import');
        if (importInput) {
            importInput.addEventListener('change', (e) => {
                const file = e.target.files[0];
                if (!file) return;
                const reader = new FileReader();
                reader.onload = (evt) => {
                    const success = window.storageManager.importJSON(evt.target.result);
                    if (success) {
                        this.showToast('Progress data restored successfully!', 'info');
                        this.applySettingsTheme();
                        this.updateHomeStats();
                    } else {
                        this.showToast('Failed to import backup file.', 'error');
                    }
                };
                reader.readAsText(file);
            });
        }

        // Reset data
        const resetBtn = document.getElementById('settings-btn-reset');
        if (resetBtn) {
            resetBtn.addEventListener('click', () => {
                if (confirm('Are you sure you want to reset all your stats and achievements? This action cannot be undone.')) {
                    window.storageManager.resetAll();
                    this.updateHomeStats();
                    this.showToast('All player statistics have been reset.', 'info');
                }
            });
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.app = new LogicLabApp();
});
