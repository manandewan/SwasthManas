import streamlit as st
import time
import pandas as pd
import streamlit.components.v1 as components 
from rl_agent import AdaptiveDifficultyAgent
from tasks import CognitiveTaskGenerator

# Fallback for tutor if file missing
try:
    from tutor import CognitiveTutor
except ImportError:
    class CognitiveTutor:
        def generate_feedback(self, task, ans, corr): return "Result processed.", None

# ---------------------------------------------------------
# 1. CONFIG & STYLES
# ---------------------------------------------------------
st.set_page_config(page_title="SwasthManas", page_icon="🧠", layout="centered")

st.markdown("""
    <style>
        h1, h2, h3, h4, h5, h6, p, span, div, caption, label { color: #333333 !important; }
        .stSuccess, .stSuccess p { color: #065f46 !important; }
        .stError, .stError p { color: #991b1b !important; }
        .stInfo, .stInfo p { color: #1e40af !important; }
        .stApp { background-color: #f8f9fa; }
        .question-card {
            background-color: white; padding: 40px; border-radius: 20px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1); margin-bottom: 20px;
            text-align: center; border: 2px solid #e0e0e0;
        }
        .question-text { font-size: 36px !important; font-weight: 700; color: #111827; }
        div.stButton > button {
            font-size: 24px !important; height: 100px !important; font-weight: 600 !important;
            white-space: normal !important; background-color: #ffffff; color: #333333;
            border: 3px solid #4F8BF9; border-radius: 12px;
        }
        div.stButton > button:hover {
            background-color: #4F8BF9; color: white; border-color: #4F8BF9;
        }
    </style>
""", unsafe_allow_html=True)

