def calculate_accuracy(correct_count, total_questions):
    """
    Calculates the percentage of correct answers.
    
    :param correct_count: Number of correct answers (int)
    :param total_questions: Total number of questions attempted (int)
    :return: Accuracy percentage (float), rounded to 1 decimal place
    """
    if total_questions == 0:
        return 0.0
    
    accuracy = (correct_count / total_questions) * 100
    return round(accuracy, 1)


def get_performance_tier(accuracy):
    """
    Buckets performance into descriptive categories suitable for user feedback.
    
    :param accuracy: Accuracy percentage (0-100)
    :return: String ('Needs Practice', 'Good Job', 'Excellent')
    """
    if accuracy >= 85:
        return "Excellent"
    elif accuracy >= 60:
        return "Good Job"
    else:
        return "Needs Practice"


def compute_reward(correct, total, avg_time_sec, difficulty=1):
    """
    Computes a 'Cognitive Score' based on accuracy, difficulty, and speed.
    
    Formula Logic:
    1. Base Score: 10 points per correct answer.
    2. Difficulty Multiplier: Higher difficulty scales the base points.
    3. Time Bonus: Extra points if answering faster than a 'generous' threshold (30s).
       *Note: Seniors are not penalized for being slow, they just gain less bonus.*
    
    :param correct: Number of correct answers
    :param total: Total questions
    :param avg_time_sec: Average time taken per question in seconds
    :param difficulty: Task difficulty level (1-5)
    :return: Final calculated score (int)
    """
    if total == 0:
        return 0

    # 1. Accuracy Base Score (Weighted by difficulty)
    # Level 1 = 10pts per Q, Level 5 = 50pts per Q
    points_per_q = 10 * difficulty
    base_score = correct * points_per_q

    # 2. Time Bonus (Incentive, not penalty)
    # Threshold: We expect ~30 seconds per question for seniors.
    # If they are faster, they get 1 point per second saved.
    target_time_per_q = 30 
    time_saved = max(0, target_time_per_q - avg_time_sec)
    
    # Scale bonus by number of correct answers (only reward speed if accurate)
    speed_bonus = int(time_saved * correct)

    final_score = base_score + speed_bonus
    return final_score


def generate_session_report(correct, total, avg_time, difficulty):
    """
    Helper to generate a full dictionary report for a session.
    """
    acc = calculate_accuracy(correct, total)
    tier = get_performance_tier(acc)
    score = compute_reward(correct, total, avg_time, difficulty)
    
    return {
        "total_questions": total,
        "correct_answers": correct,
        "accuracy_percent": acc,
        "performance_tier": tier,
        "average_time": f"{avg_time}s",
        "difficulty_level": difficulty,
        "total_score": score
    }

# ---------------------------------------------------------
# EXECUTION EXAMPLE
# ---------------------------------------------------------
if __name__ == "__main__":
    # Example Scenario: User attempts 5 questions at Difficulty 3
    # They get 4 correct, taking an average of 12 seconds per question.
    
    total_qs = 5
    correct_ans = 4
    avg_speed = 12.5 # seconds
    level = 3
    
    print(f"--- Session Stats (Level {level}) ---")
    
    # 1. Check Accuracy
    acc = calculate_accuracy(correct_ans, total_qs)
    print(f"Accuracy: {acc}%")
    
    # 2. Check Tier
    tier = get_performance_tier(acc)
    print(f"Feedback: {tier}")
    
    # 3. Compute Reward
    # Calculation:
    # Base = 4 correct * (10 * 3 difficulty) = 120 points
    # Time Bonus = (30s - 12.5s) * 4 correct = 17.5 * 4 = 70 points
    # Total should be 190
    score = compute_reward(correct_ans, total_qs, avg_speed, level)
    print(f"Cognitive Score: {score}")