"""Number Sequence Generator & Solver
Generates arithmetic, geometric, polynomial/quadratic, Fibonacci/recurrence,
and interleaved sequences with full difference tables, formulas, and progressive hints.
"""

import random
from typing import Dict, Any, List, Optional

class SequenceEngine:
    def __init__(self, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)

    def generate_arithmetic(self, difficulty: str) -> Dict[str, Any]:
        if difficulty == "easy":
            start = random.randint(1, 20)
            diff = random.choice([2, 3, 4, 5, 6, 7, 8, 10])
        elif difficulty == "medium":
            start = random.randint(20, 100)
            diff = random.choice([-9, -7, -6, -4, -3, 11, 12, 13, 15])
        elif difficulty == "hard":
            start = random.randint(50, 200)
            diff = random.choice([-17, -13, -11, 14, 16, 17, 19, 23])
        else: # expert
            start = random.randint(100, 500)
            diff = random.choice([-37, -29, -23, 27, 31, 37, 43])

        length = 6
        terms = [start + i * diff for i in range(length)]
        answer = terms[-1]
        display_terms = terms[:-1] + ["?"]

        diff_table = [terms[i+1] - terms[i] for i in range(length - 2)]

        hints = [
            "Hint 1 (Pattern Type): Calculate the difference between consecutive terms. Is the step constant?",
            f"Hint 2 (Common Difference): The difference between adjacent terms is constant: {diff}.",
            f"Hint 3 (Calculation): Add {diff} to the preceding term ({terms[-2]}): {terms[-2]} + ({diff}) = {answer}."
        ]

        steps = [
            {"step": 1, "description": f"Calculate consecutive differences: {terms[1]} - {terms[0]} = {diff}, {terms[2]} - {terms[1]} = {diff}."},
            {"step": 2, "description": f"This is an Arithmetic Progression with common difference d = {diff}."},
            {"step": 3, "description": f"Formula: a_n = a_1 + (n - 1) * d = {start} + (n - 1) * {diff}."},
            {"step": 4, "description": f"Calculate term {length}: {terms[-2]} + ({diff}) = {answer}."}
        ]

        return {
            "type_name": "Arithmetic Progression",
            "terms": display_terms,
            "answer": answer,
            "formula": f"a_n = {start} + (n - 1) × ({diff})",
            "hints": hints,
            "steps": steps,
            "explanation": f"An arithmetic sequence increases/decreases by a constant amount ({diff}) each step."
        }

    def generate_geometric(self, difficulty: str) -> Dict[str, Any]:
        if difficulty in ["easy", "medium"]:
            start = random.choice([2, 3, 4, 5])
            ratio = random.choice([2, 3])
            length = 5
        else:
            start = random.choice([1, 2, 3, -2])
            ratio = random.choice([-2, -3, 4, 5])
            length = 5

        terms = [start * (ratio ** i) for i in range(length)]
        answer = terms[-1]
        display_terms = terms[:-1] + ["?"]

        hints = [
            "Hint 1 (Growth Rate): The numbers are expanding rapidly. Look at the ratio between consecutive terms.",
            f"Hint 2 (Common Ratio): Each term is multiplied by a common ratio of {ratio}.",
            f"Hint 3 (Calculation): Multiply {terms[-2]} by {ratio}: {terms[-2]} × {ratio} = {answer}."
        ]

        steps = [
            {"step": 1, "description": f"Divide consecutive terms: {terms[1]} / {terms[0]} = {ratio}, {terms[2]} / {terms[1]} = {ratio}."},
            {"step": 2, "description": f"This is a Geometric Progression with common ratio r = {ratio}."},
            {"step": 3, "description": f"Formula: a_n = a_1 × r^(n-1) = {start} × ({ratio})^(n-1)."},
            {"step": 4, "description": f"Calculate term {length}: {terms[-2]} × {ratio} = {answer}."}
        ]

        return {
            "type_name": "Geometric Progression",
            "terms": display_terms,
            "answer": answer,
            "formula": f"a_n = {start} × ({ratio})^(n-1)",
            "hints": hints,
            "steps": steps,
            "explanation": f"A geometric sequence multiplies each preceding term by a constant ratio ({ratio})."
        }

    def generate_quadratic(self, difficulty: str) -> Dict[str, Any]:
        # a*n^2 + b*n + c
        if difficulty in ["easy", "medium"]:
            a = random.choice([1, 2])
            b = random.randint(0, 3)
            c = random.randint(1, 10)
        else:
            a = random.choice([2, 3, -1])
            b = random.randint(-2, 5)
            c = random.randint(5, 25)

        length = 6
        terms = [a * (n**2) + b * n + c for n in range(1, length + 1)]
        answer = terms[-1]
        display_terms = terms[:-1] + ["?"]

        first_diffs = [terms[i+1] - terms[i] for i in range(length - 1)]
        second_diff = 2 * a

        hints = [
            "Hint 1 (Differences): The first differences between terms are not constant. Calculate the second differences (differences of differences).",
            f"Hint 2 (Second Difference): The first differences are {first_diffs[:3]}... Notice that the second difference is constant at {second_diff}.",
            f"Hint 3 (Calculation): The next first difference must be {first_diffs[-2] + second_diff}. Add this to {terms[-2]}: {terms[-2]} + {first_diffs[-1]} = {answer}."
        ]

        steps = [
            {"step": 1, "description": f"First differences (Δ1): {', '.join(str(d) for d in first_diffs[:-1])}."},
            {"step": 2, "description": f"Second differences (Δ2): Constant value of {second_diff}."},
            {"step": 3, "description": f"Since Δ2 is constant, the sequence is quadratic: a_n = {a}n² + {b}n + {c}."},
            {"step": 4, "description": f"Next first difference is {first_diffs[-2]} + {second_diff} = {first_diffs[-1]}."},
            {"step": 5, "description": f"Next term = {terms[-2]} + {first_diffs[-1]} = {answer}."}
        ]

        return {
            "type_name": "Quadratic / Polynomial Sequence",
            "terms": display_terms,
            "answer": answer,
            "formula": f"a_n = {a}n² + {b}n + {c}",
            "hints": hints,
            "steps": steps,
            "explanation": f"A sequence whose second differences are constant ({second_diff}) follows a quadratic polynomial."
        }

    def generate_fibonacci_type(self, difficulty: str) -> Dict[str, Any]:
        if difficulty == "easy":
            # Classic Fibonacci
            terms = [1, 1, 2, 3, 5, 8, 13]
            answer = 21
            formula = "a_n = a_(n-1) + a_(n-2)"
            name = "Fibonacci Sequence"
        elif difficulty == "medium":
            # Lucas sequence
            terms = [2, 1, 3, 4, 7, 11, 18]
            answer = 29
            formula = "L_n = L_(n-1) + L_(n-2)"
            name = "Lucas Sequence"
        else: # hard / expert
            # Weighted recurrence: a_n = 2*a_(n-1) + a_(n-2) (Pell numbers)
            terms = [0, 1, 2, 5, 12, 29]
            answer = 70
            formula = "P_n = 2×P_(n-1) + P_(n-2)"
            name = "Pell Recurrence Sequence"

        display_terms = terms + ["?"]

        hints = [
            "Hint 1 (Additive Recurrence): Each term is formed by combining the previous two terms.",
            f"Hint 2 (Formula): Look at {terms[-2]} and {terms[-1]}. Notice how they produce the next value.",
            f"Hint 3 (Calculation): Apply the recurrence rule to {terms[-2]} and {terms[-1]} to get {answer}."
        ]

        steps = [
            {"step": 1, "description": f"Examine early terms: {terms[2]} = {terms[1]} + {terms[0]} (or weighted relation)."},
            {"step": 2, "description": f"Recognize recurrence relation: {formula}."},
            {"step": 3, "description": f"Calculate the next term using the last two values: {answer}."}
        ]

        return {
            "type_name": name,
            "terms": display_terms,
            "answer": answer,
            "formula": formula,
            "hints": hints,
            "steps": steps,
            "explanation": "Recurrence sequences derive each new term by mathematically combining preceding terms."
        }

    def generate_interleaved(self, difficulty: str) -> Dict[str, Any]:
        # Two interleaved sequences
        # Seq 1: odd indices
        # Seq 2: even indices
        step1 = random.choice([2, 3, 4, 5])
        mult2 = random.choice([2, 3])
        s1 = [random.randint(1, 10) + i * step1 for i in range(4)]
        s2 = [random.choice([2, 3]) * (mult2 ** i) for i in range(4)]

        interleaved = []
        for i in range(4):
            interleaved.append(s1[i])
            interleaved.append(s2[i])

        # Ask for the 8th term (index 7, which belongs to s2)
        answer = interleaved[-1]
        display_terms = interleaved[:-1] + ["?"]

        hints = [
            "Hint 1 (Dual Patterns): Look at every alternate number (terms 1, 3, 5 and terms 2, 4, 6).",
            f"Hint 2 (Sub-sequences): Odd positions follow +{step1} ({s1[0]}, {s1[1]}, {s1[2]}...). Even positions follow ×{mult2} ({s2[0]}, {s2[1]}, {s2[2]}...).",
            f"Hint 3 (Target Calculation): The missing term is in an even position. Multiply the previous even term ({s2[-2]}) by {mult2} = {answer}."
        ]

        steps = [
            {"step": 1, "description": "Check if single difference/ratio works: Differences oscillate erratically, indicating interleaved sequences."},
            {"step": 2, "description": f"Separate odd indices: {s1[0]}, {s1[1]}, {s1[2]}, {s1[3]} (Arithmetic +{step1})."},
            {"step": 3, "description": f"Separate even indices: {s2[0]}, {s2[1]}, {s2[2]}, ... (Geometric ×{mult2})."},
            {"step": 4, "description": f"The missing term '?' is the 4th term of the geometric sub-sequence: {s2[-2]} × {mult2} = {answer}."}
        ]

        return {
            "type_name": "Interleaved Alternating Sequence",
            "terms": display_terms,
            "answer": answer,
            "formula": "Alternating AP(+step) and GP(×ratio)",
            "hints": hints,
            "steps": steps,
            "explanation": "Two distinct mathematical sequences are woven into alternate positions."
        }

    def generate_puzzle(self, difficulty: str = "medium", seed: Optional[int] = None) -> Dict[str, Any]:
        if seed is not None:
            random.seed(seed)

        difficulty = difficulty.lower()

        if difficulty == "easy":
            generators = [self.generate_arithmetic, self.generate_geometric, self.generate_fibonacci_type]
        elif difficulty == "medium":
            generators = [self.generate_arithmetic, self.generate_quadratic, self.generate_geometric, self.generate_fibonacci_type]
        elif difficulty == "hard":
            generators = [self.generate_quadratic, self.generate_interleaved, self.generate_fibonacci_type]
        else: # expert
            generators = [self.generate_quadratic, self.generate_interleaved, self.generate_fibonacci_type, self.generate_arithmetic]

        generator = random.choice(generators)
        data = generator(difficulty)

        answer = data["answer"]
        # Generate 3 plausible distractors for multiple choice
        distractors = set()
        distractors.add(answer + random.choice([1, 2, -1, -2, 3, -3]))
        distractors.add(answer + random.choice([5, 10, -5, -10]))
        distractors.add(answer * 2 if answer != 0 else 4)
        distractors.discard(answer)
        while len(distractors) < 3:
            cand = answer + random.randint(-15, 15)
            if cand != answer:
                distractors.add(cand)

        options = list(distractors)[:3] + [answer]
        random.shuffle(options)

        return {
            "id": f"sequence_{difficulty}_{random.randint(1000, 9999)}",
            "category": "number_sequence",
            "title": f"Number Sequence: {data['type_name']}",
            "difficulty": difficulty,
            "question": f"Find the missing number in the sequence:\n{', '.join(str(x) for x in data['terms'])}",
            "terms": data["terms"],
            "answer": answer,
            "options": options,
            "formula": data["formula"],
            "hints": data["hints"],
            "step_by_step_solution": data["steps"],
            "explanation": data["explanation"],
            "interactive_type": "number_sequence"
        }
