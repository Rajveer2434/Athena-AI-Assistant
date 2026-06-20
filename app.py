import streamlit as st
import pandas as pd

from modules.ai_chat import ask_ai
from modules.task_manager import add_task,get_tasks
from modules.notes_manager import add_note,get_notes
from modules.weather import get_weather
from utils.db import create_tables

create_tables()

st.set_page_config(
    page_title="Athena AI",
    layout="wide"
)

st.title("🤖 Athena AI Assistant")

menu = st.sidebar.radio(
    "Select",
    [
        "Dashboard",
        "AI Chat",
        "Tasks",
        "Notes",
        "Weather"
    ]
)

# Dashboard
if menu == "Dashboard":

    st.header("Overview")

    tasks = get_tasks()
    notes = get_notes()

    c1,c2 = st.columns(2)

    c1.metric(
        "Total Tasks",
        len(tasks)
    )

    c2.metric(
        "Total Notes",
        len(notes)
    )

# AI Chat
elif menu == "AI Chat":

    st.header("Chat Assistant")

    prompt = st.text_area(
        "Ask Anything"
    )

    if st.button("Generate"):

        with st.spinner():

            answer = ask_ai(prompt)

        st.write(answer)

# Tasks
elif menu == "Tasks":

    st.header("Task Manager")

    task = st.text_input(
        "Task"
    )

    if st.button("Add Task"):

        add_task(task)

        st.success(
            "Task Added"
        )

    tasks = get_tasks()

    df = pd.DataFrame(
        tasks,
        columns=[
            "ID",
            "Task",
            "Status"
        ]
    )

    st.dataframe(df)

# Notes
elif menu == "Notes":

    st.header("Notes")

    note = st.text_area(
        "Write Note"
    )

    if st.button("Save Note"):

        add_note(note)

        st.success(
            "Saved"
        )

    notes = get_notes()

    st.write(notes)

# Weather
elif menu == "Weather":

    st.header("Weather")

    city = st.text_input(
        "City Name"
    )

    if st.button("Check Weather"):

        weather = get_weather(city)

        st.metric(
            "Temperature",
            f"{weather['temp']} °C"
        )

        st.metric(
            "Humidity",
            f"{weather['humidity']} %"
        )

        st.write(
            weather["condition"]
        )