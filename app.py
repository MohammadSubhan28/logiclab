"""LogicLab - Smart Puzzle Generator Backend
Flask Web Application & REST API
"""

import os
import hashlib
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory

from generators.sudoku_gen import SudokuEngine
from generators.sequence_gen import SequenceEngine
from generators.math_logic_gen import MathLogicEngine
from generators.pattern_gen import PatternEngine
from generators.logic_grid_gen import LogicGridEngine
from generators.riddle_gen import RiddleEngine
from generators.brain_teaser_gen import BrainTeaserEngine

app = Flask(__name__, static_folder="static", template_folder="templates")

# Initialize engines
sudoku_engine = SudokuEngine()
sequence_engine = SequenceEngine()
math_engine = MathLogicEngine()
pattern_engine = PatternEngine()
logic_grid_engine = LogicGridEngine()
riddle_engine = RiddleEngine()
brain_teaser_engine = BrainTeaserEngine()

CATEGORIES = [
    {
        "id": "sudoku",
        "name": "Sudoku",
        "icon": "grid-9",
        "description": "Standard 9×9 grids requiring deduction without guessing.",
        "skills": ["Candidate elimination", "Naked/Hidden singles", "Spatial logic"],
        "tag": "Classic Grid"
    },
    {
        "id": "number_sequence",
        "name": "Number Sequences",
        "icon": "trending-up",
        "description": "Arithmetic, geometric, polynomial, and recurrence patterns.",
        "skills": ["Finite differences", "Pattern induction", "Algebraic rules"],
        "tag": "Mathematical"
    },
    {
        "id": "pattern_recognition",
        "name": "Pattern Recognition",
        "icon": "shapes",
        "description": "3×3 visual progressive matrices with geometric transformations.",
        "skills": ["Rotational symmetry", "Boolean superposition", "Feature mapping"],
        "tag": "Visual / Spatial"
    },
    {
        "id": "grid_puzzle",
        "name": "Logic Grids (Zebra)",
        "icon": "table",
        "description": "Multi-category deductive elimination with relational clues.",
        "skills": ["Cross-referencing", "Transitive deduction", "Constraint satisfaction"],
        "tag": "Deductive Matrix"
    },
    {
        "id": "mathematical_logic",
        "name": "Mathematical Logic",
        "icon": "calculator",
        "description": "Alphametic cryptarithms, target 24 balancing, and KenKen arithmetic.",
        "skills": ["Carry analysis", "Operator precedence", "Arithmetic cages"],
        "tag": "Algebraic"
    },
    {
        "id": "riddles",
        "name": "Logic Riddles",
        "icon": "help-circle",
        "description": "Knights & Knaves, River crossing, and balance scale dilemmas.",
        "skills": ["Proof by contradiction", "State search", "Ternary decision trees"],
        "tag": "Classic Riddles"
    },
    {
        "id": "brain_teasers",
        "name": "Brain Teasers",
        "icon": "zap",
        "description": "Clock hand angles, Monty Hall paradoxes, and non-uniform rope timers.",
        "skills": ["Critical thinking", "Bayesian probability", "Lateral deduction"],
        "tag": "Mental Agility"
    }
]

DIFFICULTIES = ["easy", "medium", "hard", "expert"]

def get_engine_for_category(category: str):
    cat = category.lower()
    if cat == "sudoku":
        return sudoku_engine
    elif cat in ["number_sequence", "sequence", "numbers"]:
        return sequence_engine
    elif cat in ["mathematical_logic", "math", "math_logic"]:
        return math_engine
    elif cat in ["pattern_recognition", "pattern", "patterns"]:
        return pattern_engine
    elif cat in ["grid_puzzle", "logic_grid", "zebra"]:
        return logic_grid_engine
    elif cat in ["riddles", "riddle"]:
        return riddle_engine
    elif cat in ["brain_teasers", "teaser", "teasers"]:
        return brain_teaser_engine
    return None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/categories")
def get_categories():
    return jsonify({
        "categories": CATEGORIES,
        "difficulties": DIFFICULTIES
    })

@app.route("/api/puzzle/generate", methods=["GET"])
def generate_puzzle():
    category = request.args.get("category", "random").lower()
    difficulty = request.args.get("difficulty", "medium").lower()
    seed_arg = request.args.get("seed")

    seed = None
    if seed_arg is not None:
        try:
            seed = int(seed_arg)
        except ValueError:
            seed = int(hashlib.md5(seed_arg.encode()).hexdigest()[:8], 16)

    if category == "random" or not get_engine_for_category(category):
        import random
        cat_obj = random.choice(CATEGORIES)
        category = cat_obj["id"]

    if difficulty not in DIFFICULTIES:
        difficulty = "medium"

    engine = get_engine_for_category(category)
    puzzle = engine.generate_puzzle(difficulty=difficulty, seed=seed)

    # Return puzzle payload
    return jsonify({
        "success": True,
        "puzzle": puzzle
    })

