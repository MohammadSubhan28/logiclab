# ⚡ LogicLab – Smart Puzzle Generator & Logic Arena

**LogicLab** is a modern, responsive web application and algorithmic reasoning engine built for students, puzzle enthusiasts, and logic nerds. It generates mathematically valid, unique logic puzzles across 7 specialized categories, offers progressive hint systems, provides complete step-by-step deductive explanations, tracks local progress and streaks, and features challenge modes and an interactive Logic Academy.

---

## 🌟 Key Features

### 1. Algorithmic Puzzle Generation (7 Categories)
- **Sudoku (9×9)**: Algorithmic backtracking generator with unique solution verification and difficulty tuning (Easy, Medium, Hard, Expert). Includes interactive pencil notes (candidate drafting), duplicate and peer highlights, and undo/redo history.
- **Number Sequences**: Arithmetic progressions, geometric progressions, polynomial & quadratic differences ($\Delta_1, \Delta_2$ finite differences method), Fibonacci/Lucas recurrences, and interleaved alternating series with explicit mathematical formulas.
- **Pattern Recognition**: 3×3 Raven Progressive Matrices with rotational symmetry, element count progressions, and geometric fill morphing rendered via clean vector SVGs.
- **Logic Grids (Zebra / Einstein Puzzles)**: Multi-category deductive puzzles with direct, relational, and negative clues, accompanied by an interactive clickable deduction matrix table (`·` $\to$ `✕` $\to$ `✓`) with automated row/column cross-out.
- **Mathematical Logic**: Alphametic cryptarithms (e.g. `SEND + MORE = MONEY`, `BASE + BALL = GAMES`), Target 24 operator balancing, and 4×4 KenKen arithmetic grids with Latin square constraints.
- **Logic Riddles**: Knights and Knaves (truth-tellers and liars) solved via propositional truth tables, River Crossing state space search, and Counterfeit Coin balance scale ternary search trees.
- **Brain Teasers**: Analog clock hand angular geometry ($\theta = |30H - 5.5M|$), Monty Hall Bayesian probability paradox, and non-uniform burning fuse rope timers.

### 2. Smart Puzzle Solver & Progressive Hints
- **Immediate Answer Checking**: Server-side verification for free-text, numeric, multiple choice, and 9×9 Sudoku boards.
- **Progressive 3-Tier Clues**:
  - *Hint 1 (Guiding Area)*: Directs attention to the crucial block or relation.
  - *Hint 2 (Target Constraint)*: Identifies the exact row, column, or formula.
  - *Hint 3 (Direct Step)*: Reveals the specific next deductive step.
- **Step-by-Step Solver Drawer**: Comprehensive breakdown showing the mathematical rules, finite difference tables, and step-by-step logical proofs.

### 3. Challenge Modes
- **Daily Challenge**: Synchronized daily seed derived deterministically from the current calendar date (`YYYY-MM-DD`). Every user worldwide receives the same puzzle on that date with daily streak tracking.
- **3-Minute Timed Sprint (Blitz Challenge)**: Rapid-fire timed challenge where solvers race against a 180-second clock (+500 points for correct answers, -100 points penalty for errors).

### 4. Logic Academy (Learning Mode)
- In-depth masterclasses explaining formal solving strategies:
  1. *Mastering Sudoku*: Naked Singles, Hidden Singles, Snyder Notation, X-Wings.
  2. *The Method of Finite Differences*: Calculating $\Delta_1, \Delta_2$, and closed formulas.
  3. *Elimination Matrices & Zebra Deductions*: Transitive logic and grid elimination.
  4. *Cracking Alphametics & Cryptarithms*: The leading carry law and column bounds.
  5. *Raven Progressive Matrices*: Visual transformation axioms and rotation rules.
  6. *Knights, Knaves & Contradiction*: Formal propositional logic and ternary balance scale trees.
- Interactive *"Practice This Technique"* launcher to jump right into a relevant challenge.

### 5. Player Analytics & 16 Achievement Badges
- Offline stats tracking in browser `localStorage`:
  - Total puzzles attempted & solved, win rate accuracy, average solving time.
  - Category mastery distribution bar graphs.
  - Current daily streak & best streak.
  - Recent solving history log with difficulty and hint count.
  - **16 Unlockable Badges** (Bronze, Silver, Gold, Platinum tiers) with celebratory unlock toasts.
  - Full **Export (JSON)** and **Import (JSON)** functionality to back up or restore progress.

### 6. Modern Interactive UI & Audio Synthesizer
- Dark Nebula, Cyberpunk Neon, and Crisp Light themes.
- Built-in Web Audio API sound synthesizer: generates harmonic chimes, tactile clicks, and victory fanfares completely offline with zero external audio assets.
- Built-in HTML5 Canvas particle confetti explosions on puzzle completion.

---

## 🚀 How to Run the Application Locally

### Prerequisites
- Python 3.9+ (Python 3.10, 3.11, 3.12, 3.15 supported)
- Flask (`pip install flask`)

### Installation & Launch

1. Open your terminal in the project directory:
   ```bash
   cd "path/to/LogicLab"
   ```

2. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```

3. Run the Flask application:
   ```bash
   python app.py
   ```

4. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

---

## 📁 Project Structure

```
├── app.py                      # Flask backend API & application router
├── requirements.txt            # Python dependencies (Flask>=3.0.0)
├── README.md                   # Project documentation
├── generators/                 # Algorithmic puzzle generator engines
│   ├── __init__.py
│   ├── sudoku_gen.py           # 9x9 Sudoku generator, backtracking solver & hints
│   ├── sequence_gen.py         # AP, GP, quadratic difference & recurrence engine
│   ├── math_logic_gen.py       # Alphametic cryptarithms, Target 24 & KenKen grids
│   ├── pattern_gen.py          # 3x3 Raven Progressive Matrices with vector SVGs
│   ├── logic_grid_gen.py       # Einstein / Zebra logic elimination puzzle generator
│   ├── riddle_gen.py           # Knights & Knaves truth tables, River Crossing, Coins
│   └── brain_teaser_gen.py     # Clock angles, Monty Hall odds, rope timers
├── static/
│   ├── css/
│   │   ├── style.css           # Design system, themes (Dark, Light, Cyberpunk), layout
│   │   └── components.css      # Sudoku grid, Zebra matrix, SVGs, timers, badges
│   └── js/
│       ├── audio.js            # Offline Web Audio API sound synthesizer
│       ├── confetti.js         # Canvas particle explosion celebration engine
│       ├── storage.js          # LocalStorage analytics, streaks & 16 badges
│       ├── timer.js            # Stopwatch & sprint countdown timer
│       ├── sudoku_board.js     # Interactive Sudoku controller (notes, keypad, highlights)
│       ├── logic_grid.js       # Interactive deduction matrix & clue tracker
│       ├── visual_pattern.js   # Raven matrix SVG renderer & option cards
│       ├── academy.js          # Academy masterclass viewer & practice launcher
│       └── app.js              # Core SPA router and lifecycle manager
└── templates/
    └── index.html              # Main single-page web application
```

---

## 🛠️ API Reference

- `GET /api/categories` - Returns category list, skills, and difficulties.
- `GET /api/puzzle/generate?category=<cat>&difficulty=<diff>&seed=<seed>` - Generates a puzzle dynamically.
- `GET /api/puzzle/daily?date=YYYY-MM-DD` - Generates the deterministic daily challenge for a given date.
- `POST /api/puzzle/verify` - Validates the user's answer (free-text, choice, or Sudoku grid).
- `GET /api/academy/topics` - Returns all structured tutorials and practice configurations.
