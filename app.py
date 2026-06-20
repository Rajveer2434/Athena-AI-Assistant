import streamlit as st
import pandas as pd

from modules.ai_chat import ask_ai
from modules.task_manager import add_task, get_tasks
from modules.notes_manager import add_note, get_notes
from modules.weather import get_weather
from utils.db import create_tables

create_tables()

st.set_page_config(
    page_title="Athena AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Palette ──────────────────────────────────────────────
   Midnight navy  #0D1117
   Surface card   #161B22
   Border         #21262D
   Iris accent    #7C3AED
   Iris glow      #A78BFA
   Soft text      #8B949E
   Body text      #C9D1D9
   White          #F0F6FC
───────────────────────────────────────────────────────── */

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0D1117;
    color: #C9D1D9;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #161B22 !important;
    border-right: 1px solid #21262D;
    padding-top: 1.5rem;
}
[data-testid="stSidebar"] .stRadio > label {
    color: #8B949E;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
    gap: 0.25rem;
    display: flex;
    flex-direction: column;
}
[data-testid="stSidebar"] .stRadio label {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.6rem 1rem;
    border-radius: 8px;
    color: #8B949E;
    font-size: 0.9rem;
    font-weight: 500;
    transition: all 0.15s ease;
    cursor: pointer;
    border: 1px solid transparent;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: #21262D;
    color: #C9D1D9;
}

/* Main area */
.main .block-container {
    background-color: #0D1117;
    padding: 2rem 2.5rem;
    max-width: 1100px;
}

/* Page heading */
.page-header {
    margin-bottom: 2rem;
    padding-bottom: 1.25rem;
    border-bottom: 1px solid #21262D;
}
.page-header h1 {
    font-size: 1.6rem;
    font-weight: 700;
    color: #F0F6FC;
    margin: 0 0 0.25rem;
    letter-spacing: -0.02em;
}
.page-header p {
    color: #8B949E;
    font-size: 0.9rem;
    margin: 0;
}

/* Cards */
.card {
    background: #161B22;
    border: 1px solid #21262D;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}
.card:hover {
    border-color: #30363D;
}

/* Metric cards */
.metric-card {
    background: #161B22;
    border: 1px solid #21262D;
    border-radius: 12px;
    padding: 1.5rem 1.75rem;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #7C3AED, #A78BFA);
    border-radius: 12px 12px 0 0;
}
.metric-label {
    font-size: 0.75rem;
    font-weight: 600;
    color: #8B949E;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.5rem;
}
.metric-value {
    font-size: 2.4rem;
    font-weight: 700;
    color: #F0F6FC;
    line-height: 1;
    font-family: 'JetBrains Mono', monospace;
}
.metric-icon {
    font-size: 1.4rem;
    margin-bottom: 0.75rem;
}

/* Accent badge */
.badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(124, 58, 237, 0.15);
    color: #A78BFA;
    border: 1px solid rgba(124, 58, 237, 0.3);
    border-radius: 100px;
    padding: 0.2rem 0.75rem;
    font-size: 0.75rem;
    font-weight: 600;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #7C3AED, #6D28D9) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.55rem 1.4rem !important;
    font-size: 0.875rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.01em !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.3) !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #6D28D9, #5B21B6) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(124, 58, 237, 0.35) !important;
}

/* Inputs */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background-color: #0D1117 !important;
    border: 1px solid #30363D !important;
    border-radius: 8px !important;
    color: #C9D1D9 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    padding: 0.6rem 0.9rem !important;
    transition: border-color 0.15s ease !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #7C3AED !important;
    box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.15) !important;
}
.stTextInput label, .stTextArea label {
    color: #8B949E !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.07em !important;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border: 1px solid #21262D;
    border-radius: 10px;
    overflow: hidden;
}

/* Success/info alerts */
.stSuccess {
    background: rgba(34, 197, 94, 0.1) !important;
    border: 1px solid rgba(34, 197, 94, 0.25) !important;
    border-radius: 8px !important;
    color: #4ADE80 !important;
}

/* Divider */
hr {
    border-color: #21262D;
    margin: 1.5rem 0;
}

/* Section label */
.section-label {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #8B949E;
    margin-bottom: 1rem;
}

/* Chat bubble */
.chat-response {
    background: #161B22;
    border: 1px solid #21262D;
    border-left: 3px solid #7C3AED;
    border-radius: 0 10px 10px 0;
    padding: 1.25rem 1.5rem;
    margin-top: 1rem;
    color: #C9D1D9;
    font-size: 0.925rem;
    line-height: 1.7;
}

