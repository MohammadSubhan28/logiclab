/**
 * LogicLab Web Audio API Synthesizer
 * Generates futuristic, pleasant sound effects dynamically without external audio files.
 */
class SoundEngine {
    constructor() {
        this.ctx = null;
        this.enabled = true;
        this.volume = 0.5;
        this.init();
    }

    init() {
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        if (AudioContext) {
            this.ctx = new AudioContext();
        }
    }

    ensureContext() {
        if (!this.ctx) this.init();
        if (this.ctx && this.ctx.state === 'suspended') {
            this.ctx.resume();
        }
    }

    setEnabled(enabled) {
        this.enabled = enabled;
    }

    setVolume(val) {
        this.volume = Math.max(0, Math.min(1, val));
    }

    playClick() {
        if (!this.enabled || !this.ctx) return;
        this.ensureContext();
        try {
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();
            osc.type = 'sine';
            osc.frequency.setValueAtTime(600, this.ctx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(300, this.ctx.currentTime + 0.05);

            gain.gain.setValueAtTime(0.15 * this.volume, this.ctx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.01, this.ctx.currentTime + 0.05);

            osc.connect(gain);
            gain.connect(this.ctx.destination);

            osc.start();
            osc.stop(this.ctx.currentTime + 0.05);
        } catch (e) {
            // Audio policy fallback
        }
    }

    playSuccess() {
        if (!this.enabled || !this.ctx) return;
        this.ensureContext();
        try {
            // Harmonic arpeggio (C5 -> E5 -> G5 -> C6)
            const notes = [523.25, 659.25, 783.99, 1046.50];
            const startTime = this.ctx.currentTime;

            notes.forEach((freq, idx) => {
                const osc = this.ctx.createOscillator();
                const gain = this.ctx.createGain();

                osc.type = 'triangle';
                osc.frequency.setValueAtTime(freq, startTime + idx * 0.07);

                gain.gain.setValueAtTime(0.2 * this.volume, startTime + idx * 0.07);
                gain.gain.exponentialRampToValueAtTime(0.001, startTime + idx * 0.07 + 0.28);

                osc.connect(gain);
                gain.connect(this.ctx.destination);

                osc.start(startTime + idx * 0.07);
                osc.stop(startTime + idx * 0.07 + 0.3);
            });
        } catch (e) {}
    }

    playError() {
        if (!this.enabled || !this.ctx) return;
        this.ensureContext();
        try {
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();

            osc.type = 'sawtooth';
            osc.frequency.setValueAtTime(180, this.ctx.currentTime);
            osc.frequency.linearRampToValueAtTime(140, this.ctx.currentTime + 0.15);

            gain.gain.setValueAtTime(0.18 * this.volume, this.ctx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.01, this.ctx.currentTime + 0.15);

            osc.connect(gain);
            gain.connect(this.ctx.destination);

            osc.start();
            osc.stop(this.ctx.currentTime + 0.15);
        } catch (e) {}
    }

    playHint() {
        if (!this.enabled || !this.ctx) return;
        this.ensureContext();
        try {
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();

            osc.type = 'sine';
            osc.frequency.setValueAtTime(440, this.ctx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(880, this.ctx.currentTime + 0.2);

            gain.gain.setValueAtTime(0.18 * this.volume, this.ctx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.01, this.ctx.currentTime + 0.25);

            osc.connect(gain);
            gain.connect(this.ctx.destination);

            osc.start();
            osc.stop(this.ctx.currentTime + 0.25);
        } catch (e) {}
    }

    playVictory() {
        if (!this.enabled || !this.ctx) return;
        this.ensureContext();
        try {
            // Chime fanfare: G4 -> C5 -> E5 -> G5
            const chord = [392.00, 523.25, 659.25, 783.99, 1046.50];
            const startTime = this.ctx.currentTime;

            chord.forEach((freq, idx) => {
                const osc = this.ctx.createOscillator();
                const gain = this.ctx.createGain();

                osc.type = 'sine';
                osc.frequency.setValueAtTime(freq, startTime + idx * 0.1);

                gain.gain.setValueAtTime(0.22 * this.volume, startTime + idx * 0.1);
                gain.gain.exponentialRampToValueAtTime(0.001, startTime + idx * 0.1 + 0.6);

                osc.connect(gain);
                gain.connect(this.ctx.destination);

                osc.start(startTime + idx * 0.1);
                osc.stop(startTime + idx * 0.1 + 0.65);
            });
        } catch (e) {}
    }
}

window.soundEngine = new SoundEngine();
