import random

class CognitiveTutor:
    """
    RAG-Lite system for intelligent feedback.
    """
    
    def __init__(self):
        self.strategy_db = {
            "math": [
                "**Chunking:** Break large numbers into smaller parts (e.g., 15+8 -> 15+5+3).",
                "**Estimation:** Round numbers first to guess the ballpark answer.",
                "**Visualization:** Imagine physical objects like coins or apples.",
                "**Money Method:** Think of numbers as currency (quarters, dollars)."
            ],
            "memory": [
                "**Story Method:** Create a quick funny story connecting the items.",
                "**Grouping:** Remember numbers in chunks (e.g., 25-14 instead of 2-5-1-4).",
                "**Visualization:** Close your eyes and create a mental image of the list."
            ]
        }

    def generate_feedback(self, task, user_answer, is_correct):
        """
        Returns TWO values: (Main Feedback Message, Strategic Tip)
        """
        if is_correct:
            msg = random.choice([
                "Spot on! Your strategy is working.",
                "Excellent focus.",
                "Perfect. You are processing this information efficiently.",
                "Great work! That was quick and accurate."
            ])
            return msg, None  # No tip needed for correct answers
        
        category = task['category']
        correct_ans = task['correct_answer']
        
        # 1. Retrieve the Strategy (The Tip)
        strategy = random.choice(self.strategy_db.get(category, ["Take a deep breath and try again."]))
        
        # 2. Generate the Explanation
        explanation = ""
        if category == "math":
            explanation = f"The answer was **{correct_ans}**."
        elif category == "memory":
             explanation = f"The missing item was **{correct_ans}**."
        else:
             explanation = f"The correct answer was **{correct_ans}**."

        feedback_msg = f"**Not quite.** {explanation}"
        
        return feedback_msg, strategy