import random

class CognitiveTaskGenerator:
    """
    Generates senior-friendly cognitive exercises (MCQ) with enhanced difficulty levels.
    """

    def __init__(self):
        self.tasks_data = []
        
        # Initialize categories (Logic removed)
        self._generate_math_tasks()
        self._generate_memory_tasks()

    def _generate_math_tasks(self):
        """
        Generates Math tasks based on the 5-level difficulty matrix and cognitive algorithms.
        """
        # ==================================================
        # LEVEL 1: Exact Change / Simple Purchase
        # Matrix: 1-2 items, Exact Change, No distractors
        # ==================================================
        items_l1 = {"Milk": 30, "Bread": 40, "Eggs": 60, "Tea": 20, "Biscuit": 10}
        for _ in range(5):
            i1, p1 = random.choice(list(items_l1.items()))
            note = 100 if p1 < 100 else 200
            change = note - p1
            
            self.tasks_data.append({
                "category": "math", "difficulty": 1,
                "question": f"You buy {i1} for ₹{p1}. You pay with a ₹{note} note. How much change do you get?",
                "answer": f"₹{change}",
                "options": [f"₹{change}", f"₹{change+10}", f"₹{change-5}", f"₹{change+5}"],
                "hint": "Subtract the price from the note."
            })

        # ==================================================
        # LEVEL 2: Simple Addition + Subtraction with Context
        # Matrix: 2-3 items, Irrelevant context ("It is raining")
        # ==================================================
        weather_context = ["It is raining heavily.", "The sun is very bright today.", "It is a windy evening."]
        for _ in range(5):
            # Select 2 items
            selection = random.sample(list(items_l1.items()), 2)
            (i1, p1), (i2, p2) = selection[0], selection[1]
            total = p1 + p2
            context = random.choice(weather_context)
            
            self.tasks_data.append({
                "category": "math", "difficulty": 2,
                "question": f"{context} You buy {i1} (₹{p1}) and {i2} (₹{p2}). What is the total bill?",
                "answer": f"₹{total}",
                "options": [f"₹{total}", f"₹{total+10}", f"₹{total-10}", f"₹{total+5}"],
                "hint": "Ignore the weather. Just add the two prices."
            })

        # ==================================================
        # LEVEL 3: Algorithm A - "Market Kid" Heuristic
        # Matrix: Decomposition, Irrelevant numbers ("Bus Route 402"), Rounding
        # ==================================================
        bus_routes = [402, 101, 55, 303]
        for _ in range(5):
            # Scenario: Bill 327. Pay 500 + 20 + 7.
            base = random.choice([100, 200, 300])
            tens = random.randint(1, 9) * 10
            units = random.choice([3, 6, 7, 8, 9]) # Non-zero/five units
            bill = base + tens + units # e.g., 327
            
            # Payment strategy: Next round note + exact coins for the units
            note_val = 500
            coins_val = units # e.g., 7
            total_paid = note_val + coins_val # 507
            
            change = total_paid - bill # 507 - 327 = 180 (Round number)
            route = random.choice(bus_routes)

            self.tasks_data.append({
                "category": "math", "difficulty": 3,
                "question": f"You take Bus Route {route} to the market. The bill is ₹{bill}. You hand the cashier a ₹{note_val} note and ₹{coins_val} in coins (Total ₹{total_paid}). How much change do you get?",
                "answer": f"₹{change}",
                "options": [f"₹{change}", f"₹{change-coins_val}", f"₹{change+7}", f"₹{change-10}"],
                "hint": f"Think: ₹{total_paid} - ₹{bill}. The ₹{coins_val} cancels out the last digit."
            })

        # ==================================================
        # LEVEL 4: Algorithm B - Inflationary Budgeting
        # Matrix: Inflation, Budgeting, Price Shocks
        # ==================================================
        market_items = [("Rice", 200), ("Oil", 150), ("Dal", 120), ("Sugar", 50), ("Spices", 80)]
        for _ in range(5):
            budget = 500
            # Create a cart near the budget limit
            cart = random.sample(market_items, 3)
            initial_total = sum(item[1] for item in cart)
            
            # Ensure scenario allows for a deficit after shock
            while initial_total > 450 or initial_total < 350:
                cart = random.sample(market_items, 3)
                initial_total = sum(item[1] for item in cart)

            # Event: Monsoon damages crop -> Price Shock
            shock_idx = 0
            shock_name, old_price = cart[shock_idx]
            rise_pct = 40 # 40% rise
            new_price = int(old_price * 1.40)
            
            new_total = initial_total - old_price + new_price
            deficit = new_total - budget
            
            # If deficit is positive, ask for extra money needed. If negative, ask for remaining.
            if deficit > 0:
                q_text = f"Your budget is ₹{budget}. Cart: {cart[0][0]}, {cart[1][0]}, {cart[2][0]} (Total ₹{initial_total}). Suddenly, monsoon rains damage the {shock_name} crop! Price rises 40% to ₹{new_price}. How much EXTRA money do you need?"
                ans = f"₹{deficit}"
                opts = [f"₹{deficit}", f"₹{deficit+10}", f"₹{deficit-5}", "₹0"]
            else:
                remaining = abs(deficit)
                q_text = f"Your budget is ₹{budget}. Cart: {cart[0][0]}, {cart[1][0]}, {cart[2][0]}. {shock_name} price rises 40% to ₹{new_price}. New Total is ₹{new_total}. How much money is left?"
                ans = f"₹{remaining}"
                opts = [f"₹{remaining}", f"₹{remaining+20}", "₹0", "Not enough"]

            self.tasks_data.append({
                "category": "math", "difficulty": 4,
                "question": q_text,
                "answer": ans,
                "options": opts,
                "hint": f"Calculate the new total first: old total - {old_price} + {new_price}."
            })

        # ==================================================
        # LEVEL 5: Algorithm C - Unit Price Optimization
        # Matrix: Optimization, Deceptive Bulk, Low absolute price lure
        # ==================================================
        products = ["Garlic", "Coffee", "Cashews", "Detergent"]
        for _ in range(5):
            prod = random.choice(products)
            
            # Option A (Standard / Best Value)
            # 1kg for ₹200 -> Unit ₹200/kg
            base_price = random.choice([200, 300, 400])
            opt_a = f"1 kg for ₹{base_price}"
            
            # Option B (Deceptive Bulk - More expensive per unit)
            # 500g for (half price + 20%) -> Unit higher
            price_b = int((base_price / 2) * 1.2)
            opt_b = f"500g for ₹{price_b}"
            
            # Option C (Small Packet - Lure: Lowest absolute cost, highest unit cost)
            # 100g for (1/10th price * 1.5)
            price_c = int((base_price / 10) * 1.5)
            opt_c = f"100g for ₹{price_c}"
            
            self.tasks_data.append({
                "category": "math", "difficulty": 5,
                "question": f"Which {prod} option offers the BEST value per kilogram? (Watch out for small packets!)\n\nA: {opt_a}\nB: {opt_b}\nC: {opt_c}",
                "answer": "Option A",
                "options": ["Option A", "Option B", "Option C", "All equal"],
                "hint": "Calculate the price for 1 kg for each. For 100g, multiply by 10."
            })

    def _generate_memory_tasks(self):
        # Dynamic Memory Tasks (Positional Recall)
        # Scaled: L1=5 digits ... L5=9 digits
        ordinals = {1:"1st", 2:"2nd", 3:"3rd", 4:"4th", 5:"5th", 6:"6th", 7:"7th", 8:"8th", 9:"9th"}
        
        for level in range(1, 6):
            num_digits = level + 4 # L1=5, L5=9
            
            for _ in range(5):
                digits = [str(random.randint(0, 9)) for _ in range(num_digits)]
                memorize_str = " - ".join(digits)
                
                target_idx = random.randint(0, num_digits - 1)
                target_pos = target_idx + 1
                correct_digit = digits[target_idx]
                
                question_text = f"Which number was {ordinals[target_pos]}?"
                
                options = {correct_digit}
                while len(options) < 4:
                    options.add(str(random.randint(0, 9)))
                
                self.tasks_data.append({
                    "category": "memory",
                    "difficulty": level,
                    "memorize_content": memorize_str,
                    "question": question_text,
                    "answer": correct_digit,
                    "options": list(options),
                    "hint": "Try visualizing the number in that specific spot."
                })

    def generate_task(self, category=None, difficulty=1, exclude_questions=None):
        if exclude_questions is None: exclude_questions = []

        filtered_tasks = [
            t for t in self.tasks_data 
            if t['difficulty'] == difficulty 
            and (category is None or t['category'] == category)
            # Use memorize_content as ID for memory tasks, otherwise question
            and (t.get('memorize_content', t['question']) not in exclude_questions)
        ]

        if not filtered_tasks:
            filtered_tasks = [
                t for t in self.tasks_data 
                if t['difficulty'] == difficulty 
                and (category is None or t['category'] == category)
            ]
        
        if not filtered_tasks:
            # Fallback
            fallback = [t for t in self.tasks_data if t['category'] == 'math' and t['difficulty'] == 1]
            return self._format_task(random.choice(fallback))
        
        selected_task = random.choice(filtered_tasks)
        return self._format_task(selected_task)

    def _format_task(self, task):
        options = task['options'].copy()
        random.shuffle(options)
        
        return {
            'question': task['question'],
            'memorize_content': task.get('memorize_content'),
            'options': options,
            'correct_answer': task['answer'],
            'category': task['category'],
            'difficulty': task['difficulty'],
            'hint': task.get('hint', 'No hint available.')
        }