@app.route("/api/puzzle/daily", methods=["GET"])
def get_daily_puzzle():
    date_str = request.args.get("date")
    if not date_str:
        date_str = datetime.now().strftime("%Y-%m-%d")

    # Hash date to get a deterministic integer seed
    date_hash = int(hashlib.md5(date_str.encode("utf-8")).hexdigest()[:8], 16)

    # Cycle categories based on date hash
    cat_index = date_hash % len(CATEGORIES)
    selected_cat = CATEGORIES[cat_index]["id"]

    # Cycle difficulty: Weekdays medium, Saturday hard, Sunday expert
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        weekday = dt.weekday()
        if weekday in [0, 1, 2]:
            difficulty = "medium"
        elif weekday in [3, 4]:
            difficulty = "hard"
        else:
            difficulty = "expert"
    except Exception:
        difficulty = "medium"

    engine = get_engine_for_category(selected_cat)
    puzzle = engine.generate_puzzle(difficulty=difficulty, seed=date_hash)
    puzzle["is_daily"] = True
    puzzle["daily_date"] = date_str

    return jsonify({
        "success": True,
        "daily_date": date_str,
        "puzzle": puzzle
    })

@app.route("/api/puzzle/verify", methods=["POST"])
def verify_puzzle():
    data = request.get_json() or {}
    puzzle_category = data.get("category")
    user_answer = data.get("user_answer")
    correct_answer = data.get("correct_answer")

    if user_answer is None or correct_answer is None:
        return jsonify({"success": False, "error": "Missing answer parameters"}), 400

    # Sudoku board verification
    if puzzle_category == "sudoku":
        # user_answer is 9x9 list, correct_answer is 9x9 list
        try:
            is_correct = True
            for r in range(9):
                for c in range(9):
                    if int(user_answer[r][c]) != int(correct_answer[r][c]):
                        is_correct = False
                        break
                if not is_correct:
                    break
            return jsonify({
                "success": True,
                "is_correct": is_correct,
                "message": "Flawless! Every row, column, and 3x3 block is satisfied!" if is_correct else "Some numbers conflict or are incomplete."
            })
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 400

    # General answer verification with lenient string & numeric matching
    u_str = str(user_answer).strip().lower().replace("°", "").replace(" ", "")
    c_str = str(correct_answer).strip().lower().replace("°", "").replace(" ", "")

    is_correct = (u_str == c_str)

    # Secondary check: numeric equality
    if not is_correct:
        try:
            if float(u_str) == float(c_str):
                is_correct = True
        except ValueError:
            pass

    return jsonify({
        "success": True,
        "is_correct": is_correct,
        "message": "Correct! Brilliant logical deduction!" if is_correct else "Not quite right. Review the clues or request a hint!"
    })

