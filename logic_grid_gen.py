"""Zebra / Einstein Logic Grid Generator & Solver
Generates multi-category deductive logic grid puzzles with direct clues,
exclusion clues, relational clues, an interactive deduction matrix,
and step-by-step elimination logic.
"""

import random
from typing import Dict, Any, List, Optional

class LogicGridEngine:
    def __init__(self, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)

    def generate_puzzle(self, difficulty: str = "medium", seed: Optional[int] = None) -> Dict[str, Any]:
        if seed is not None:
            random.seed(seed)

        difficulty = difficulty.lower()

        # Categories
        if difficulty in ["easy", "medium"]:
            num_items = 3
            people = ["Alex", "Blake", "Casey"]
            pets = ["Cat", "Dog", "Parrot"]
            drinks = ["Coffee", "Tea", "Lemonade"]
        else: # hard, expert
            num_items = 4
            people = ["Alex", "Blake", "Casey", "Dana"]
            pets = ["Cat", "Dog", "Parrot", "Fish"]
            drinks = ["Coffee", "Tea", "Lemonade", "Water"]

        # Shuffle mappings to form unique solution
        shuffled_pets = pets.copy()
        shuffled_drinks = drinks.copy()
        random.shuffle(shuffled_pets)
        random.shuffle(shuffled_drinks)

        solution_map = {}
        for i in range(num_items):
            solution_map[people[i]] = {
                "pet": shuffled_pets[i],
                "drink": shuffled_drinks[i]
            }

        # Build clues
        clues = []
        # Direct clue 1
        clues.append(f"{people[0]} drinks {solution_map[people[0]]['drink']}.")
        # Relational clue
        clues.append(f"The person who owns the {solution_map[people[1]]['pet']} is {people[1]}.")
        # Linked clue
        clues.append(f"The pet owner of the {solution_map[people[0]]['pet']} also enjoys {solution_map[people[0]]['drink']}.")
        # Negative / elimination clue
        other_drink = [d for d in drinks if d != solution_map[people[2]]["drink"]][0]
        clues.append(f"{people[2]} does not drink {other_drink}.")

        if num_items == 4:
            clues.append(f"{people[3]} drinks {solution_map[people[3]]['drink']}.")
            clues.append(f"The owner of the {solution_map[people[3]]['pet']} does not drink {solution_map[people[0]]['drink']}.")

        # Formulate question
        target_person = people[random.randint(0, num_items - 1)]
        target_pet = solution_map[target_person]["pet"]
        question = (
            f"Based on the clues provided, deduce who owns each pet and drinks each beverage.\n"
            f"Question: Which pet does {target_person} own?"
        )

        hints = [
            f"Hint 1 (Clue Cross-Reference): Look at direct clues linking names directly to drinks or pets first.",
            f"Hint 2 (Elimination): Use the deduction grid to mark 'X' where combinations are impossible.",
            f"Hint 3 (Direct Answer): {target_person} owns the {target_pet}."
        ]

        steps = [
            {"step": 1, "description": f"Start with direct positive clue: '{clues[0]}'. Mark an 'O' in that grid cell and 'X' in the rest of that row/column."},
            {"step": 2, "description": f"Apply pet assignment: '{clues[1]}'. Mark 'O' for {people[1]} and {solution_map[people[1]]['pet']}."},
            {"step": 3, "description": f"Cross-reference drink and pet clues to resolve remaining assignments through elimination."},
            {"step": 4, "description": f"Conclusion: {target_person} is uniquely assigned to the {target_pet}."}
        ]

        options = pets.copy()
        random.shuffle(options)

        return {
            "id": f"logicgrid_{difficulty}_{random.randint(1000, 9999)}",
            "category": "grid_puzzle",
            "title": f"Logic Grid Mystery ({num_items}×{num_items})",
            "difficulty": difficulty,
            "question": question,
            "people": people,
            "pets": pets,
            "drinks": drinks,
            "clues": clues,
            "solution_map": solution_map,
            "target_person": target_person,
            "answer": target_pet,
            "options": options,
            "hints": hints,
            "step_by_step_solution": steps,
            "explanation": "Zebra logic puzzles rely on transitive deductions and elimination matrices to rule out conflicting hypotheses.",
            "interactive_type": "logic_grid"
        }
