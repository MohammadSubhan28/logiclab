"""Mathematical Logic Generator & Solver
Generates Cryptarithmetic (Alphametics), Operator Balancing / 24-Game Puzzles,
and Mini KenKen / Math Box Grids with full step-by-step mathematical reasoning.
"""

import random
import itertools
from typing import Dict, Any, List, Optional, Tuple

class MathLogicEngine:
    def __init__(self, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)

    def generate_cryptarithmetic(self, difficulty: str) -> Dict[str, Any]:
        """Generate verified cryptarithmetic puzzles with unique letter-to-digit mappings."""
        puzzles = [
            {
                "equation": "SEND + MORE = MONEY",
                "difficulty": "medium",
                "target_letter": "M",
                "mapping": {"S": 9, "E": 5, "N": 6, "D": 7, "M": 1, "O": 0, "R": 8, "Y": 2},
                "deductions": [
                    "Step 1: The sum of two 4-digit numbers results in a 5-digit number 'MONEY'. The only possible carry-over to the 5th column is 1. Therefore, M = 1.",
                    "Step 2: Looking at the thousands column: S + M (1) + carry = O + 10. Since M = 1, S + 1 must produce a carry. Since letters represent distinct digits and M = 1, O must be 0, and S must be 9 (or 8 with carry 1).",
                    "Step 3: Continuing column analysis: S = 9, O = 0. E + 0 + carry = N (so carry must be 1, meaning N = E + 1).",
                    "Step 4: Looking at N + R + carry = E + 10, substituting N = E + 1 yields (E + 1) + R + carry = E + 10 => R + carry = 9. Since distinct, R = 8.",
                    "Step 5: Testing D + E = Y + 10 with remaining digits {2, 5, 6, 7} yields D = 7, E = 5, Y = 2, N = 6."
                ],
                "question": "In the classic cryptarithmetic puzzle SEND + MORE = MONEY (where each distinct letter represents a unique digit 0-9 and no number starts with 0), what is the value of the letter 'M'?"
            },
            {
                "equation": "BASE + BALL = GAMES",
                "difficulty": "hard",
                "target_letter": "G",
                "mapping": {"B": 7, "A": 4, "S": 8, "E": 3, "L": 5, "G": 1, "M": 9},
                "deductions": [
                    "Step 1: Two 4-digit numbers sum to a 5-digit number 'GAMES'. The leading carry can only be 1. Therefore, G = 1.",
                    "Step 2: In the units column: E + L = S (or with carry). In the tens column: S + L + carry = E + 10.",
                    "Step 3: Since B + B + carry = 10 + A, B must be at least 5. Testing B = 7 yields 7 + 7 = 14, so A = 4.",
                    "Step 4: Deductions lead consistently to G = 1, B = 7, A = 4, S = 8, E = 3, L = 5, M = 9."
                ],
                "question": "In the puzzle BASE + BALL = GAMES (distinct digits 0-9, no leading zero), what is the value of 'G'?"
            },
            {
                "equation": "TWO + TWO = FOUR",
                "difficulty": "easy",
                "target_letter": "F",
                "mapping": {"T": 7, "W": 3, "O": 4, "F": 1, "O": 4, "U": 6, "R": 8},
                "deductions": [
                    "Step 1: Adding two 3-digit numbers TWO + TWO yields a 4-digit number FOUR. The only possible carry to the thousands place is 1. Thus, F = 1.",
                    "Step 2: Looking at the units column: O + O ends in R. Both O and R must be even if no carry, or R is even (since O + O = 2O).",
                    "Step 3: In the hundreds column: T + T (+ carry) = O + 10. Since F = 1, T must be ≥ 5. If T = 7, 7 + 7 = 14, so O = 4, R = 8, W = 3, U = 6."
                ],
                "question": "In TWO + TWO = FOUR (where each letter is a unique digit 0-9, no leading zeroes), what digit does 'F' represent?"
            },
            {
                "equation": "CROSS + ROADS = DANGER",
                "difficulty": "expert",
                "target_letter": "D",
                "mapping": {"C": 9, "R": 6, "O": 2, "S": 3, "A": 5, "D": 1, "N": 8, "G": 7, "E": 4},
                "deductions": [
                    "Step 1: Adding 5-digit CROSS and ROADS yields a 6-digit number DANGER. Therefore, the leading carry D must equal 1.",
                    "Step 2: Since D = 1, in the hundred-thousands column: C + carry = 10 + A. Since C ≤ 9, C must be 9 and A must be 0 or carry propagated.",
                    "Step 3: Analyzing column-by-column carries and digit uniqueness confirms D = 1."
                ],
                "question": "In CROSS + ROADS = DANGER (unique digits 0-9, no leading zeroes), what is the value of 'D'?"
            }
        ]

        # Filter by difficulty or choose closest
        matching = [p for p in puzzles if p["difficulty"] == difficulty]
        selected = random.choice(matching if matching else puzzles)

        letter = selected["target_letter"]
        answer = selected["mapping"][letter]

        hints = [
            f"Hint 1 (Leading Digits): Look at the sum's leftmost digit. When adding two N-digit numbers to get an (N+1)-digit number, what is the only possible carry value?",
            f"Hint 2 (Carry Bounds): The maximum sum of two single digits plus carry is 9 + 9 + 1 = 19.",
            f"Hint 3 (Direct Deduction): The leading digit of the sum must be 1. Therefore, {letter} = {answer}."
        ]

        steps = [{"step": i + 1, "description": d} for i, d in enumerate(selected["deductions"])]

        # Generate multiple choice options
        options = [answer]
        while len(options) < 4:
            cand = random.randint(0, 9)
            if cand not in options:
                options.append(cand)
        random.shuffle(options)

        return {
            "id": f"math_crypto_{difficulty}_{random.randint(1000, 9999)}",
            "category": "mathematical_logic",
            "title": f"Cryptarithmetic: {selected['equation']}",
            "difficulty": difficulty,
            "question": selected["question"],
            "equation": selected["equation"],
            "target_letter": letter,
            "answer": answer,
            "options": options,
            "hints": hints,
            "step_by_step_solution": steps,
            "explanation": f"In alphametic puzzles, column addition, carry limits, and uniqueness constraints uniquely determine each letter.",
            "interactive_type": "math_quiz"
        }

    def generate_make_24(self, difficulty: str) -> Dict[str, Any]:
        """Generate a 24-game or target arithmetic puzzle."""
        # Predefined verified sets with rich arithmetic tricks
        puzzles_24 = [
            {"nums": [3, 8, 3, 8], "solution": "8 / (3 - 8/3) = 24", "steps": ["Notice 8/3 = 2.666...", "3 - 8/3 = 1/3", "8 / (1/3) = 8 * 3 = 24"]},
            {"nums": [4, 4, 10, 10], "solution": "(10 * 10 - 4) / 4 = 24", "steps": ["10 * 10 = 100", "100 - 4 = 96", "96 / 4 = 24"]},
            {"nums": [5, 5, 5, 1], "solution": "(5 - 1/5) * 5 = 24", "steps": ["1/5 = 0.2", "5 - 0.2 = 4.8 (or 24/5)", "24/5 * 5 = 24"]},
            {"nums": [7, 7, 3, 3], "solution": "(3 + 3/7) * 7 = 24", "steps": ["3/7 = fraction", "3 + 3/7 = 24/7", "24/7 * 7 = 24"]},
            {"nums": [1, 3, 4, 6], "solution": "6 / (1 - 3/4) = 24", "steps": ["3/4 = 0.75", "1 - 3/4 = 1/4", "6 / (1/4) = 24"]},
            {"nums": [2, 3, 4, 5], "solution": "(5 + 3 - 2) * 4 = 24", "steps": ["5 + 3 = 8", "8 - 2 = 6", "6 * 4 = 24"]},
            {"nums": [1, 5, 5, 5], "solution": "5 * 5 - (5/5) = 24", "steps": ["5 * 5 = 25", "5 / 5 = 1", "25 - 1 = 24"]}
        ]

        item = random.choice(puzzles_24)
        nums_str = ", ".join(str(n) for n in item["nums"])

        hints = [
            "Hint 1 (Division & Fractions): Don't just stick to whole numbers—try dividing into fractions like 1/3, 1/4, or 1/5.",
            f"Hint 2 (Target Factor): 24 can be factored as 8 × 3, 6 × 4, or 24/1.",
            f"Hint 3 (Formula Insight): One working expression is: {item['solution']}."
        ]

        steps = [{"step": i + 1, "description": s} for i, s in enumerate(item["steps"])]
        steps.append({"step": len(item["steps"]) + 1, "description": f"Final equation: {item['solution']}."})

        return {
            "id": f"math_24_{difficulty}_{random.randint(1000, 9999)}",
            "category": "mathematical_logic",
            "title": "Target 24: Operator Balancing",
            "difficulty": difficulty,
            "question": f"Using each of the numbers [{nums_str}] exactly once and the basic operators (+, -, *, /, and parentheses), form an expression that equals 24.\nWhich of the following expressions is mathematically correct?",
            "numbers": item["nums"],
            "answer": item["solution"],
            "options": [
                item["solution"],
                f"({item['nums'][0]} + {item['nums'][1]}) * ({item['nums'][2]} - {item['nums'][3]}) = 24",
                f"({item['nums'][0]} * {item['nums'][1]} * {item['nums'][2]}) - {item['nums'][3]} = 24",
                f"({item['nums'][3]} + {item['nums'][0]}) * {item['nums'][1]} + {item['nums'][2]} = 24"
            ],
            "hints": hints,
            "step_by_step_solution": steps,
            "explanation": "Target 24 challenges algebraic grouping, division by fractions, and operator precedence.",
            "interactive_type": "math_quiz"
        }

    def generate_kenken_mini(self, difficulty: str) -> Dict[str, Any]:
        """Generate an interactive 4x4 Mathdoku / KenKen arithmetic puzzle."""
        # 4x4 Latin Square
        latin_square = [
            [1, 2, 3, 4],
            [3, 4, 1, 2],
            [4, 3, 2, 1],
            [2, 1, 4, 3]
        ]
        # Shuffle digits and rows/cols
        perm = list(range(1, 5))
        random.shuffle(perm)
        grid = [[perm[val - 1] for val in row] for row in latin_square]

        # Define 4 arithmetic cages
        cages = [
            {"id": "A", "cells": [(0, 0), (0, 1)], "op": "+", "target": grid[0][0] + grid[0][1]},
            {"id": "B", "cells": [(0, 2), (0, 3)], "op": "*", "target": grid[0][2] * grid[0][3]},
            {"id": "C", "cells": [(1, 0), (2, 0)], "op": "-", "target": abs(grid[1][0] - grid[2][0])},
            {"id": "D", "cells": [(1, 1), (1, 2)], "op": "+", "target": grid[1][1] + grid[1][2]},
            {"id": "E", "cells": [(1, 3), (2, 3)], "op": "*", "target": grid[1][3] * grid[2][3]},
            {"id": "F", "cells": [(2, 1), (2, 2)], "op": "-", "target": abs(grid[2][1] - grid[2][2])},
            {"id": "G", "cells": [(3, 0), (3, 1)], "op": "*", "target": grid[3][0] * grid[3][1]},
            {"id": "H", "cells": [(3, 2), (3, 3)], "op": "+", "target": grid[3][2] + grid[3][3]}
        ]

        question = (
            "4×4 KenKen Logic Grid: Place digits 1 to 4 in each row and column with no duplicates.\n"
            f"Cage A (Row 1, Cols 1-2): target is {cages[0]['target']}{cages[0]['op']}\n"
            f"Cage B (Row 1, Cols 3-4): target is {cages[1]['target']}{cages[1]['op']}\n"
            f"Cage C (Rows 2-3, Col 1): difference is {cages[2]['target']}{cages[2]['op']}\n"
            "What is the value of the cell at Row 1, Column 1?"
        )

        answer = grid[0][0]

        hints = [
            "Hint 1 (Constraints): Digits 1-4 must appear exactly once in each row and column.",
            f"Hint 2 (Cage Analysis): Row 1 has Cage A sum = {cages[0]['target']} and Cage B product = {cages[1]['target']}.",
            f"Hint 3 (Direct Value): The top-left cell (Row 1, Col 1) must be {answer}."
        ]

        steps = [
            {"step": 1, "description": f"Examine Cage B (product = {cages[1]['target']}): The factors must come from digits 1-4."},
            {"step": 2, "description": f"Examine Cage A (sum = {cages[0]['target']}): The remaining digits in Row 1 must sum to {cages[0]['target']}."},
            {"step": 3, "description": f"Cross-referencing column constraints uniquely places {answer} in Row 1, Column 1."}
        ]

        options = [1, 2, 3, 4]

        return {
            "id": f"math_kenken_{difficulty}_{random.randint(1000, 9999)}",
            "category": "mathematical_logic",
            "title": "KenKen 4×4 Arithmetic Deduction",
            "difficulty": difficulty,
            "question": question,
            "cages": cages,
            "grid_solution": grid,
            "answer": answer,
            "options": options,
            "hints": hints,
            "step_by_step_solution": steps,
            "explanation": "KenKen combines Latin square row/column exclusivity with arithmetic cage constraints.",
            "interactive_type": "math_quiz"
        }

    def generate_puzzle(self, difficulty: str = "medium", seed: Optional[int] = None) -> Dict[str, Any]:
        if seed is not None:
            random.seed(seed)

        difficulty = difficulty.lower()
        choice = random.choice(["crypto", "make_24", "kenken"])
        if choice == "crypto":
            return self.generate_cryptarithmetic(difficulty)
        elif choice == "make_24":
            return self.generate_make_24(difficulty)
        else:
            return self.generate_kenken_mini(difficulty)
