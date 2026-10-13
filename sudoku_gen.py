"""Sudoku Generator & Solver
Generates 9x9 Sudoku puzzles with guaranteed unique solutions,
supports multiple difficulty levels, progressive hints, and step-by-step explanations.
"""

import random
import copy
from typing import List, Tuple, Optional, Dict, Any

class SudokuEngine:
    def __init__(self, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)

    def is_valid(self, board: List[List[int]], row: int, col: int, num: int) -> bool:
        """Check if placing num at board[row][col] is valid."""
        # Check row
        for c in range(9):
            if board[row][c] == num:
                return False
        # Check column
        for r in range(9):
            if board[r][col] == num:
                return False
        # Check 3x3 box
        start_row, start_col = (row // 3) * 3, (col // 3) * 3
        for r in range(3):
            for c in range(3):
                if board[start_row + r][start_col + c] == num:
                    return False
        return True

    def find_empty(self, board: List[List[int]]) -> Optional[Tuple[int, int]]:
        """Find the next empty cell with the fewest candidates (MRV heuristic for speed)."""
        best_cell = None
        min_candidates = 10
        for r in range(9):
            for c in range(9):
                if board[r][c] == 0:
                    candidates = [n for n in range(1, 10) if self.is_valid(board, r, c, n)]
                    if len(candidates) < min_candidates:
                        min_candidates = len(candidates)
                        best_cell = (r, c)
                        if min_candidates <= 1:
                            return best_cell
        return best_cell

    def solve(self, board: List[List[int]]) -> bool:
        """Solve board using backtracking with MRV heuristic."""
        empty = self.find_empty(board)
        if not empty:
            return True
        row, col = empty
        candidates = [n for n in range(1, 10) if self.is_valid(board, row, col, n)]
        random.shuffle(candidates)
        for num in candidates:
            board[row][col] = num
            if self.solve(board):
                return True
            board[row][col] = 0
        return False

    def count_solutions(self, board: List[List[int]], limit: int = 2) -> int:
        """Count the number of solutions up to limit (to test uniqueness)."""
        empty = self.find_empty(board)
        if not empty:
            return 1
        row, col = empty
        candidates = [n for n in range(1, 10) if self.is_valid(board, row, col, n)]
        count = 0
        for num in candidates:
            board[row][col] = num
            count += self.count_solutions(board, limit - count)
            board[row][col] = 0
            if count >= limit:
                break
        return count

    def generate_full_board(self) -> List[List[int]]:
        """Generate a complete valid 9x9 Sudoku grid."""
        board = [[0 for _ in range(9)] for _ in range(9)]
        # Fill diagonal 3x3 boxes independently
        for box in range(0, 9, 3):
            nums = list(range(1, 10))
            random.shuffle(nums)
            idx = 0
            for r in range(3):
                for c in range(3):
                    board[box + r][box + c] = nums[idx]
                    idx += 1
        # Solve the rest of the board
        self.solve(board)
        return board

    def generate_puzzle(self, difficulty: str = "medium", seed: Optional[int] = None) -> Dict[str, Any]:
        """Generate a Sudoku puzzle with target difficulty and unique solution."""
        if seed is not None:
            random.seed(seed)

        difficulty = difficulty.lower()
        # Target clue counts
        clue_targets = {
            "easy": random.randint(36, 40),
            "medium": random.randint(30, 34),
            "hard": random.randint(26, 29),
            "expert": random.randint(23, 25)
        }
        target_clues = clue_targets.get(difficulty, 32)

        full_board = self.generate_full_board()
        solution = copy.deepcopy(full_board)
        puzzle = copy.deepcopy(full_board)

        cells = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(cells)

        current_clues = 81
        for r, c in cells:
            if current_clues <= target_clues:
                break
            removed_val = puzzle[r][c]
            puzzle[r][c] = 0

            # Test uniqueness
            test_board = copy.deepcopy(puzzle)
            if self.count_solutions(test_board, limit=2) != 1:
                # Not unique, put it back
                puzzle[r][c] = removed_val
            else:
                current_clues -= 1

        hints, steps = self.deduce_hints_and_steps(puzzle, solution)

        return {
            "id": f"sudoku_{difficulty}_{random.randint(1000, 9999)}",
            "category": "sudoku",
            "title": f"Sudoku ({difficulty.capitalize()})",
            "difficulty": difficulty,
            "board": puzzle,
            "solution": solution,
            "clues_count": current_clues,
            "hints": hints,
            "step_by_step_solution": steps,
            "explanation": (
                "Each row, column, and 3x3 box must contain the digits 1 through 9 with no repetition. "
                "Use deduction techniques like Naked Singles, Hidden Singles, and Elimination."
            ),
            "interactive_type": "sudoku_grid"
        }

    def get_candidates(self, board: List[List[int]], row: int, col: int) -> List[int]:
        """Get valid candidate numbers for a cell."""
        if board[row][col] != 0:
            return []
        return [n for n in range(1, 10) if self.is_valid(board, row, col, n)]

    def deduce_hints_and_steps(self, puzzle: List[List[int]], solution: List[List[int]]) -> Tuple[List[str], List[Dict[str, Any]]]:
        """Generate logical hints and a logical step-by-step solving path."""
        working_board = copy.deepcopy(puzzle)
        steps = []
        first_naked_single = None

        # Simulate logical solving to collect steps
        progress = True
        step_num = 1

        while progress and step_num <= 10:
            progress = False
            # Check Naked Singles
            for r in range(9):
                for c in range(9):
                    if working_board[r][c] == 0:
                        cand = self.get_candidates(working_board, r, c)
                        if len(cand) == 1:
                            val = cand[0]
                            box_num = (r // 3) * 3 + (c // 3) + 1
                            step_info = {
                                "step": step_num,
                                "row": r + 1,
                                "col": c + 1,
                                "value": val,
                                "technique": "Naked Single",
                                "description": (
                                    f"Cell (Row {r + 1}, Col {c + 1}) in Box {box_num} has only one possible candidate: "
                                    f"{val}. All other digits 1-9 are eliminated by existing numbers in its row, column, or 3x3 box."
                                )
                            }
                            steps.append(step_info)
                            if first_naked_single is None:
                                first_naked_single = (r, c, val, box_num)
                            working_board[r][c] = val
                            progress = True
                            step_num += 1
                            break
                if progress:
                    break

            if not progress:
                # Check Hidden Singles in rows
                for r in range(9):
                    for num in range(1, 10):
                        possible_cols = [c for c in range(9) if working_board[r][c] == 0 and self.is_valid(working_board, r, c, num)]
                        if len(possible_cols) == 1:
                            c = possible_cols[0]
                            step_info = {
                                "step": step_num,
                                "row": r + 1,
                                "col": c + 1,
                                "value": num,
                                "technique": "Hidden Single (Row)",
                                "description": f"In Row {r + 1}, digit {num} can only fit into Column {c + 1}."
                            }
                            steps.append(step_info)
                            if first_naked_single is None:
                                first_naked_single = (r, c, num, (r // 3) * 3 + (c // 3) + 1)
                            working_board[r][c] = num
                            progress = True
                            step_num += 1
                            break
                    if progress:
                        break

        # Fallback if no easy steps found immediately
        if not first_naked_single:
            for r in range(9):
                for c in range(9):
                    if puzzle[r][c] == 0:
                        val = solution[r][c]
                        first_naked_single = (r, c, val, (r // 3) * 3 + (c // 3) + 1)
                        steps.append({
                            "step": 1,
                            "row": r + 1,
                            "col": c + 1,
                            "value": val,
                            "technique": "Constraint Elimination",
                            "description": f"Examine Row {r + 1}, Column {c + 1}: Placing {val} satisfies all row, column, and box constraints."
                        })
                        break
                if first_naked_single:
                    break

        r, c, val, box_num = first_naked_single
        hints = [
            f"Hint 1 (Area): Focus your attention on Row {r + 1} or 3x3 Box {box_num}. Notice which empty cell has the fewest remaining options.",
            f"Hint 2 (Target Cell): Look specifically at Cell (Row {r + 1}, Column {c + 1}). Check all numbers 1-9 against its row and column.",
            f"Hint 3 (Direct Deduction): The correct digit for Cell (Row {r + 1}, Column {c + 1}) is {val}."
        ]

        return hints, steps
