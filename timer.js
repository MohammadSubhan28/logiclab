/**
 * LogicLab Puzzle Timer
 * Supports Stopwatch (forward) and Countdown (sprint challenge) modes with pause/resume.
 */
class PuzzleTimer {
    constructor(displayElement, options = {}) {
        this.display = displayElement;
        this.mode = options.mode || 'stopwatch'; // 'stopwatch' | 'countdown'
        this.duration = options.duration || 180; // 3 minutes default for countdown
        this.onExpire = options.onExpire || null;
        this.onTick = options.onTick || null;

        this.elapsedSeconds = 0;
        this.remainingSeconds = this.duration;
        this.isRunning = false;
        this.timerId = null;

        this.updateDisplay();
    }

    start() {
        if (this.isRunning) return;
        this.isRunning = true;
        this.timerId = setInterval(() => this.tick(), 1000);
    }

    pause() {
        this.isRunning = false;
        if (this.timerId) {
            clearInterval(this.timerId);
            this.timerId = null;
        }
    }

    reset(newDuration = null) {
        this.pause();
        this.elapsedSeconds = 0;
        if (newDuration !== null) this.duration = newDuration;
        this.remainingSeconds = this.duration;
        this.updateDisplay();
    }

    tick() {
        if (this.mode === 'stopwatch') {
            this.elapsedSeconds++;
            if (this.onTick) this.onTick(this.elapsedSeconds);
        } else {
            this.remainingSeconds--;
            if (this.onTick) this.onTick(this.remainingSeconds);
            if (this.remainingSeconds <= 0) {
                this.pause();
                this.remainingSeconds = 0;
                this.updateDisplay();
                if (this.onExpire) this.onExpire();
                return;
            }
        }
        this.updateDisplay();
    }

    updateDisplay() {
        if (!this.display) return;
        const secs = this.mode === 'stopwatch' ? this.elapsedSeconds : this.remainingSeconds;
        const mins = Math.floor(secs / 60);
        const remSecs = secs % 60;
        const formatted = `${String(mins).padStart(2, '0')}:${String(remSecs).padStart(2, '0')}`;
        this.display.innerText = formatted;

        // Add warning pulse for sprint mode under 30s
        if (this.mode === 'countdown' && secs <= 30) {
            this.display.classList.add('timer-warning');
        } else if (this.display.classList.contains('timer-warning')) {
            this.display.classList.remove('timer-warning');
        }
    }

    getTimeSeconds() {
        return this.mode === 'stopwatch' ? this.elapsedSeconds : (this.duration - this.remainingSeconds);
    }
}

window.PuzzleTimer = PuzzleTimer;