/* Note card */
.note-item {
    background: #161B22;
    border: 1px solid #21262D;
    border-radius: 10px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.6rem;
    font-size: 0.9rem;
    color: #C9D1D9;
    line-height: 1.5;
}

/* Weather stat */
.weather-stat {
    background: #161B22;
    border: 1px solid #21262D;
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
}
.weather-stat-value {
    font-size: 2rem;
    font-weight: 700;
    color: #F0F6FC;
    font-family: 'JetBrains Mono', monospace;
}
.weather-stat-label {
    font-size: 0.75rem;
    color: #8B949E;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 0.3rem;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0D1117; }
::-webkit-scrollbar-thumb { background: #30363D; border-radius: 3px; }

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 0 0.5rem 1.5rem; border-bottom: 1px solid #21262D; margin-bottom: 1.25rem;">
        <div style="display:flex;align-items:center;gap:0.6rem;margin-bottom:0.3rem;">
            <span style="font-size:1.3rem;">⚡</span>
            <span style="font-size:1.1rem;font-weight:700;color:#F0F6FC;letter-spacing:-0.02em;">Athena AI</span>
        </div>
        <span class="badge">● Online</span>
    </div>
    """, unsafe_allow_html=True)

    nav_icons = {
        "Dashboard": "◈",
        "AI Chat": "◎",
        "Tasks": "◻",
        "Notes": "◇",
        "Weather": "◉"
    }

    menu = st.radio(
        "NAVIGATION",
        list(nav_icons.keys()),
        format_func=lambda x: f"{nav_icons[x]}  {x}"
    )

    st.markdown("<div style='flex:1'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="position:absolute;bottom:1.5rem;left:1rem;right:1rem;">
        <div style="padding:0.75rem 1rem;background:#0D1117;border:1px solid #21262D;border-radius:8px;">
            <div style="font-size:0.7rem;color:#8B949E;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.2rem;">Model</div>
            <div style="font-size:0.85rem;color:#A78BFA;font-weight:500;">claude-sonnet-4-6</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── Pages ─────────────────────────────────────────────────────────────────────

# Dashboard
if menu == "Dashboard":
    st.markdown("""
    <div class="page-header">
        <h1>Dashboard</h1>
        <p>Your workspace at a glance</p>
    </div>
    """, unsafe_allow_html=True)

    tasks = get_tasks()
    notes = get_notes()

    completed = [t for t in tasks if len(t) > 2 and str(t[2]).lower() == "done"]

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">📋</div>
            <div class="metric-label">Total Tasks</div>
            <div class="metric-value">{len(tasks)}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">✅</div>
            <div class="metric-label">Completed</div>
            <div class="metric-value">{len(completed)}</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">📝</div>
            <div class="metric-label">Notes Saved</div>
            <div class="metric-value">{len(notes)}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:2rem;'></div>", unsafe_allow_html=True)

    col_l, col_r = st.columns([1, 1])

    with col_l:
        st.markdown('<div class="section-label">Recent Tasks</div>', unsafe_allow_html=True)
        if tasks:
            df = pd.DataFrame(tasks, columns=["ID", "Task", "Status"])
            st.dataframe(
                df.tail(5),
                use_container_width=True,
                hide_index=True,
                column_config={
                    "ID": st.column_config.NumberColumn("ID", width="small"),
                    "Task": st.column_config.TextColumn("Task"),
                    "Status": st.column_config.TextColumn("Status"),
                }
            )
        else:
            st.markdown('<div class="note-item" style="color:#8B949E;text-align:center;padding:2rem;">No tasks yet — add one in Tasks.</div>', unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="section-label">Recent Notes</div>', unsafe_allow_html=True)
        if notes:
            for note in notes[-3:]:
                content = note[1] if isinstance(note, (list, tuple)) and len(note) > 1 else str(note)
                preview = content[:120] + ("…" if len(content) > 120 else "")
                st.markdown(f'<div class="note-item">{preview}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="note-item" style="color:#8B949E;text-align:center;padding:2rem;">No notes yet — start writing in Notes.</div>', unsafe_allow_html=True)


# AI Chat
elif menu == "AI Chat":
    st.markdown("""
    <div class="page-header">
        <h1>AI Chat</h1>
        <p>Ask Athena anything</p>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        prompt = st.text_area(
            "Your message",
            placeholder="What would you like to know?",
            height=130,
            label_visibility="visible"
        )
        col_btn, col_tip = st.columns([1, 4])
        with col_btn:
            send = st.button("Send  →", use_container_width=True)
        with col_tip:
            st.markdown('<p style="color:#8B949E;font-size:0.8rem;margin-top:0.65rem;">Press Send or Ctrl+Enter</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if send and prompt.strip():
        with st.spinner("Thinking…"):
            answer = ask_ai(prompt)
        st.markdown(f'<div class="chat-response">{answer}</div>', unsafe_allow_html=True)
    elif send and not prompt.strip():
        st.warning("Type a message first.")


# Tasks
elif menu == "Tasks":
    st.markdown("""
    <div class="page-header">
        <h1>Task Manager</h1>
        <p>Track what needs to get done</p>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">New Task</div>', unsafe_allow_html=True)
        col_input, col_add = st.columns([5, 1])
        with col_input:
            task = st.text_input("Task description", placeholder="e.g. Review design proposal", label_visibility="collapsed")
        with col_add:
            add = st.button("Add Task", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if add:
        if task.strip():
            add_task(task)
            st.success("✓ Task added successfully.")
        else:
            st.warning("Enter a task description first.")

    st.markdown("<div style='margin-top:1.5rem;'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">All Tasks</div>', unsafe_allow_html=True)

    tasks = get_tasks()
    if tasks:
        df = pd.DataFrame(tasks, columns=["ID", "Task", "Status"])
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "ID": st.column_config.NumberColumn("ID", width="small"),
                "Task": st.column_config.TextColumn("Task", width="large"),
                "Status": st.column_config.TextColumn("Status"),
            }
        )
    else:
        st.markdown('<div class="note-item" style="color:#8B949E;text-align:center;padding:2.5rem;">No tasks yet. Add your first one above.</div>', unsafe_allow_html=True)


# Notes
elif menu == "Notes":
    st.markdown("""
    <div class="page-header">
        <h1>Notes</h1>
        <p>Capture ideas before they slip away</p>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">New Note</div>', unsafe_allow_html=True)
        note = st.text_area("Note content", placeholder="Write anything…", height=150, label_visibility="collapsed")
        save = st.button("Save Note")
        st.markdown('</div>', unsafe_allow_html=True)

    if save:
        if note.strip():
            add_note(note)
            st.success("✓ Note saved.")
        else:
            st.warning("Write something first.")

    st.markdown("<div style='margin-top:1.5rem;'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">Saved Notes</div>', unsafe_allow_html=True)

    notes = get_notes()
    if notes:
        for i, note_row in enumerate(reversed(notes)):
            content = note_row[1] if isinstance(note_row, (list, tuple)) and len(note_row) > 1 else str(note_row)
            note_id = note_row[0] if isinstance(note_row, (list, tuple)) else i + 1
            st.markdown(f"""
            <div class="note-item">
                <div style="font-size:0.7rem;color:#8B949E;margin-bottom:0.4rem;font-weight:600;">#{note_id}</div>
                {content}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="note-item" style="color:#8B949E;text-align:center;padding:2.5rem;">No notes yet. Write your first one above.</div>', unsafe_allow_html=True)


# Weather
elif menu == "Weather":
    st.markdown("""
    <div class="page-header">
        <h1>Weather</h1>
        <p>Current conditions for any city</p>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        col_city, col_btn = st.columns([5, 1])
        with col_city:
            city = st.text_input("City", placeholder="e.g. Mumbai, London, Tokyo", label_visibility="collapsed")
        with col_btn:
            check = st.button("Search", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if check and city.strip():
        with st.spinner(f"Fetching weather for {city}…"):
            weather = get_weather(city)

        st.markdown("<div style='margin-top:1.5rem;'></div>", unsafe_allow_html=True)

        w1, w2, w3 = st.columns(3)
        with w1:
            st.markdown(f"""
            <div class="weather-stat">
                <div style="font-size:2rem;margin-bottom:0.5rem;">🌡️</div>
                <div class="weather-stat-value">{weather['temp']}°C</div>
                <div class="weather-stat-label">Temperature</div>
            </div>
            """, unsafe_allow_html=True)
        with w2:
            st.markdown(f"""
            <div class="weather-stat">
                <div style="font-size:2rem;margin-bottom:0.5rem;">💧</div>
                <div class="weather-stat-value">{weather['humidity']}%</div>
                <div class="weather-stat-label">Humidity</div>
            </div>
            """, unsafe_allow_html=True)
        with w3:
            st.markdown(f"""
            <div class="weather-stat">
                <div style="font-size:2rem;margin-bottom:0.5rem;">🌤️</div>
                <div class="weather-stat-value" style="font-size:1.1rem;padding-top:0.5rem;">{weather['condition']}</div>
                <div class="weather-stat-label">Condition</div>
            </div>
            """, unsafe_allow_html=True)
    elif check:
        st.warning("Enter a city name to check the weather.")
