import numpy as np
import random
import pickle
import os

class AdaptiveDifficultyAgent:
    """
    Tabular Q-Learning Agent with Heuristic Initialization ("Instincts").
    """
    def __init__(self, alpha=0.5, gamma=0.8, epsilon=0.2):
        self.q_table = {} 
        self.alpha = alpha      
        self.gamma = gamma      
        self.epsilon = epsilon  
        self.actions = [-1, 0, 1]  # Decrease, Stay, Increase

    def get_q_values(self, state):
        """
        Returns Q-values. If state is new, we initialize with 'Instincts'.
        """
        if state not in self.q_table:
            # Unpack 3 values (Category is just a string here, agent doesn't care what it is)
            category, difficulty, tier = state 
            
            # Instincts: Bias values based on performance
            if tier == "Excellent":
                self.q_table[state] = [0.0, 1.0, 10.0] # Strong push to INCREASE
            elif tier == "Needs Practice":
                self.q_table[state] = [10.0, 1.0, -5.0] # Strong push to DECREASE
            else: 
                self.q_table[state] = [-1.0, 5.0, 2.0] # Bias to STAY
                
        return self.q_table[state]

    def choose_action(self, category, difficulty, tier):
        state = (category, difficulty, tier) # Create 3-tuple state
        q_values = self.get_q_values(state)

        # Exploration
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(self.actions)

        # Exploitation
        max_q_index = np.argmax(q_values)
        return self.actions[max_q_index]

    def learn(self, state, action, reward, next_state):
        action_idx = self.actions.index(action)
        current_q = self.get_q_values(state)[action_idx]
        next_q_values = self.get_q_values(next_state)
        max_next_q = np.max(next_q_values)
        
        # Bellman Equation Update
        new_q = current_q + self.alpha * (reward + self.gamma * max_next_q - current_q)
        self.q_table[state][action_idx] = new_q
        
        self.save_agent()

    def save_agent(self, filename="q_table.pkl"):
        try:
            with open(filename, "wb") as f:
                pickle.dump(self.q_table, f)
        except Exception:
            pass

    def load_agent(self, filename="q_table.pkl"):
        if os.path.exists(filename):
            try:
                with open(filename, "rb") as f:
                    self.q_table = pickle.load(f)
            except Exception:
                pass