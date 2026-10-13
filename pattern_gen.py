"""Pattern Recognition Generator & Solver
Generates 3x3 Raven-style visual progressive matrices with geometric SVG graphics,
transformation rules (rotation, count progression, fill types, shape combinations),
progressive hints, and step-by-step visual explanations.
"""

import random
from typing import Dict, Any, List, Optional

class PatternEngine:
    def __init__(self, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)

    def _generate_svg_shape(self, shape: str, fill: str, rotation: int = 0, count: int = 1) -> str:
        """Helper to create clean SVG for a matrix cell."""
        svg_header = '<svg viewBox="0 0 100 100" class="matrix-svg" xmlns="http://www.w3.org/2000/svg">'
        svg_footer = '</svg>'
        content = ""

        # Base style
        stroke_color = "#38bdf8" # neon sky
        fill_color = "#0284c7" if fill == "solid" else ("rgba(56, 189, 248, 0.25)" if fill == "half" else "none")

        transform = f'transform="rotate({rotation} 50 50)"'

        if shape == "square":
            size = 46
            offset = 50 - size / 2
            content = f'<rect x="{offset}" y="{offset}" width="{size}" height="{size}" rx="6" stroke="{stroke_color}" stroke-width="3" fill="{fill_color}" {transform}/>'
        elif shape == "circle":
            r = 24
            content = f'<circle cx="50" cy="50" r="{r}" stroke="{stroke_color}" stroke-width="3" fill="{fill_color}" />'
        elif shape == "triangle":
            pts = "50,22 76,74 24,74"
            content = f'<polygon points="{pts}" stroke="{stroke_color}" stroke-width="3" fill="{fill_color}" {transform}/>'
        elif shape == "diamond":
            pts = "50,20 78,50 50,80 22,50"
            content = f'<polygon points="{pts}" stroke="{stroke_color}" stroke-width="3" fill="{fill_color}" {transform}/>'
        elif shape == "cross":
            content = f'<g stroke="{stroke_color}" stroke-width="4" stroke-linecap="round" {transform}><line x1="50" y1="24" x2="50" y2="76"/><line x1="24" y1="50" x2="76" y2="50"/></g>'
        elif shape == "arrow":
            content = f'<g stroke="{stroke_color}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" fill="none" {transform}><line x1="50" y1="75" x2="50" y2="25"/><polyline points="32,42 50,25 68,42"/></g>'

        # Draw dots if count > 1
        if count > 1:
            dot_color = "#f43f5e" if fill != "solid" else "#ffffff"
            dots_svg = ""
            if count == 2:
                dots_svg = f'<circle cx="40" cy="50" r="3.5" fill="{dot_color}"/><circle cx="60" cy="50" r="3.5" fill="{dot_color}"/>'
            elif count == 3:
                dots_svg = f'<circle cx="35" cy="50" r="3" fill="{dot_color}"/><circle cx="50" cy="50" r="3" fill="{dot_color}"/><circle cx="65" cy="50" r="3" fill="{dot_color}"/>'
            elif count == 4:
                dots_svg = f'<circle cx="40" cy="40" r="3" fill="{dot_color}"/><circle cx="60" cy="40" r="3" fill="{dot_color}"/><circle cx="40" cy="60" r="3" fill="{dot_color}"/><circle cx="60" cy="60" r="3" fill="{dot_color}"/>'
            elif count == 5:
                dots_svg = f'<circle cx="40" cy="40" r="3" fill="{dot_color}"/><circle cx="60" cy="40" r="3" fill="{dot_color}"/><circle cx="50" cy="50" r="3" fill="{dot_color}"/><circle cx="40" cy="60" r="3" fill="{dot_color}"/><circle cx="60" cy="60" r="3" fill="{dot_color}"/>'
            content += dots_svg

        return f'{svg_header}{content}{svg_footer}'

    def generate_rotation_matrix(self, difficulty: str) -> Dict[str, Any]:
        """Shape rotates by 90 degrees across rows and columns."""
        shape = random.choice(["arrow", "triangle", "cross"])
        base_rotation = random.choice([0, 45])
        step = 90

        grid = []
        for r in range(3):
            row_items = []
            for c in range(3):
                rot = (base_rotation + (r + c) * step) % 360
                row_items.append({
                    "shape": shape,
                    "fill": "none",
                    "rotation": rot,
                    "count": 1,
                    "svg": self._generate_svg_shape(shape, "none", rot, 1)
                })
            grid.append(row_items)

        target = grid[2][2]
        correct_svg = target["svg"]

        # Distractor options
        options_data = [
            {"label": "A", "rotation": (target["rotation"] + 90) % 360, "svg": self._generate_svg_shape(shape, "none", (target["rotation"] + 90) % 360, 1)},
            {"label": "B", "rotation": (target["rotation"] + 180) % 360, "svg": self._generate_svg_shape(shape, "none", (target["rotation"] + 180) % 360, 1)},
            {"label": "C", "rotation": target["rotation"], "svg": correct_svg, "correct": True},
            {"label": "D", "rotation": (target["rotation"] + 270) % 360, "svg": self._generate_svg_shape(shape, "none", (target["rotation"] + 270) % 360, 1)},
        ]
        random.shuffle(options_data)
        correct_label = next(opt["label"] for opt in options_data if opt.get("correct"))

        hints = [
            "Hint 1 (Motion Rule): Watch how the symbol rotates as you move from left to right along each row.",
            f"Hint 2 (Degrees): Each step to the right adds +{step}° clockwise rotation.",
            f"Hint 3 (Final Orientation): In the third row, the middle symbol is at {grid[2][1]['rotation']}°. Adding {step}° yields {target['rotation']}° (Option {correct_label})."
        ]

        steps = [
            {"step": 1, "description": f"Row 1 orientation angles: {grid[0][0]['rotation']}° -> {grid[0][1]['rotation']}° -> {grid[0][2]['rotation']}° (+{step}° per column)."},
            {"step": 2, "description": f"Row 2 orientation angles: {grid[1][0]['rotation']}° -> {grid[1][1]['rotation']}° -> {grid[1][2]['rotation']}° (+{step}° per column)."},
            {"step": 3, "description": f"Row 3 orientation angles: {grid[2][0]['rotation']}° -> {grid[2][1]['rotation']}° -> ?."},
            {"step": 4, "description": f"Applying the +{step}° rotation to {grid[2][1]['rotation']}° gives {target['rotation']}°, matching Option {correct_label}."}
        ]

        return {
            "type_name": "Rotational Symmetry Matrix",
            "grid": grid,
            "options": options_data,
            "answer": correct_label,
            "hints": hints,
            "steps": steps,
            "explanation": f"The symbol rotates {step}° clockwise with every horizontal and vertical step."
        }

    def generate_count_and_fill_matrix(self, difficulty: str) -> Dict[str, Any]:
        """Matrix where dot count increases across columns and fill changes across rows."""
        shapes = ["circle", "square", "diamond"]
        fills = ["none", "half", "solid"]

        grid = []
        for r in range(3):
            row_items = []
            for c in range(3):
                shape = shapes[r]
                fill = fills[c]
                count = c + 1
                row_items.append({
                    "shape": shape,
                    "fill": fill,
                    "rotation": 0,
                    "count": count,
                    "svg": self._generate_svg_shape(shape, fill, 0, count)
                })
            grid.append(row_items)

        target = grid[2][2]
        correct_svg = target["svg"]

        options_data = [
            {"label": "A", "svg": self._generate_svg_shape(target["shape"], "none", 0, target["count"])},
            {"label": "B", "svg": self._generate_svg_shape(target["shape"], "half", 0, target["count"] - 1)},
            {"label": "C", "svg": correct_svg, "correct": True},
            {"label": "D", "svg": self._generate_svg_shape(shapes[0], target["fill"], 0, target["count"])},
        ]
        random.shuffle(options_data)
        correct_label = next(opt["label"] for opt in options_data if opt.get("correct"))

        hints = [
            "Hint 1 (Row Rule): Look at the outer shape in each row. Row 1 = circles, Row 2 = squares, Row 3 = diamonds.",
            "Hint 2 (Column Rule): Look at the shading and dot counts. Column 1 = empty (1 dot), Column 2 = shaded (2 dots), Column 3 = solid (3 dots).",
            f"Hint 3 (Deduction): The missing cell must be a Diamond with solid fill and 3 dots, corresponding to Option {correct_label}."
        ]

        steps = [
            {"step": 1, "description": "Row-wise rule: All elements in Row 3 are Diamond shapes."},
            {"step": 2, "description": "Column-wise rule: Elements in Column 3 always have solid fill and 3 interior dots."},
            {"step": 3, "description": f"Combining both rules: Diamond + Solid Fill + 3 dots uniquely identifies Option {correct_label}."}
        ]

        return {
            "type_name": "Shape, Shading & Dot Progression",
            "grid": grid,
            "options": options_data,
            "answer": correct_label,
            "hints": hints,
            "steps": steps,
            "explanation": "Progressive matrices combine independent horizontal and vertical feature transformations."
        }

    def generate_puzzle(self, difficulty: str = "medium", seed: Optional[int] = None) -> Dict[str, Any]:
        if seed is not None:
            random.seed(seed)

        difficulty = difficulty.lower()
        if random.random() < 0.5:
            data = self.generate_rotation_matrix(difficulty)
        else:
            data = self.generate_count_and_fill_matrix(difficulty)

        # Build grid with the 9th cell as placeholder
        display_grid = []
        for r in range(3):
            row_cells = []
            for c in range(3):
                if r == 2 and c == 2:
                    row_cells.append({
                        "is_target": True,
                        "svg": '<div class="matrix-target-cell"><span class="target-question">?</span></div>'
                    })
                else:
                    row_cells.append({
                        "is_target": False,
                        "svg": data["grid"][r][c]["svg"]
                    })
            display_grid.append(row_cells)

        return {
            "id": f"pattern_{difficulty}_{random.randint(1000, 9999)}",
            "category": "pattern_recognition",
            "title": f"Pattern Recognition: {data['type_name']}",
            "difficulty": difficulty,
            "question": "Identify the missing symbol (cell ?) that logically completes the 3×3 matrix pattern.",
            "matrix_grid": display_grid,
            "options": [{"label": opt["label"], "svg": opt["svg"]} for opt in data["options"]],
            "answer": data["answer"],
            "hints": data["hints"],
            "step_by_step_solution": data["steps"],
            "explanation": data["explanation"],
            "interactive_type": "pattern_matrix"
        }
