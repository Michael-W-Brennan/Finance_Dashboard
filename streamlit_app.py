import streamlit as st
import datetime
import random

# --------------------------------------------------
# Page Setup
# --------------------------------------------------

st.set_page_config(
    page_title="Simple Streamlit Demo",
    page_icon="🐍",
    layout="wide",
)

# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("Simple Streamlit Application")
st.write("This example uses only Streamlit and Python's standard library.")

st.divider()

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

st.sidebar.header("Controls")

name = st.sidebar.text_input("Your Name", "Guest")

age = st.sidebar.slider(
    "Age",
    min_value=1,
    max_value=100,
    value=25,
)

show_time = st.sidebar.checkbox("Show Current Time", True)

number = st.sidebar.number_input(
    "Favorite Number",
    value=10,
)

# --------------------------------------------------
# Main Area
# --------------------------------------------------

st.header("Welcome")

st.write(f"Hello **{name}**!")

st.write(f"You are **{age}** years old.")

st.write(f"Your favorite number is **{number}**.")

if show_time:
    now = datetime.datetime.now()
    st.success(now.strftime("%A, %B %d, %Y"))
    st.info(now.strftime("%I:%M:%S %p"))

st.divider()

# --------------------------------------------------
# Buttons
# --------------------------------------------------

st.header("Buttons")

if st.button("Generate Random Number"):
    st.write(random.randint(1, 100))

if st.button("Roll Dice"):
    st.write(f"🎲 {random.randint(1,6)}")

st.divider()

# --------------------------------------------------
# Text Input
# --------------------------------------------------

st.header("Echo")

message = st.text_area("Type something")

if message:
    st.write("You typed:")
    st.code(message)

st.divider()

# --------------------------------------------------
# Progress Bar
# --------------------------------------------------

st.header("Progress Example")

progress = st.progress(0)

for i in range(101):
    progress.progress(i)

st.success("Finished!")

st.divider()

# --------------------------------------------------
# Table
# --------------------------------------------------

st.header("Simple Table")

table = [
    {"Item": "Apple", "Price": 1.25},
    {"Item": "Orange", "Price": 0.95},
    {"Item": "Banana", "Price": 0.65},
]

st.table(table)

st.divider()

st.caption("End of demo.")
