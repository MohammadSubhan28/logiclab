/**
 * LogicLab LocalStorage & Achievement Manager
 * Tracks offline statistics, streaks, achievements, and player progress.
 */
class StorageManager {
    constructor() {
        this.STORAGE_KEY = 'logiclab_player_data';
        this.SETTINGS_KEY = 'logiclab_settings';
        this.data = this.loadData();
        this.settings = this.loadSettings();
    }

    getDefaultData() {
        return {
            totalAttempted: 0,
            totalSolved: 0,
            totalTimeSeconds: 0,
            currentStreak: 0,
            bestStreak: 0,
            lastPlayedDate: null,
            dailyHistory: {},
            categoryStats: {
                sudoku: { attempted: 0, solved: 0, totalTime: 0 },
                number_sequence: { attempted: 0, solved: 0, totalTime: 0 },
                pattern_recognition: { attempted: 0, solved: 0, totalTime: 0 },
                grid_puzzle: { attempted: 0, solved: 0, totalTime: 0 },
                mathematical_logic: { attempted: 0, solved: 0, totalTime: 0 },
                riddles: { attempted: 0, solved: 0, totalTime: 0 },
                brain_teasers: { attempted: 0, solved: 0, totalTime: 0 }
            },
            difficultyStats: {
                easy: { attempted: 0, solved: 0 },
                medium: { attempted: 0, solved: 0 },
                hard: { attempted: 0, solved: 0 },
                expert: { attempted: 0, solved: 0 }
            },
            unlockedAchievements: {},
            history: [] // recent 50 solved
        };
    }

    getDefaultSettings() {
        return {
            theme: 'dark', // 'dark', 'light', 'cyberpunk'
            soundEnabled: true,
            soundVolume: 0.6,
            highlightDuplicates: true,
            highlightConflicts: true,
            autoStartTimer: true
        };
    }

    loadData() {
        try {
            const raw = localStorage.getItem(this.STORAGE_KEY);
            if (!raw) return this.getDefaultData();
            const parsed = JSON.parse(raw);
            return { ...this.getDefaultData(), ...parsed };
        } catch (e) {
            console.error('Failed to load storage data', e);
            return this.getDefaultData();
        }
    }

    saveData() {
        try {
            localStorage.setItem(this.STORAGE_KEY, JSON.stringify(this.data));
        } catch (e) {
            console.error('Failed to save data', e);
        }
    }

    loadSettings() {
        try {
            const raw = localStorage.getItem(this.SETTINGS_KEY);
            if (!raw) return this.getDefaultSettings();
            return { ...this.getDefaultSettings(), ...JSON.parse(raw) };
        } catch (e) {
            return this.getDefaultSettings();
        }
    }

    saveSettings() {
        try {
            localStorage.setItem(this.SETTINGS_KEY, JSON.stringify(this.settings));
        } catch (e) {
            console.error('Failed to save settings', e);
        }
    }

    recordAttempt(category, difficulty) {
        this.data.totalAttempted++;
        if (this.data.categoryStats[category]) {
            this.data.categoryStats[category].attempted++;
        }
        if (this.data.difficultyStats[difficulty]) {
            this.data.difficultyStats[difficulty].attempted++;
        }
        this.saveData();
    }

    recordSolved(puzzle, timeElapsedSeconds, hintsUsed) {
        this.data.totalSolved++;
        this.data.totalTimeSeconds += timeElapsedSeconds;

        const cat = puzzle.category;
        const diff = puzzle.difficulty;

        if (!this.data.categoryStats[cat]) {
            this.data.categoryStats[cat] = { attempted: 1, solved: 0, totalTime: 0 };
        }
        this.data.categoryStats[cat].solved++;
        this.data.categoryStats[cat].totalTime += timeElapsedSeconds;

        if (this.data.difficultyStats[diff]) {
            this.data.difficultyStats[diff].solved++;
        }

        // Daily Streak handling
        const todayStr = new Date().toISOString().split('T')[0];
        if (puzzle.is_daily) {
            this.data.dailyHistory[todayStr] = {
                solved: true,
                time: timeElapsedSeconds,
                date: todayStr
            };
        }

        this.updateStreak(todayStr);

        // Add to history log
        this.data.history.unshift({
            id: puzzle.id,
            title: puzzle.title,
            category: cat,
            difficulty: diff,
            time: timeElapsedSeconds,
            hintsUsed: hintsUsed,
            timestamp: new Date().toISOString()
        });
        if (this.data.history.length > 50) {
            this.data.history = this.data.history.slice(0, 50);
        }

        this.saveData();

        // Check for newly unlocked achievements
        const newlyUnlocked = this.checkAchievements(puzzle, timeElapsedSeconds, hintsUsed);
        return newlyUnlocked;
    }

    updateStreak(todayStr) {
        if (!this.data.lastPlayedDate) {
            this.data.currentStreak = 1;
            this.data.lastPlayedDate = todayStr;
        } else if (this.data.lastPlayedDate !== todayStr) {
            const lastDate = new Date(this.data.lastPlayedDate);
            const today = new Date(todayStr);
            const diffDays = Math.round((today - lastDate) / (1000 * 60 * 60 * 24));

            if (diffDays === 1) {
                this.data.currentStreak++;
            } else if (diffDays > 1) {
                this.data.currentStreak = 1;
            }
            this.data.lastPlayedDate = todayStr;
        }

        if (this.data.currentStreak > this.data.bestStreak) {
            this.data.bestStreak = this.data.currentStreak;
        }
    }

