========================================================================
SWASTHMANAS: AI-DRIVEN COGNITIVE TRAINING FOR SENIORS
========================================================================

PROJECT OVERVIEW
----------------
SwasthManas is a personalized brain-training application designed specifically for seniors. Unlike traditional apps that use static difficulty scaling (e.g., "Level up after 3 wins"), SwasthManas utilizes a Reinforcement Learning (RL) Agent to dynamically adjust the difficulty of tasks in real-time.

The goal is to keep the user in the "Flow Channel"—a state balanced between boredom (task too easy) and anxiety (task too hard)—to maximize engagement and therapeutic value.

KEY FEATURES
----------------
1. Adaptive AI Agent: 
   Uses Tabular Q-Learning to learn the user's capability and adjust difficulty (Levels 1-5) on the fly.

2. Procedural Content Generation:
   - Math: Generates problems ranging from simple exact change (Level 1) to unit price optimization (Level 5).
   - Memory: Dynamic sequence recall tasks scaling from 5 to 9 digits.

3. Senior-Centric UI: 
   High-contrast design, large text (40px+), and accessible buttons.

4. Intelligent Tutor: 
   Provides context-aware hints and strategic feedback (e.g., "Chunking" strategies for memory).

TECH STACK
----------------
- Frontend: Streamlit (Python)
- Core Logic: Python (NumPy, Pandas)
- AI/ML: Reinforcement Learning (Q-Learning), Procedural Generation

INSTALLATION & SETUP
----------------
Step 1: Clone the Repository
   git clone https://github.com/YOUR_USERNAME/SwasthManas.git
   cd SwasthManas

Step 2: Install Dependencies
   pip install -r requirements.txt

Step 3: Run the Application
   streamlit run app.py

PROJECT STRUCTURE
----------------
- app.py .......... Main application entry point; handles UI and session state.
- rl_agent.py ..... Contains the AdaptiveDifficultyAgent class (Q-Learning logic).
- tasks.py ........ CognitiveTaskGenerator class for creating procedural questions.
- tutor.py ........ Logic for generating hints and pedagogical feedback.
- performance.py .. Metrics for calculating accuracy, speed bonuses, and scores.
- project.ipynb ... SOURCE OF TRUTH: Contains simulation pipeline and data analysis.
- styles.py ....... Custom CSS injections for senior-friendly accessibility.

HOW THE AI WORKS
----------------
The system uses a Model-Free Reinforcement Learning approach (Tabular Q-Learning).

1. State: Defined by Category, Current Difficulty, and Performance Tier.
2. Action: The agent chooses to Increase (+1), Decrease (-1), or Stay (0).
3. Reward: Calculated based on Accuracy (+10 pts), Speed Bonus (target 30s), and Hint Usage penalties.

Note: To avoid the "Cold Start" problem, the AI is initialized with "Instincts" (e.g., if performance is 'Excellent', the agent is biased to increase difficulty immediately).

EVALUATION
----------------
To verify the agent's behavior without playing 50 games manually, run the simulation in the notebook:
1. Open "project.ipynb"
2. Run the "Simulation Pipeline" cells.
3. View the generated "Adaptive Difficulty Curve" graph.

ETHICAL CONSIDERATIONS
----------------
- Accessibility: The UI explicitly supports age-related vision changes.
- Inclusivity: Math problems use generic items and currency to minimize cultural friction.
- Data Privacy: The RL agent runs locally on the device; no personal data is sent to the cloud.

LICENSE
----------------
This project is open-source and available under the MIT License.