"""Brain Teasers & Critical Deductions Generator & Solver
Generates clock angle puzzles, Monty Hall probability paradoxes,
irregular fuse ropes timing, and water jug measuring problems with rigorous explanations.
"""

import random
from typing import Dict, Any, List, Optional

class BrainTeaserEngine:
    def __init__(self, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)

    def generate_clock_angle(self, difficulty: str) -> Dict[str, Any]:
        times = [
            (3, 15, 7.5),
            (8, 20, 130),
            (2, 40, 160),
            (9, 30, 105),
            (4, 50, 155),
            (1, 20, 80)
        ]
        h, m, expected_angle = random.choice(times)

        question = (
            f"At {h}:{m:02d} on a standard 12-hour analog clock, what is the acute angle (in degrees) "
            "between the hour hand and the minute hand?"
        )
        answer = f"{expected_angle}°"

        # Distractor options
        distractors = [
            f"{abs(expected_angle - 7.5):.1f}°".rstrip('.0') + "°",
            f"{expected_angle + 15:.1f}".rstrip('.0') + "°",
            f"{abs(30 * h - 6 * m)}°"
        ]
        options = list(set([answer] + distractors))
        while len(options) < 4:
            options.append(f"{random.randint(10, 170)}°")
        random.shuffle(options)

        hints = [
            "Hint 1 (Hour Hand Drift): Don't forget that the hour hand doesn't stay stationary on the number; it creeps forward as minutes pass!",
            f"Hint 2 (Rates of Movement): The minute hand moves 6° per minute. The hour hand moves 0.5° per minute (30° per hour).",
            f"Hint 3 (Formula): θ = |30×H - 5.5×M| = |30×{h} - 5.5×{m}| = {expected_angle}°."
        ]

        steps = [
            {"step": 1, "description": f"Calculate minute hand position: {m} min × 6°/min = {m * 6}° from the 12 o'clock mark."},
            {"step": 2, "description": f"Calculate hour hand position: {h} hours × 30°/hr + {m} min × 0.5°/min = {h * 30 + m * 0.5}°."},
            {"step": 3, "description": f"Find absolute difference: |{h * 30 + m * 0.5}° - {m * 6}°| = {expected_angle}°."}
        ]

        return {
            "type_name": "Analog Clock Hand Geometry",
            "question": question,
            "answer": answer,
            "options": options,
            "hints": hints,
            "steps": steps,
            "explanation": "Because the hour hand advances 0.5 degrees every minute, the hands are rarely aligned directly on hour ticks."
        }

    def generate_monty_hall(self, difficulty: str) -> Dict[str, Any]:
        return {
            "type_name": "Monty Hall Probability Paradox",
            "question": (
                "You are on a game show with 3 closed doors. Behind one door is a luxury car; behind the other two are goats. "
                "You pick Door 1. The host (who knows what is behind every door) opens Door 3, revealing a goat. "
                "He then asks: 'Do you want to switch to Door 2?' What is your probability of winning if you switch?"
            ),
            "answer": "2/3 (approx 66.7%)",
            "options": [
                "2/3 (approx 66.7%)",
                "1/2 (50%)",
                "1/3 (approx 33.3%)",
                "3/4 (75%)"
            ],
            "hints": [
                "Hint 1 (Initial Probability): When you made your initial choice, what was the chance your chosen door contained the car?",
                "Hint 2 (Information Transfer): The host will ALWAYS reveal a goat. He cannot pick your door, and he cannot reveal the car.",
                "Hint 3 (Bayesian Updating): Your initial door still only has a 1/3 probability of being correct. The remaining 2/3 probability shifts entirely to the unopened remaining door!"
            ],
            "steps": [
                {"step": 1, "description": "Prior probability: Probability(Door 1 has car) = 1/3. Probability(Car is behind Door 2 or 3) = 2/3."},
                {"step": 2, "description": "The host filters out the goat among the unchosen doors by opening Door 3."},
                {"step": 3, "description": "Because the host's action is constrained, the entire 2/3 probability of the unchosen set collapses onto Door 2."},
                {"step": 4, "description": "Switching yields the car 2 out of 3 times (66.7% win rate), whereas staying only wins 1 out of 3 times."}
            ],
            "explanation": "Conditional probability shifts the weight of unchosen outcomes onto the remaining door once a non-car door is revealed."
        }

    def generate_rope_timer(self, difficulty: str) -> Dict[str, Any]:
        return {
            "type_name": "Irregular Burning Fuse Timing",
            "question": (
                "You have two ropes. Each rope takes exactly 60 minutes to burn from one end to the other, "
                "but neither rope burns at a uniform rate (e.g., half the rope might burn in 10 minutes). "
                "Using only these two ropes and a lighter, how can you measure exactly 45 minutes?"
            ),
            "answer": "Light Rope 1 at both ends and Rope 2 at one end; when Rope 1 finishes (30 min), light the other end of Rope 2 (15 min)",
            "options": [
                "Light Rope 1 at both ends and Rope 2 at one end; when Rope 1 finishes (30 min), light the other end of Rope 2 (15 min)",
                "Light both ropes at one end and extinguish one when half-burned",
                "Cut both ropes in half and burn three halves sequentially",
                "Light Rope 1 at both ends, wait until it finishes, then light Rope 2 at both ends"
            ],
            "hints": [
                "Hint 1 (Dual-End Burning): If a 60-minute rope is lit at both ends simultaneously, how long does it take for the two flames to meet and consume it completely?",
                "Hint 2 (30 Minutes): Lighting both ends of a rope cuts its burn duration to exactly 30 minutes, regardless of non-uniform burn rate!",
                "Hint 3 (Remaining 15 Minutes): At the 30-minute mark, the second rope has 30 minutes of fuel left. If you immediately ignite its other end, it will burn out in 15 minutes: 30 + 15 = 45 minutes."
            ],
            "steps": [
                {"step": 1, "description": "Simultaneously light Rope A at BOTH ends, and Rope B at ONE end at t = 0."},
                {"step": 2, "description": "Because Rope A is burning from both sides, the flames meet at t = 30 minutes, completely consuming Rope A."},
                {"step": 3, "description": "At t = 30 minutes, Rope B has exactly 30 minutes of burn time left. Immediately ignite the second end of Rope B."},
                {"step": 4, "description": "Rope B will burn out in 30 / 2 = 15 minutes. Total elapsed time = 30 + 15 = 45 minutes."}
            ],
            "explanation": "Igniting both ends of an irregularly burning fuse doubles the rate of consumption, halving the total duration."
        }

    def generate_puzzle(self, difficulty: str = "medium", seed: Optional[int] = None) -> Dict[str, Any]:
        if seed is not None:
            random.seed(seed)

        difficulty = difficulty.lower()
        choice = random.choice(["clock", "monty", "rope"])
        if choice == "clock":
            data = self.generate_clock_angle(difficulty)
        elif choice == "monty":
            data = self.generate_monty_hall(difficulty)
        else:
            data = self.generate_rope_timer(difficulty)

        return {
            "id": f"teaser_{difficulty}_{random.randint(1000, 9999)}",
            "category": "brain_teasers",
            "title": f"Brain Teaser: {data['type_name']}",
            "difficulty": difficulty,
            "question": data["question"],
            "answer": data["answer"],
            "options": data["options"],
            "hints": data["hints"],
            "step_by_step_solution": data["steps"],
            "explanation": data["explanation"],
            "interactive_type": "multiple_choice"
        }