def show_question_card(question_text):
    st.markdown(f"""
        <div class="question-card">
            <div class="question-text">{question_text}</div>
        </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. INIT SESSION STATE
# ---------------------------------------------------------
if 'generator' not in st.session_state: st.session_state.generator = CognitiveTaskGenerator()
if 'tutor' not in st.session_state: st.session_state.tutor = CognitiveTutor()
if 'agent' not in st.session_state:
    st.session_state.agent = AdaptiveDifficultyAgent()
    st.session_state.agent.load_agent()

# Vars
if 'page' not in st.session_state: st.session_state.page = "onboarding"
if 'selected_category' not in st.session_state: st.session_state.selected_category = None
if 'current_difficulty' not in st.session_state: st.session_state.current_difficulty = 1
if 'history' not in st.session_state: st.session_state.history = []
if 'current_task' not in st.session_state: st.session_state.current_task = None
if 'feedback_msg' not in st.session_state: st.session_state.feedback_msg = None
if 'questions_played' not in st.session_state: st.session_state.questions_played = 0
if 'hint_visible' not in st.session_state: st.session_state.hint_visible = False
if 'played_ids' not in st.session_state: st.session_state.played_ids = []

# Tracks individual user levels in THIS session only (RAM only)
if 'user_levels' not in st.session_state:
    st.session_state.user_levels = {"math": 1, "memory": 1}
    
# Track memory phase state
if 'memory_shown' not in st.session_state: st.session_state.memory_shown = False

# --- CHANGE: Reduced game length to 5 ---
GAME_LENGTH = 5

# ---------------------------------------------------------
# 3. HELPER FUNCTIONS
# ---------------------------------------------------------
def map_comfort_to_level(choice):
    if choice == "Comfortable": return 5
    elif choice == "Not sure": return 3
    else: return 2

def save_onboarding(math_choice, mem_choice):
    # Save to session state only (will reset on refresh)
    st.session_state.user_levels["math"] = map_comfort_to_level(math_choice)
    st.session_state.user_levels["memory"] = map_comfort_to_level(mem_choice)
    st.session_state.page = "menu"
    st.rerun()

def start_game(category):
    st.session_state.selected_category = category.lower()
    st.session_state.page = "game"
    
    # Load from temporary session memory
    start_level = st.session_state.user_levels.get(category.lower(), 1)
    
    st.session_state.current_difficulty = start_level
    st.session_state.feedback_msg = None
    st.session_state.questions_played = 0
    st.session_state.history = []
    st.session_state.played_ids = []
    
    # Reset memory flag
    st.session_state.memory_shown = False
    
    generate_new_task()
    st.rerun()

def return_to_menu():
    st.session_state.page = "menu"
    st.session_state.selected_category = None
    st.session_state.current_task = None
    st.rerun()

def generate_new_task():
    if st.session_state.questions_played >= GAME_LENGTH:
        # Update session memory before showing score
        if st.session_state.selected_category:
            cat = st.session_state.selected_category
            st.session_state.user_levels[cat] = st.session_state.current_difficulty
            
        st.session_state.page = "score"
        return
    
    diff = st.session_state.current_difficulty
    cat = st.session_state.selected_category
    
    # Generate task
    task = st.session_state.generator.generate_task(
        category=cat, 
        difficulty=diff,
        exclude_questions=st.session_state.played_ids
    )
    
    st.session_state.current_task = task
    # Use memorize content as ID if available, else question
    t_id = task.get('memorize_content', task['question'])
    st.session_state.played_ids.append(t_id)
    
    st.session_state.start_time = time.time()
    st.session_state.feedback_msg = None
    st.session_state.hint_visible = False
    
    # IMPORTANT: Reset memory flag for new task
    st.session_state.memory_shown = False

def process_answer(selected_option):
    end_time = time.time()
    duration = end_time - st.session_state.start_time
    used_hint = st.session_state.hint_visible
    
    task = st.session_state.current_task
    correct_ans = task['correct_answer']
    is_correct = (selected_option == correct_ans)
    
    # 1. Reward
    reward = 10 if is_correct else -10
    if used_hint: reward -= 5
    if is_correct:
        if duration < 5: reward += 5
        elif duration > 15: reward -= 2

    # 2. Tier Logic
    tier = "Needs Practice"
    if is_correct:
        if used_hint or duration > 15: tier = "Average"
        else: tier = "Excellent"
        
    # 3. AI Decision
    current_diff = st.session_state.current_difficulty
    current_cat = task['category']  
    
    action = st.session_state.agent.choose_action(current_cat, current_diff, tier)
    next_diff = max(1, min(5, current_diff + action))
    
    # Notification
    if action == 1: st.toast("Level Up! ⬆️", icon="🔥")
    elif action == -1: st.toast("Easing down. ⬇️", icon="🛡️")

    # 4. Learn
    state = (current_cat, current_diff, tier)
    next_state = (current_cat, next_diff, tier)
    
    st.session_state.agent.learn(state, action, reward, next_state)
    
    st.session_state.current_difficulty = next_diff
    st.session_state.questions_played += 1
    
    st.session_state.history.append({
        "Question": task['question'], "Result": "✅" if is_correct else "❌",
        "Diff": current_diff, "Time": f"{duration:.1f}s", "Hint": "Yes" if used_hint else "No"
    })
    
    # 5. Tutor
    txt, tip = st.session_state.tutor.generate_feedback(task, selected_option, is_correct)
    st.session_state.feedback_msg = {"text": txt, "tip": tip, "type": "success" if is_correct else "error"}

# ---------------------------------------------------------
# 4. UI PAGES
# ---------------------------------------------------------

# --- A. ONBOARDING ---
if st.session_state.page == "onboarding":
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.markdown("""
            <div style="text-align: center;">
                <h1 style="color: #1f2937; margin: 0;">SwasthManas</h1>
                <p style="color: #666;">Let's customize your training plan.</p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
        
        st.markdown("##### 1. How comfortable are you with **Math**?")
        math_choice = st.radio("Math Comfort", ["Comfortable", "Not sure", "Not comfortable"], key="m_conf", label_visibility="collapsed")
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("##### 2. How comfortable are you with your **Memory**?")
        mem_choice = st.radio("Memory Comfort", ["Comfortable", "Not sure", "Not comfortable"], key="mem_conf", label_visibility="collapsed")
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("Create My Plan 🚀", type="primary", use_container_width=True):
            save_onboarding(math_choice, mem_choice)

# --- B. MENU ---
elif st.session_state.page == "menu":
    c1, c2 = st.columns([1.2, 4])
    with c1: st.markdown("""<svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><circle cx="50" cy="50" r="45" fill="#E0F2FE" stroke="#4F8BF9" stroke-width="3"/><path d="M35 50 C 35 30, 65 30, 65 50" stroke="white" stroke-width="3" stroke-linecap="round"/><path d="M50 25 V 45" stroke="#4F8BF9" stroke-width="4"/><path d="M30 55 C 30 40, 70 40, 70 55 C 70 70, 30 70, 30 55" fill="#4F8BF9" opacity="0.8"/></svg>""", unsafe_allow_html=True)
    with c2: 
        st.markdown("<div style='padding-top:10px;'><h1 style='margin:0; font-size: 64px;'>SwasthManas</h1><h4 style='margin:0; font-weight:400;'>Daily Brain Training</h4></div>", unsafe_allow_html=True)
    st.markdown("---")
    
    math_lvl = st.session_state.user_levels["math"]
    mem_lvl = st.session_state.user_levels["memory"]
    
    st.info(f"**Your Progress:** Math (Lvl {math_lvl}) | Memory (Lvl {mem_lvl})")
    
    c1, c2 = st.columns(2)
    with c1: 
        st.image("https://img.icons8.com/fluency/96/calculator.png", width=80)
        if st.button("Math", use_container_width=True): start_game("math")
    with c2: 
        st.image("https://img.icons8.com/fluency/96/brain.png", width=80)
        if st.button("Memory", use_container_width=True): start_game("memory")

# --- C. GAME ---
elif st.session_state.page == "game":
    c1, c2 = st.columns([1, 4])
    with c1: 
        if st.button("Quit"): return_to_menu()
    with c2: 
        st.progress(st.session_state.questions_played / GAME_LENGTH)
    
    # --- VISUAL TIMER (JS Injection) ---
    components.html(
        """
        <div style="font-family: sans-serif; font-size: 18px; color: #555; text-align: right; padding-right: 20px;">
            ⏱️ <span id="time">0</span>s
        </div>
        <script>
            var sec = 0;
            setInterval(function(){
                sec += 1;
                document.getElementById("time").innerHTML = sec;
            }, 1000);
        </script>
        """, 
        height=40
    )

    # 1. SHOW FEEDBACK IF ANSWERED
    if st.session_state.feedback_msg:
        fb = st.session_state.feedback_msg
        if fb['type'] == "success": st.success(fb['text'])
        else:
            st.error(fb['text'])
            if fb.get('tip'): st.info(f"💡 **Coach's Tip:**\n\n{fb['tip']}")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Next ➡️", type="primary", use_container_width=True):
            generate_new_task()
            st.rerun()

    else:
        # 2. SHOW TASK
        if st.session_state.current_task:
            task = st.session_state.current_task
            
            # --- MEMORY SPECIFIC LOGIC ---
            if task.get('memorize_content') and not st.session_state.memory_shown:
                # PHASE 1: MEMORIZE
                st.info("🧠 **Memorize this sequence!**")
                show_question_card(task['memorize_content']) 
                
                # FIXED 10 Seconds for all levels
                memorize_time = 10
                
                # Display countdown
                timer_text = st.empty()
                for i in range(memorize_time, 0, -1):
                    timer_text.markdown(f"<h3 style='text-align: center; color: #4F8BF9;'>⏳ Time remaining: {i}s</h3>", unsafe_allow_html=True)
                    time.sleep(1)
                
                timer_text.empty()
                st.session_state.memory_shown = True
                st.rerun()

            # --- STANDARD OR MEMORY RECALL PHASE ---
            else:
                # PHASE 2: RECALL (or Standard Question)
                show_question_card(task['question'])
                
                # Hint Logic
                hint = task.get('hint', "No hint.")
                if not st.session_state.hint_visible:
                    if st.button("💡 Hint"): st.session_state.hint_visible = True; st.rerun()
                else: st.info(f"**Hint:** {hint}")
                
                st.markdown("<br>", unsafe_allow_html=True)
                opts = task['options']
                c1, c2 = st.columns(2)
                with c1:
                    if st.button(str(opts[0]), key="o0", use_container_width=True): process_answer(opts[0]); st.rerun()
                    if len(opts)>2 and st.button(str(opts[2]), key="o2", use_container_width=True): process_answer(opts[2]); st.rerun()
                with c2:
                    if len(opts)>1 and st.button(str(opts[1]), key="o1", use_container_width=True): process_answer(opts[1]); st.rerun()
                    if len(opts)>3 and st.button(str(opts[3]), key="o3", use_container_width=True): process_answer(opts[3]); st.rerun()

# --- D. SCORE ---
elif st.session_state.page == "score":
    st.title("🎉 Session Complete!")
    st.markdown("---")
    df = pd.DataFrame(st.session_state.history)
    acc = (len(df[df['Result']=="✅"]) / GAME_LENGTH) * 100
    
    st.markdown(f"<div style='background-color:#d1fae5;padding:20px;border-radius:15px;text-align:center;border:2px solid #10b981;'><h1 style='color:#047857;margin:0;'>{acc:.0f}% Accuracy</h1></div>", unsafe_allow_html=True)
    
    if not df.empty:
        st.markdown("### 📈 Difficulty Adaptation")
        chart_data = df.reset_index()[['index', 'Diff']]
        chart_data.columns = ['Question', 'Level']
        st.line_chart(chart_data, x='Question', y='Level')
        
    c1, c2 = st.columns(2)
    with c1: 
        if st.button("🏠 Menu", type="primary", use_container_width=True): return_to_menu()
    with c2: 
        if st.button("🔄 Play Again", use_container_width=True): start_game(st.session_state.selected_category)