    getAchievementsList() {
        return [
            { id: 'first_spark', title: 'First Spark', desc: 'Solve your very first logic puzzle.', icon: '✨', tier: 'bronze' },
            { id: 'speed_demon', title: 'Speed Demon', desc: 'Solve any puzzle in under 30 seconds.', icon: '⚡', tier: 'silver' },
            { id: 'flawless_mind', title: 'Flawless Mind', desc: 'Solve 3 puzzles without using any hints.', icon: '🧠', tier: 'gold' },
            { id: 'streak_3', title: 'Streak Flame', desc: 'Achieve a 3-day daily puzzle streak.', icon: '🔥', tier: 'bronze' },
            { id: 'streak_7', title: 'Relentless Deduction', desc: 'Achieve a 7-day daily puzzle streak.', icon: '🌟', tier: 'gold' },
            { id: 'sudoku_apprentice', title: 'Sudoku Novice', desc: 'Successfully solve a Sudoku grid.', icon: '🔢', tier: 'bronze' },
            { id: 'sudoku_virtuoso', title: 'Sudoku Virtuoso', desc: 'Solve 5 Sudoku challenges.', icon: '👑', tier: 'silver' },
            { id: 'sequence_wizard', title: 'Sequence Wizard', desc: 'Solve 3 Number Sequence puzzles.', icon: '📈', tier: 'silver' },
            { id: 'pattern_seer', title: 'Visual Seer', desc: 'Solve 3 Pattern Recognition puzzles.', icon: '🔮', tier: 'silver' },
            { id: 'zebra_detective', title: 'Zebra Sleuth', desc: 'Solve 3 Logic Grid deduction mysteries.', icon: '🕵️', tier: 'silver' },
            { id: 'crypto_master', title: 'Math Alchemist', desc: 'Solve 3 Mathematical Logic puzzles.', icon: '📐', tier: 'silver' },
            { id: 'riddle_scholar', title: 'Riddle Scholar', desc: 'Solve 3 Classical Logic Riddles.', icon: '📜', tier: 'silver' },
            { id: 'teaser_champ', title: 'Teaser Champion', desc: 'Solve 3 Critical Brain Teasers.', icon: '🎯', tier: 'silver' },
            { id: 'polymath', title: 'True Polymath', desc: 'Solve at least one puzzle in all 7 categories.', icon: '🌌', tier: 'gold' },
            { id: 'expert_conqueror', title: 'Expert Conqueror', desc: 'Solve any Expert difficulty puzzle.', icon: '💎', tier: 'gold' },
            { id: 'grand_master', title: 'Grand Logician', desc: 'Solve 20 total puzzles across the platform.', icon: '🏆', tier: 'platinum' }
        ];
    }

    checkAchievements(puzzle, timeElapsedSeconds, hintsUsed) {
        const newlyUnlocked = [];
        const unlock = (id) => {
            if (!this.data.unlockedAchievements[id]) {
                this.data.unlockedAchievements[id] = {
                    date: new Date().toISOString()
                };
                const badge = this.getAchievementsList().find(b => b.id === id);
                if (badge) newlyUnlocked.push(badge);
            }
        };

        // First spark
        if (this.data.totalSolved >= 1) unlock('first_spark');

        // Speed demon
        if (timeElapsedSeconds <= 30) unlock('speed_demon');

        // Expert conqueror
        if (puzzle.difficulty === 'expert') unlock('expert_conqueror');

        // Flawless mind (count solved with 0 hints)
        const zeroHintCount = this.data.history.filter(h => h.hintsUsed === 0).length;
        if (zeroHintCount >= 3) unlock('flawless_mind');

        // Streaks
        if (this.data.currentStreak >= 3) unlock('streak_3');
        if (this.data.currentStreak >= 7) unlock('streak_7');

        // Category achievements
        const cats = this.data.categoryStats;
        if (cats.sudoku && cats.sudoku.solved >= 1) unlock('sudoku_apprentice');
        if (cats.sudoku && cats.sudoku.solved >= 5) unlock('sudoku_virtuoso');
        if (cats.number_sequence && cats.number_sequence.solved >= 3) unlock('sequence_wizard');
        if (cats.pattern_recognition && cats.pattern_recognition.solved >= 3) unlock('pattern_seer');
        if (cats.grid_puzzle && cats.grid_puzzle.solved >= 3) unlock('zebra_detective');
        if (cats.mathematical_logic && cats.mathematical_logic.solved >= 3) unlock('crypto_master');
        if (cats.riddles && cats.riddles.solved >= 3) unlock('riddle_scholar');
        if (cats.brain_teasers && cats.brain_teasers.solved >= 3) unlock('teaser_champ');

        // Polymath (all 7 categories have >= 1 solved)
        const allSeven = Object.values(cats).filter(c => c.solved >= 1).length >= 7;
        if (allSeven) unlock('polymath');

        // Grand Logician
        if (this.data.totalSolved >= 20) unlock('grand_master');

        if (newlyUnlocked.length > 0) {
            this.saveData();
        }

        return newlyUnlocked;
    }

    exportJSON() {
        return JSON.stringify({
            data: this.data,
            settings: this.settings,
            version: '1.0.0',
            exportedAt: new Date().toISOString()
        }, null, 2);
    }

    importJSON(jsonString) {
        try {
            const parsed = JSON.parse(jsonString);
            if (parsed.data) {
                this.data = { ...this.getDefaultData(), ...parsed.data };
                this.saveData();
            }
            if (parsed.settings) {
                this.settings = { ...this.getDefaultSettings(), ...parsed.settings };
                this.saveSettings();
            }
            return true;
        } catch (e) {
            console.error('Import failed', e);
            return false;
        }
    }

    resetAll() {
        this.data = this.getDefaultData();
        this.saveData();
    }
}

window.storageManager = new StorageManager();