@app.route("/api/academy/topics")
def get_academy_topics():
    topics = [
        {
            "id": "sudoku_techniques",
            "category": "Sudoku",
            "title": "Mastering Sudoku: From Singles to X-Wings",
            "read_time": "5 min read",
            "summary": "Step-by-step techniques to solve any Sudoku without guessing.",
            "sections": [
                {
                    "title": "1. Naked Singles",
                    "content": "A Naked Single occurs when a cell has only one possible candidate remaining because all other numbers 1-9 are already present in its row, column, or 3x3 box."
                },
                {
                    "title": "2. Hidden Singles",
                    "content": "A Hidden Single occurs when a number can only fit into one specific cell in a house (row, column, or block), even if that cell still has other potential candidates."
                },
                {
                    "title": "3. Snyder Notation",
                    "content": "When a 3x3 box has only TWO cells where a digit can go, write down that candidate in small pencil notes in both cells. This immediately reveals pointing pairs."
                },
                {
                    "title": "4. The X-Wing Technique",
                    "content": "When a candidate appears exactly twice in two different rows, and those candidates fall into the exact same two columns, they form a rectangle. You can safely eliminate that candidate from the rest of those two columns!"
                }
            ],
            "practice_category": "sudoku",
            "practice_difficulty": "easy"
        },
        {
            "id": "sequence_methods",
            "category": "Number Sequences",
            "title": "The Method of Finite Differences & Recurrence",
            "read_time": "4 min read",
            "summary": "Crack any polynomial, geometric, or interleaved sequence in seconds.",
            "sections": [
                {
                    "title": "1. The First & Second Differences (Δ1, Δ2)",
                    "content": "Subtract each term from the next. If the differences are constant, the sequence is linear (AP: a*n + b). If the second differences (differences of differences) are constant, it is quadratic (a*n² + b*n + c) where the constant 2nd difference equals 2a!"
                },
                {
                    "title": "2. Geometric Ratios & Oscillations",
                    "content": "If numbers increase by multiplying factors, calculate term ratios (a_{n+1} / a_n). Negative ratios cause terms to oscillate between positive and negative."
                },
                {
                    "title": "3. Interleaved Series Detection",
                    "content": "If the sequence jumps up and down irregularly, split it into odd-positioned terms (1st, 3rd, 5th) and even-positioned terms (2nd, 4th, 6th). Two independent patterns are usually running side-by-side!"
                }
            ],
            "practice_category": "number_sequence",
            "practice_difficulty": "medium"
        },
        {
            "id": "zebra_logic",
            "category": "Logic Grids",
            "title": "Elimination Matrices & Zebra Deductions",
            "read_time": "6 min read",
            "summary": "Systematic grid elimination to solve complex multi-attribute puzzles.",
            "sections": [
                {
                    "title": "1. Direct vs. Relational Clues",
                    "content": "Always execute direct matches first (e.g. 'Alice drinks Coffee'). Place an 'O' in the intersection. Once an 'O' is placed, immediately cross out ('X') all other cells in that row and column within that sub-grid."
                },
                {
                    "title": "2. Transitive Linkage",
                    "content": "If Alice drinks Coffee, and the Coffee drinker owns a Parrot, transitive logic dictates Alice owns the Parrot. Transfer confirmed intersections across matrices!"
                },
                {
                    "title": "3. Positional Bounds",
                    "content": "If 'The green house is immediately to the right of the red house', the red house cannot be the rightmost house, and the green house cannot be the leftmost house."
                }
            ],
            "practice_category": "grid_puzzle",
            "practice_difficulty": "easy"
        },
        {
            "id": "alphametic_rules",
            "category": "Mathematical Logic",
            "title": "Cracking Alphametics & Cryptarithms",
            "read_time": "5 min read",
            "summary": "How to determine letter-to-digit assignments using algebraic bounds.",
            "sections": [
                {
                    "title": "1. The Leading Carry Law",
                    "content": "When two N-digit numbers sum to an (N+1)-digit number, the leftmost digit of the sum MUST be 1. (Example: SEND + MORE = MONEY, M must equal 1)."
                },
                {
                    "title": "2. Leading Zero Constraint",
                    "content": "No standard number begins with the digit 0. Any letter appearing at the front of a word cannot be 0."
                },
                {
                    "title": "3. Parity & Modulo Arithmetic",
                    "content": "If X + X = Y, then Y must be an even number (or ends in an even digit). Look at column unit digits to test parity."
                }
            ],
            "practice_category": "mathematical_logic",
            "practice_difficulty": "medium"
        },
        {
            "id": "raven_matrices",
            "category": "Pattern Recognition",
            "title": "Raven Matrices: Visual Transformation Axioms",
            "read_time": "4 min read",
            "summary": "The 4 fundamental transformation rules used in abstract reasoning tests.",
            "sections": [
                {
                    "title": "1. Rotational Symmetry",
                    "content": "Objects rotate 45°, 90°, or 180° clockwise or counterclockwise across rows. Check if columns mirror the rotation."
                },
                {
                    "title": "2. Element Arithmetic",
                    "content": "Count dots, lines, or sides. Often Row 1 has (1, 2, 3), Row 2 has (2, 3, 4), and Row 3 has (3, 4, 5)."
                },
                {
                    "title": "3. Boolean Overlay (XOR / AND)",
                    "content": "In advanced matrices, Cell 3 is the visual overlay of Cell 1 and Cell 2, or common elements disappear (exclusive-OR rule)."
                }
            ],
            "practice_category": "pattern_recognition",
            "practice_difficulty": "medium"
        },
        {
            "id": "riddle_contradictions",
            "category": "Logic Riddles",
            "title": "Knights, Knaves & Proof by Contradiction",
            "read_time": "5 min read",
            "summary": "Formal propositional logic methods for truth-tellers, liars, and river crossings.",
            "sections": [
                {
                    "title": "1. Assumption & Contradiction",
                    "content": "Assume person A is a Knave (liar). Then evaluate their statement. If the statement turns out to be TRUE, you have reached a contradiction (knaves cannot speak truth). Hence, the assumption is false and A is a Knight."
                },
                {
                    "title": "2. River Crossing State Trees",
                    "content": "Model every bank configuration as a state (Farmer, Wolf, Goat, Cabbage). Never leave {Wolf, Goat} or {Goat, Cabbage} on either bank without the Farmer. The key breakthrough is bringing an item BACK on crossing 4 to prevent conflicts!"
                },
                {
                    "title": "3. Balance Scales & Information Theory",
                    "content": "A two-pan balance scale has 3 outcomes: left-heavy, right-heavy, balanced. In k weighings, you can distinguish at most 3^k possibilities (3^2 = 9 coins, 3^3 = 27 coins)."
                }
            ],
            "practice_category": "riddles",
            "practice_difficulty": "medium"
        }
    ]
    return jsonify({"topics": topics})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"LogicLab Server starting at http://127.0.0.1:{port}")
    app.run(host="127.0.0.1", port=port, debug=True)
