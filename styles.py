import streamlit as st

def apply_custom_styles():
    st.markdown("""
        <style>
        /* 1. INCREASE PAGE WIDTH */
        section.main > div {
            max-width: 1000px !important;
            padding-left: 2rem;
            padding-right: 2rem;
        }

        /* MAIN BACKGROUND */
        .stApp {
            background-color: #f8f9fa;
        }
        
        /* CARD CONTAINER */
        .question-card {
            background-color: white;
            padding: 50px;
            border-radius: 20px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            margin-bottom: 30px;
            text-align: center;
            border: 2px solid #e0e0e0;
        }
        
        /* --- TEXT SIZE INCREASES --- */
        
        /* 1. HUGE QUESTION TEXT */
        .question-text {
            font-size: 40px !important; /* Increased from 32px */
            font-weight: 800;
            color: #111827; /* Darker black for contrast */
            line-height: 1.4;
        }
        
        /* 2. GIANT BUTTON TEXT */
        div.stButton > button {
            font-size: 32px !important; /* Increased from 26px */
            height: 120px !important;   /* Taller to fit new text */
            font-weight: 600 !important;
            
            white-space: normal !important; 
            background-color: #ffffff;
            color: #333333;
            border: 4px solid #4F8BF9; /* Thicker border */
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }
        
        /* HOVER EFFECT */
        div.stButton > button:hover {
            background-color: #4F8BF9;
            color: white;
            border-color: #4F8BF9;
            transform: scale(1.02);
        }

        /* 3. LARGE FEEDBACK TEXT */
        .stSuccess, .stError {
            font-size: 28px !important; /* Increased from 22px */
            padding: 30px !important;
            text-align: center;
            font-weight: bold;
        }

        /* HIDE EXTRA STREAMLIT ELEMENTS */
        small { display: none !important; }
        footer { display: none !important; }
        
        </style>
    """, unsafe_allow_html=True)

def show_question_card(question_text):
    st.markdown(f"""
        <div class="question-card">
            <div class="question-text">{question_text}</div>
        </div>
    """, unsafe_allow_html=True)