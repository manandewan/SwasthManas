import random

class CognitiveTaskGenerator:
    """
    Generates senior-friendly cognitive exercises.
    Math tasks are now generated 'Live' using random variables to ensure zero repetition.
    """

    def __init__(self):
        # We still initialize memory tasks, but math is now procedural
        self.memory_tasks_data = []
        self._generate_memory_tasks()

    def _generate_math_live(self, difficulty):
        """
        Generates a random math question based on difficulty.
        """
        items = ["Apples", "Milk", "Bread", "Tea", "Coffee", "Rice", "Oil", "Soap"]
        
        if difficulty == 1:
            # Simple Subtraction (Change)
            item = random.choice(items)
            price = random.randint(3, 15) * 5 # 15 to 75
            note = random.choice([100, 200])
            correct = note - price
            return {
                "question": f"You buy {item} for ₹{price}. You pay with a ₹{note} note. What is your change?",
                "answer": f"₹{correct}",
                "options": [f"₹{correct}", f"₹{correct+5}", f"₹{correct-5}", f"₹{correct+10}"],
                "hint": "Subtract the price from the note."
            }

        elif difficulty == 2:
            # Addition of two items
            i1, i2 = random.sample(items, 2)
            p1 = random.randint(2, 10) * 10
            p2 = random.randint(2, 10) * 10
            correct = p1 + p2
            return {
                "question": f"You buy {i1} for ₹{p1} and {i2} for ₹{p2}. What is the total?",
                "answer": f"₹{correct}",
                "options": [f"₹{correct}", f"₹{correct+10}", f"₹{correct-10}", f"₹{correct+20}"],
                "hint": "Add the two prices together."
            }

        elif difficulty == 3:
            # Multiplication (Simple Quantity)
            item = random.choice(items)
            price = random.randint(15, 45)
            qty = random.randint(3, 6)
            correct = price * qty
            return {
                "question": f"One pack of {item} costs ₹{price}. How much do {qty} packs cost?",
                "answer": f"₹{correct}",
                "options": [f"₹{correct}", f"₹{correct+price}", f"₹{correct-price}", f"₹{correct+10}"],
                "hint": f"Try adding {price} to itself {qty} times."
            }

        elif difficulty == 4:
            # Two-step: Multiply and Subtract
            item = random.choice(items)
            price = random.randint(60, 120)
            qty = 2
            note = 500
            total = price * qty
            correct = note - total
            return {
                "question": f"You buy {qty} units of {item} at ₹{price} each. You pay with ₹{note}. What is the change?",
                "answer": f"₹{correct}",
                "options": [f"₹{correct}", f"₹{correct+20}", f"₹{total}", f"₹{correct-10}"],
                "hint": f"First find the total (2 x {price}), then subtract from {note}."
            }

        elif difficulty == 5:
            # LEVEL 5: Hard Multi-step Logic
            # Percentage Discount + Remaining Budget
            item = "Premium Grains"
            price = random.randint(800, 1500)
            discount_pct = random.choice([10, 20, 25])
            budget = 2000
            
            discount_amt = int(price * (discount_pct / 100))
            final_price = price - discount_amt
            remaining = budget - final_price
            
            return {
                "question": f"A sack of {item} is priced at ₹{price}. There is a {discount_pct}% discount today. If you have ₹{budget}, how much money will you have LEFT after buying it?",
                "answer": f"₹{remaining}",
                "options": [f"₹{remaining}", f"₹{final_price}", f"₹{remaining-50}", f"₹{remaining+100}"],
                "hint": f"1. Find the discount. 2. Subtract it from {price}. 3. Subtract that from {budget}."
            }

    def _generate_memory_tasks(self):
        # We keep the memory generation as is, but generate a large batch
        ordinals = {1:"1st", 2:"2nd", 3:"3rd", 4:"4th", 5:"5th", 6:"6th", 7:"7th", 8:"8th", 9:"9th"}
        for level in range(1, 6):
            num_digits = level + 4
            for _ in range(100):
                digits = [str(random.randint(0, 9)) for _ in range(num_digits)]
                mem_str = " - ".join(digits)
                idx = random.randint(0, num_digits - 1)
                self.memory_tasks_data.append({
                    "category": "memory", "difficulty": level,
                    "memorize_content": mem_str,
                    "question": f"Which number was {ordinals[idx+1]}?",
                    "answer": digits[idx],
                    "options": list(set([digits[idx], str(random.randint(0,9)), str(random.randint(0,9)), str(random.randint(0,9))])),
                    "hint": "Try to group the numbers in your head."
                })

    def generate_task(self, category=None, difficulty=1, exclude_questions=None):
        if category == "math":
            raw_task = self._generate_math_live(difficulty)
        else:
            # Memory still uses the pool but it's large (500 tasks total)
            pool = [t for t in self.memory_tasks_data if t['difficulty'] == difficulty]
            raw_task = random.choice(pool)

        # Ensure 4 options
        opts = raw_task['options']
        while len(opts) < 4:
            opts.append(str(random.randint(10, 100)))
        random.shuffle(opts)

        return {
            'question': raw_task['question'],
            'memorize_content': raw_task.get('memorize_content'),
            'options': opts,
            'correct_answer': raw_task['answer'],
            'category': category,
            'difficulty': difficulty,
            'hint': raw_task.get('hint')
        }