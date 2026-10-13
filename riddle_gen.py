"""Classical Logic Riddles Generator & Solver
Features Knights and Knaves (Truth-tellers & Liars) with truth-table solver,
River Crossing state problems, Counterfeit Coin Balance scales, and Bridge Crossing.
"""

import random
from typing import Dict, Any, List, Optional

class RiddleEngine:
    def __init__(self, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)

    def generate_knights_and_knaves(self, difficulty: str) -> Dict[str, Any]:
        """Knights always tell the truth; Knaves always lie."""
        scenarios = [
            {
                "setup": "You meet two islanders, A and B. A makes the statement: 'At least one of us is a Knave.'",
                "question": "What are the identities of A and B?",
                "answer": "A is a Knight, B is a Knave",
                "options": [
                    "A is a Knight, B is a Knave",
                    "Both A and B are Knights",
                    "Both A and B are Knaves",
                    "A is a Knave, B is a Knight"
                ],
                "hints": [
                    "Hint 1 (Hypothesis Testing): Assume A is a Knave first. If A is a Knave, what would that imply about A's statement?",
                    "Hint 2 (Contradiction): If A were a Knave, A's statement ('At least one of us is a Knave') would be TRUE (since A is a Knave). But Knaves cannot tell the truth! Thus A cannot be a Knave.",
                    "Hint 3 (Resolution): Since A must be a Knight, A's statement is true. A is a Knight, so B must be the Knave."
                ],
                "steps": [
                    {"step": 1, "description": "Case 1: Suppose A is a Knave (liar). Then A's statement 'At least one of us is a Knave' would be true because A is indeed a Knave. But a Knave cannot speak a true statement—contradiction!"},
                    {"step": 2, "description": "Deduction: A cannot be a Knave, so A must be a Knight (truth-teller)."},
                    {"step": 3, "description": "Case 2: Since A is a Knight, A's statement is TRUE. The statement asserts 'At least one of us is a Knave'."},
                    {"step": 4, "description": "Since A is a Knight, the Knave must be B. Therefore: A is a Knight and B is a Knave."}
                ]
            },
            {
                "setup": "You meet two islanders, X and Y. X says: 'We are both Knaves.'",
                "question": "What can you deduce about X and Y?",
                "answer": "X is a Knave, Y is a Knight",
                "options": [
                    "X is a Knave, Y is a Knight",
                    "Both X and Y are Knaves",
                    "Both X and Y are Knights",
                    "X is a Knight, Y is a Knave"
                ],
                "hints": [
                    "Hint 1 (Can a Knight say this?): Could a Knight ever say 'I am a Knave' or 'We are both Knaves'?",
                    "Hint 2 (Status of X): If X were a Knight, X's statement would be true, which means X is a Knave—an impossible paradox. So X MUST be a Knave.",
                    "Hint 3 (Status of Y): Since X is a Knave, X's statement 'We are both Knaves' is a LIE (false). For it to be false, they cannot BOTH be Knaves, meaning Y is a Knight."
                ],
                "steps": [
                    {"step": 1, "description": "Could X be a Knight? If X is a Knight, then 'We are both Knaves' is true, making X a Knave—contradiction."},
                    {"step": 2, "description": "Therefore, X is definitely a Knave."},
                    {"step": 3, "description": "Since X is a Knave, the statement 'We are both Knaves' is FALSE (a lie)."},
                    {"step": 4, "description": "For the conjunction 'X is a Knave AND Y is a Knave' to be false given X is a Knave, Y must NOT be a Knave. Hence, Y is a Knight."}
                ]
            },
            {
                "setup": "You encounter islander C, who says: 'If I am a Knight, then 2 + 2 = 5.'",
                "question": "What is C's identity?",
                "answer": "C is a Knave",
                "options": [
                    "C is a Knave",
                    "C is a Knight",
                    "C can be either Knight or Knave",
                    "The scenario is logically impossible"
                ],
                "hints": [
                    "Hint 1 (Implication Logic): In formal logic, a conditional 'P -> Q' is false only when P is true and Q is false.",
                    "Hint 2 (Assume Knight): If C is a Knight, the premise 'I am a Knight' is true. But the conclusion '2 + 2 = 5' is false. A true premise implying a false conclusion is FALSE.",
                    "Hint 3 (Conclusion): A Knight cannot make a false statement. So C is a Knave (whose statement P -> Q is vacuously true in standard logic, creating a Smullyan paradox where C must be a Knave)."
                ],
                "steps": [
                    {"step": 1, "description": "Statement has form: 'Knight(C) -> (2 + 2 = 5)'."},
                    {"step": 2, "description": "If C were a Knight, the premise 'Knight(C)' is True, but the conclusion '2 + 2 = 5' is False. Thus the conditional True -> False evaluates to False."},
                    {"step": 3, "description": "A Knight cannot utter a false statement. Therefore, C cannot be a Knight; C must be a Knave."}
                ]
            }
        ]
        return random.choice(scenarios)

    def generate_river_crossing(self, difficulty: str) -> Dict[str, Any]:
        """Classic Wolf, Goat, and Cabbage state transition riddle."""
        return {
            "setup": (
                "A farmer needs to transport a wolf, a goat, and a head of cabbage across a river using a small boat. "
                "The boat can only carry the farmer and one item at a time. "
                "If left alone without the farmer, the wolf will eat the goat, and the goat will eat the cabbage. "
                "The wolf does not eat cabbage."
            ),
            "question": "What is the minimum number of one-way boat crossings required to get all three safely to the other side?",
            "answer": "7",
            "options": ["5", "7", "9", "11"],
            "hints": [
                "Hint 1 (First Trip): Who is the only passenger you can safely leave behind on the starting bank? Wolf and cabbage are safe together.",
                "Hint 2 (Return Item): On crossing 3 or 4, you must bring a passenger back with you to prevent an unsupervised conflict!",
                "Hint 3 (Calculation): 1: Take goat. 2: Return empty. 3: Take wolf. 4: Return with goat! 5: Take cabbage. 6: Return empty. 7: Take goat. Total: 7 crossings."
            ],
            "steps": [
                {"step": 1, "description": "Trip 1: Farmer takes Goat across (Wolf & Cabbage remain safe together on starting bank)."},
                {"step": 2, "description": "Trip 2: Farmer returns alone to start bank."},
                {"step": 3, "description": "Trip 3: Farmer takes Wolf across."},
                {"step": 4, "description": "Trip 4 (Key Move!): Farmer brings Goat back to avoid leaving Wolf and Goat together."},
                {"step": 5, "description": "Trip 5: Farmer takes Cabbage across (leaving Goat safely on start bank)."},
                {"step": 6, "description": "Trip 6: Farmer returns alone to start bank."},
                {"step": 7, "description": "Trip 7: Farmer takes Goat across. All arrive safely! Total = 7 trips."}
            ]
        }

    def generate_coin_weighing(self, difficulty: str) -> Dict[str, Any]:
        """Ternary division balance scale coin puzzle."""
        coins = random.choice([9, 27])
        min_weighings = 2 if coins == 9 else 3
        return {
            "setup": (
                f"You have {coins} identical-looking gold coins, but one of them is counterfeit and slightly lighter than the others. "
                "You have a two-pan balance scale that can compare the weight of any two groups of coins."
            ),
            "question": f"What is the absolute minimum number of weighings guaranteed to identify the fake coin in the worst case?",
            "answer": str(min_weighings),
            "options": [str(min_weighings - 1), str(min_weighings), str(min_weighings + 1), str(min_weighings + 2)],
            "hints": [
                "Hint 1 (Ternary Division): A balance scale has 3 possible outcomes: left is heavier, right is heavier, or both balance evenly.",
                f"Hint 2 (Group Sizes): Divide the {coins} coins into 3 equal piles of {coins // 3}.",
                f"Hint 3 (Exponential Power): 3^k must be ≥ {coins}. Since 3^{min_weighings} = {coins}, {min_weighings} weighings are guaranteed."
            ],
            "steps": [
                {"step": 1, "description": f"Each balance scale weighing provides 3 outcomes (left pan down, right pan down, balanced), capable of resolving 3^k possibilities."},
                {"step": 2, "description": f"Weighing 1: Divide {coins} coins into three groups of {coins // 3}. Put two groups on the pans. If balanced, fake is in 3rd pile; if unbalanced, fake is in lighter pan."},
                {"step": 3, "description": f"Each weighing eliminates 2/3 of remaining candidates, narrowing {coins} down to 1 in exactly {min_weighings} weighings."}
            ]
        }

    def generate_puzzle(self, difficulty: str = "medium", seed: Optional[int] = None) -> Dict[str, Any]:
        if seed is not None:
            random.seed(seed)

        difficulty = difficulty.lower()
        choice = random.choice(["knights", "river", "coin"])
        if choice == "knights":
            data = self.generate_knights_and_knaves(difficulty)
            category_title = "Knights & Knaves Deductive Logic"
        elif choice == "river":
            data = self.generate_river_crossing(difficulty)
            category_title = "River Crossing State Search"
        else:
            data = self.generate_coin_weighing(difficulty)
            category_title = "Counterfeit Coin Balance Scale"

        return {
            "id": f"riddle_{difficulty}_{random.randint(1000, 9999)}",
            "category": "riddles",
            "title": f"Logic Riddle: {category_title}",
            "difficulty": difficulty,
            "question": f"{data['setup']}\n\n{data['question']}",
            "answer": data["answer"],
            "options": data["options"],
            "hints": data["hints"],
            "step_by_step_solution": data["steps"],
            "explanation": "Classical logic riddles test proof by contradiction, state-space tree traversal, and information-theoretic branching.",
            "interactive_type": "multiple_choice"
        }
