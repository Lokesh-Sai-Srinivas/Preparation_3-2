import streamlit as st
import os
import json

# --- 1. SETUP PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Exam Master",
    layout="wide", # Wide layout for better reading experience
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR PREMIUM DARK UI ---
st.markdown("""
<style>
    /* Global Styles */
    .stApp {
        background-color: #0E1117; /* Streamlit Dark Default is good, but let's enforce sleekness */
        color: #FAFAFA;
    }
    
    /* Typography */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        color: #FFFFFF;
    }
    p, li, .stMarkdown {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        line-height: 1.7;
        color: #E0E0E0;
    }

    /* Question Card */
    .question-card {
        background-color: #1E1E1E; /* Subtle lighter dark */
        padding: 24px;
        border-radius: 12px;
        border-left: 4px solid #FF4B4B; /* Accent color */
        margin-bottom: 24px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    .question-text {
        font-size: 1.3rem;
        font-weight: 600;
        color: #FFFFFF;
        margin: 0;
    }

    /* Answer Area - Clean Dark */
    .answer-area {
        margin-top: 20px;
        padding-left: 10px;
        border-left: 2px solid #333;
    }

    /* Navigation Bubbles */
    .stButton button {
        background-color: #262730;
        color: #FFFFFF;
        border: 1px solid #333;
        border-radius: 20px;
        padding: 4px 16px;
        font-size: 0.9rem;
        transition: all 0.2s;
    }
    .stButton button:hover {
        background-color: #3E4050;
        border-color: #FF4B4B;
        color: #FFFFFF;
    }
    .stButton button:active, .stButton button:focus {
        background-color: #FF4B4B !important;
        color: #FFFFFF !important;
        border-color: #FF4B4B !important;
    }
    
    /* Highlight the active question button if we could target it directly, 
       but we handles this via session state logic in python mostly */

</style>
""", unsafe_allow_html=True)

# --- 2. DATA LOADING FUNCTIONS ---
DATA_DIR = "data"

def get_subjects():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        return []
    return [d for d in os.listdir(DATA_DIR) if os.path.isdir(os.path.join(DATA_DIR, d))]

def get_units(subject):
    subject_path = os.path.join(DATA_DIR, subject)
    if not os.path.exists(subject_path):
        return []
    return sorted([d for d in os.listdir(subject_path) if os.path.isdir(os.path.join(subject_path, d))])

def load_questions(subject, unit, q_type):
    file_path = os.path.join(DATA_DIR, subject, unit, f"{q_type}.json")
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return []
    return []

# --- 3. SIDEBAR SELECTION ---
st.sidebar.title("📚 Study Filters")
subjects = get_subjects()
selected_subject = st.sidebar.selectbox("Select Subject", subjects) if subjects else None
selected_unit = None

if selected_subject:
    units = get_units(selected_subject)
    if units:
        selected_unit = st.sidebar.selectbox("Select Unit", units)
    else:
        st.sidebar.warning("No units found.")

# q_type = st.sidebar.radio("Question Type", ["Short", "Long"])
# Let's make the type selection cleaner, maybe pill-like in the sidebar
q_type = st.sidebar.radio("Mode", ["Short Questions", "Long Questions"])
q_type_key = "Short" if "Short" in q_type else "Long"


# --- 4. MAIN LOGIC ---
if selected_subject and selected_unit:
    # Title Section - Detailed Custom Heading
    st.markdown(f"<h1 style='text-align: center; color: #FF4B4B; margin-bottom: 0px;'>{selected_subject}</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; color: #E0E0E0; margin-top: 10px; margin-bottom: 40px; font-weight: 300;'>{selected_unit}</h3>", unsafe_allow_html=True)

    # Load Questions
    questions = load_questions(selected_subject, selected_unit, q_type_key)

    if not questions:
        st.info(f"No {q_type_key} questions available yet.")
    else:
        # --- SESSION STATE MANAGEMENT ---
        session_key = f"{selected_subject}_{selected_unit}_{q_type_key}"
        
        if 'current_session_key' not in st.session_state or st.session_state.current_session_key != session_key:
            st.session_state.current_session_key = session_key
            st.session_state.q_index = 0

        # --- NAVIGATION BUBBLES ---
        st.write("### 🧭 Navigate")
        
        cols = st.columns(10)
        for i in range(len(questions)):
            is_active = (i == st.session_state.q_index)
            label = f"{i + 1}"
            with cols[i % 10]:
                if st.button(label, key=f"q_nav_{i}", type="primary" if is_active else "secondary", use_container_width=True):
                    st.session_state.q_index = i
                    st.rerun()
        
        st.markdown("---")

        # --- QUESTION DISPLAY ---
        if st.session_state.q_index >= len(questions):
            st.session_state.q_index = 0
            
        current_q = questions[st.session_state.q_index]
        
        # Display Question Card
        st.markdown(f"""
        <div class="question-card">
            <div style="color: #FF4B4B; font-size: 0.9rem; margin-bottom: 8px; font-weight: bold; letter-spacing: 1px;">
                QUESTION {st.session_state.q_index + 1}
            </div>
            <p class="question-text" style="white-space: pre-wrap;">{current_q['q']}</p>
        </div>
        """, unsafe_allow_html=True)

        st.subheader("Answer")
        
        with st.container():
             # Check for Split Question (Part A / Part B)
             if 'answer_a' in current_q:
                 # --- PART A ---
                 st.markdown(current_q['answer_a'])
                 
                 if 'graphviz_a' in current_q:
                     st.write("#### 📊 Diagram (Part A)")
                     st.graphviz_chart(current_q['graphviz_a'])
                 
                 if 'table_a' in current_q:
                     st.write("#### 📋 Table (Part A)")
                     st.markdown(current_q['table_a'])
                 
                 st.markdown("---")
                 
                 # --- PART B ---
                 if 'answer_b' in current_q:
                    st.markdown(current_q['answer_b'])
                    
                    if 'graphviz_b' in current_q:
                        st.write("#### 📊 Diagram (Part B)")
                        st.graphviz_chart(current_q['graphviz_b'])
                    
                    if 'table_b' in current_q:
                        st.write("#### 📋 Table (Part B)")
                        st.markdown(current_q['table_b'])
             
             else:
                 # --- STANDARD SINGLE ANSWER ---
                 st.markdown(current_q.get('a', 'No answer provided.'))
                 
                 if 'graphviz' in current_q:
                     st.write("### 📊 Diagram")
                     st.graphviz_chart(current_q['graphviz'])
                 
                 if 'table' in current_q:
                     st.write("### 📋 Table")
                     st.markdown(current_q['table'])

else:
    st.markdown("""
    <div style="text-align: center; padding: 50px; opacity: 0.6;">
        <h2>Select a Subject and Unit to Start Studying</h2>
        <p>👈 Use the sidebar to navigate</p>
    </div>
    """, unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("""
<div style="position: fixed; bottom: 0; left: 0; width: 100%; background-color: #0E1117; color: #808495; text-align: center; padding: 10px; font-size: 0.8rem; border-top: 1px solid #262730;">
    © 2026 All Rights Reserved | Created by <b>A. Lokesh Sai Srinivas</b>
</div>
<style>
    /* Adjust main block padding to ensure footer doesn't overlap content */
    .block-container {
        padding-bottom: 60px;
    }
</style>
""", unsafe_allow_html=True)