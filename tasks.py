import random

class CognitiveTaskGenerator:
    """
    Generates senior-friendly cognitive exercises (MCQ) with enhanced difficulty levels.
    Now generates 50+ unique variations per level to prevent repetition.
    """

    def __init__(self):
        self.tasks_data = []
        
        # Initialize categories
        self._generate_math_tasks()
        self._generate_memory_tasks()

    def _generate_math_tasks(self):
        """
        Generates Math tasks with randomized numbers to ensure variety.
        """
        # Common Items for variety
        grocery_items = ["Milk", "Bread", "Eggs", "Tea", "Biscuits", "Curd", "Butter", "Cheese"]
        
        # ==================================================
        # LEVEL 1: Exact Change / Simple Purchase
        # ==================================================
        for _ in range(50): # Increased from 5 to 50
            item = random.choice(grocery_items)
            # Random price between 20 and 90 (multiples of 5)
            price = random.randint(4, 18) * 5 
            
            # Note is either 100, 200, or 500
            note = random.choice([100, 200, 500])
            while note < price: 
                note = 500 # Ensure note covers price
                
            change = note - price
            
            # Generate wrong options (close to correct answer)
            wrong1 = change + 10
            wrong2 = change - 5
            wrong3 = change + 5
            
            self.tasks_data.append({
                "category": "math", "difficulty": 1,
                "question": f"You buy {item} for ₹{price}. You pay with a ₹{note} note. How much change do you get?",
                "answer": f"₹{change}",
                "options": [f"₹{change}", f"₹{wrong1}", f"₹{wrong2}", f"₹{wrong3}"],
                "hint": "Subtract the price from the note."
            })

        # ==================================================
        # LEVEL 2: Simple Addition + Subtraction with Context
        # ==================================================
        weather_context = ["It is raining heavily.", "The sun is very bright today.", "It is a windy evening.", "There is a lot of traffic."]
        for _ in range(50):
            # Select 2 random items and random prices
            i1, i2 = random.sample(grocery_items, 2)
            p1 = random.randint(5, 20) * 10 # e.g., 50, 60... 200
            p2 = random.randint(5, 20) * 10
            
            total = p1 + p2
            context = random.choice(weather_context)
            
            self.tasks_data.append({
                "category": "math", "difficulty": 2,
                "question": f"{context} You buy {i1} (₹{p1}) and {i2} (₹{p2}). What is the total bill?",
                "answer": f"₹{total}",
                "options": [f"₹{total}", f"₹{total+10}", f"₹{total-10}", f"₹{total+20}"],
                "hint": "Ignore the weather. Just add the two prices."
            })

        # ==================================================
        # LEVEL 3: Algorithm A - "Market Kid" Heuristic
        # ==================================================
        for _ in range(50):
            # Scenario: Bill 327. Pay 500 + 20 + 7.
            base = random.choice([100, 200, 300, 400])
            tens = random.randint(1, 9) * 10
            units = random.choice([3, 6, 7, 8, 9]) 
            bill = base + tens + units 
            
            note_val = 500 if bill < 500 else 1000
            coins_val = units 
            total_paid = note_val + coins_val 
            
            change = total_paid - bill 
            route = random.randint(100, 500)

            self.tasks_data.append({
                "category": "math", "difficulty": 3,
                "question": f"You take Bus Route {route} to the market. The bill is ₹{bill}. You hand the cashier a ₹{note_val} note and ₹{coins_val} in coins (Total ₹{total_paid}). How much change do you get?",
                "answer": f"₹{change}",
                "options": [f"₹{change}", f"₹{change-coins_val}", f"₹{change+10}", f"₹{change-10}"],
                "hint": f"Think: ₹{total_paid} - ₹{bill}. The ₹{coins_val} cancels out the last digit."
            })

        # ==================================================
        # LEVEL 4: Algorithm B - Inflationary Budgeting
        # ==================================================
        market_types = ["Rice", "Oil", "Dal", "Sugar", "Spices", "Wheat"]
        for _ in range(50):
            budget = 500
            # Randomize cart
            cart_items = random.sample(market_types, 3)
            # Random prices
            prices = [random.randint(10, 20)*10 for _ in range(3)] 
            
            initial_total = sum(prices)
            
            # Make sure total is close to budget for the logic to work
            if initial_total < 300: initial_total += 100

            shock_idx = 0
            shock_name = cart_items[shock_idx]
            old_price = prices[shock_idx]
            
            new_price = int(old_price * 1.40) # 40% rise
            new_total = initial_total - old_price + new_price
            deficit = new_total - budget
            
            if deficit > 0:
                q_text = f"Your budget is ₹{budget}. Cart: {cart_items[0]}, {cart_items[1]}, {cart_items[2]} (Total ₹{initial_total}). Suddenly, monsoon rains damage the {shock_name} crop! Price rises 40% to ₹{new_price}. How much EXTRA money do you need?"
                ans = f"₹{deficit}"
                opts = [f"₹{deficit}", f"₹{deficit+10}", f"₹{deficit-5}", "₹0"]
            else:
                remaining = abs(deficit)
                q_text = f"Your budget is ₹{budget}. Cart: {cart_items[0]}, {cart_items[1]}, {cart_items[2]}. {shock_name} price rises 40% to ₹{new_price}. New Total is ₹{new_total}. How much money is left?"
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
        # ==================================================
        products = ["Garlic", "Coffee", "Cashews", "Detergent", "Almonds"]
        for _ in range(50):
            prod = random.choice(products)
            base_price = random.choice([200, 300, 400, 500, 600])
            
            opt_a = f"1 kg for ₹{base_price}"
            price_b = int((base_price / 2) * 1.2)
            opt_b = f"500g for ₹{price_b}"
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
        ordinals = {1:"1st", 2:"2nd", 3:"3rd", 4:"4th", 5:"5th", 6:"6th", 7:"7th", 8:"8th", 9:"9th"}
        
        for level in range(1, 6):
            num_digits = level + 4
            
            for _ in range(50): # Increased to 50
                # Generate completely random sequences every time
                digits = [str(random.randint(0, 9)) for _ in range(num_digits)]
                memorize_str = " - ".join(digits)
                
                target_idx = random.randint(0, num_digits - 1)
                target_pos = target_idx + 1
                correct_digit = digits[target_idx]
                
                question_text = f"Which number was {ordinals[target_pos]}?"
                
                # Ensure unique options
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

        # Filter available tasks
        filtered_tasks = [
            t for t in self.tasks_data 
            if t['difficulty'] == difficulty 
            and (category is None or t['category'] == category)
            # Exclude already played ones
            and (t.get('memorize_content', t['question']) not in exclude_questions)
        ]

        # If we run out of unique tasks, reset pool (allow repeats but warn user)
        if not filtered_tasks:
            filtered_tasks = [
                t for t in self.tasks_data 
                if t['difficulty'] == difficulty 
                and (category is None or t['category'] == category)
            ]
        
        # Fallback if somehow still empty
        if not filtered_tasks:
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