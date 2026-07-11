import streamlit as st
import random
import datetime
import math


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Python + Streamlit Showcase",
    page_icon="🐍",
    layout="wide"
)


# ============================================================
# SESSION STATE
# ============================================================

if "click_count" not in st.session_state:
    st.session_state.click_count = 0

if "random_number" not in st.session_state:
    st.session_state.random_number = 0


# ============================================================
# TITLE AREA
# ============================================================

st.title("🐍 Python + Streamlit Showcase")

st.subheader(
    "A tour of built-in Streamlit widgets"
)

st.caption(
    "This app uses Streamlit plus Python's standard library only."
)


st.divider()


# ============================================================
# INTRO TEXT
# ============================================================

st.header("Text Components")


st.write(
    "Streamlit allows Python programs to become interactive web applications."
)


st.markdown(
    """
    ### Markdown Support

    You can create:

    - **Bold text**
    - *Italic text*
    - Lists
    - Tables
    - Code blocks
    - Mathematical expressions
    """
)


st.latex(
    r"E = mc^2"
)


with st.expander("Click to see hidden information"):

    st.write(
        """
        Expanders are useful for:
        
        - documentation
        - settings
        - advanced options
        """
    )



# ============================================================
# COLUMNS
# ============================================================

st.header("Column Layout")


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "CPU Usage",
        "42%",
        "+5%"
    )


with col2:

    st.metric(
        "Users",
        "12,450",
        "+320"
    )


with col3:

    st.metric(
        "Revenue",
        "$84K",
        "+12%"
    )



st.divider()


# ============================================================
# BUTTONS
# ============================================================

st.header("Buttons")


if st.button("Click Me"):

    st.session_state.click_count += 1


st.write(
    f"You clicked the button {st.session_state.click_count} times."
)


if st.button("Generate Random Number"):

    st.session_state.random_number = random.randint(
        1,
        1000
    )


st.success(
    f"Random number: {st.session_state.random_number}"
)
# ============================================================
# INPUT WIDGETS
# ============================================================

st.header("Input Widgets")


# ------------------------------------------------------------
# Slider
# ------------------------------------------------------------

st.subheader("Slider")

volume = st.slider(
    "Volume",
    min_value=0,
    max_value=100,
    value=50
)

st.write(
    f"Volume setting: {volume}"
)



# ------------------------------------------------------------
# Range Slider
# ------------------------------------------------------------

st.subheader("Range Slider")

price_range = st.slider(
    "Select a price range",
    0,
    1000,
    (100, 500)
)

st.write(
    f"Selected range: {price_range}"
)



# ------------------------------------------------------------
# Number Input
# ------------------------------------------------------------

st.subheader("Number Input")

age = st.number_input(
    "Enter your age",
    min_value=0,
    max_value=120,
    value=30
)

st.write(
    f"Age: {age}"
)



# ------------------------------------------------------------
# Text Input
# ------------------------------------------------------------

st.subheader("Text Input")

username = st.text_input(
    "Username",
    placeholder="Enter your name"
)


if username:

    st.info(
        f"Hello {username}"
    )



# ------------------------------------------------------------
# Text Area
# ------------------------------------------------------------

st.subheader("Text Area")

message = st.text_area(
    "Write a message"
)


if message:

    st.write(
        "You wrote:"
    )

    st.code(
        message
    )



# ------------------------------------------------------------
# Radio Buttons
# ------------------------------------------------------------

st.subheader("Radio Buttons")


language = st.radio(
    "Choose a programming language",
    [
        "Python",
        "JavaScript",
        "C++",
        "Rust"
    ]
)


st.write(
    f"Selected: {language}"
)



# ------------------------------------------------------------
# Select Box
# ------------------------------------------------------------

st.subheader("Select Box")


country = st.selectbox(
    "Select a country",
    [
        "United States",
        "Canada",
        "United Kingdom",
        "Japan",
        "Germany"
    ]
)


st.write(
    f"Country: {country}"
)



# ------------------------------------------------------------
# Multiselect
# ------------------------------------------------------------

st.subheader("Multiselect")


skills = st.multiselect(
    "Choose skills",
    [
        "Python",
        "Data Science",
        "AI",
        "Web Development",
        "Finance",
        "Game Development"
    ]
)


st.write(
    "Selected skills:",
    skills
)



# ------------------------------------------------------------
# Checkbox
# ------------------------------------------------------------

st.subheader("Checkbox")


dark_mode = st.checkbox(
    "Enable dark mode"
)


if dark_mode:

    st.success(
        "Dark mode enabled"
    )

else:

    st.warning(
        "Dark mode disabled"
    )



# ------------------------------------------------------------
# Date Input
# ------------------------------------------------------------

st.subheader("Date Picker")


birthday = st.date_input(
    "Select a date",
    datetime.date.today()
)


st.write(
    f"Selected date: {birthday}"
)



# ------------------------------------------------------------
# Time Input
# ------------------------------------------------------------

st.subheader("Time Picker")


meeting_time = st.time_input(
    "Choose a time"
)


st.write(
    f"Time selected: {meeting_time}"
)



# ------------------------------------------------------------
# Color Picker
# ------------------------------------------------------------

st.subheader("Color Picker")


color = st.color_picker(
    "Choose a color",
    "#00FF00"
)


st.write(
    f"Selected color: {color}"
)


st.divider()
# ============================================================
# ADVANCED STREAMLIT FEATURES
# ============================================================

st.header("Advanced Components")



# ------------------------------------------------------------
# Progress Bar
# ------------------------------------------------------------

st.subheader("Progress Bar")


progress = st.progress(0)


if st.button("Run Progress Demo"):

    for i in range(101):

        progress.progress(i)

        time.sleep(0.01)


    st.success(
        "Complete!"
    )



# ------------------------------------------------------------
# Status Messages
# ------------------------------------------------------------

st.subheader("Status Messages")


st.success(
    "Operation completed successfully."
)


st.info(
    "This is an information message."
)


st.warning(
    "This is a warning message."
)


st.error(
    "This is an error message."
)



# ------------------------------------------------------------
# Spinner
# ------------------------------------------------------------

st.subheader("Spinner")


if st.button("Run Task"):

    with st.spinner(
        "Processing..."
    ):

        time.sleep(2)


    st.success(
        "Task finished!"
    )



# ------------------------------------------------------------
# Built-in Charts
# ------------------------------------------------------------

st.subheader("Charts")


chart_data = []

for i in range(20):

    chart_data.append(
        random.randint(
            10,
            100
        )
    )


st.line_chart(
    chart_data
)


st.bar_chart(
    chart_data
)


st.area_chart(
    chart_data
)



# ------------------------------------------------------------
# File Upload
# ------------------------------------------------------------

st.subheader("File Upload")


uploaded_file = st.file_uploader(
    "Upload a text file"
)


if uploaded_file:


    contents = uploaded_file.read()


    st.write(
        "File size:",
        len(contents),
        "bytes"
    )


    st.code(
        contents.decode(
            errors="ignore"
        )
    )



# ------------------------------------------------------------
# Tabs
# ------------------------------------------------------------

st.subheader("Tabs")


tab1, tab2, tab3 = st.tabs(
    [
        "Python",
        "Math",
        "About"
    ]
)



with tab1:

    st.write(
        "Python is a powerful general-purpose language."
    )

    st.code(
        """
print("Hello Streamlit")
        """
    )



with tab2:

    st.write(
        "Simple calculator"
    )


    x = st.number_input(
        "Number A",
        value=5
    )


    y = st.number_input(
        "Number B",
        value=10
    )


    st.write(
        "Result:",
        x + y
    )



with tab3:

    st.write(
        "This tab demonstrates Streamlit navigation."
    )



# ------------------------------------------------------------
# Forms
# ------------------------------------------------------------

st.subheader("Forms")


with st.form(
    "user_form"
):


    name = st.text_input(
        "Name"
    )


    occupation = st.selectbox(
        "Occupation",
        [
            "Developer",
            "Engineer",
            "Student",
            "Other"
        ]
    )


    submitted = st.form_submit_button(
        "Submit"
    )



    if submitted:

        st.success(
            f"{name} - {occupation}"
        )



# ------------------------------------------------------------
# Code Display
# ------------------------------------------------------------

st.subheader(
    "Code Viewer"
)


sample_code = """

def hello():

    print("Hello from Python")

"""


st.code(
    sample_code,
    language="python"
)


st.divider()
# ============================================================
# FINAL SHOWCASE FEATURES
# ============================================================


st.header("Final Streamlit Showcase Features")



# ------------------------------------------------------------
# Sidebar Showcase
# ------------------------------------------------------------

st.sidebar.title(
    "🐍 Sidebar Controls"
)


sidebar_choice = st.sidebar.selectbox(
    "Choose a section",
    [
        "Dashboard",
        "Analytics",
        "Settings",
        "About"
    ]
)


sidebar_slider = st.sidebar.slider(
    "Sidebar Slider",
    0,
    100,
    50
)


sidebar_check = st.sidebar.checkbox(
    "Enable notifications"
)


st.sidebar.write(
    f"Selected: {sidebar_choice}"
)


st.sidebar.write(
    f"Slider value: {sidebar_slider}"
)



# ------------------------------------------------------------
# Containers
# ------------------------------------------------------------

st.subheader(
    "Containers"
)


with st.container():

    st.write(
        "This entire area is inside a container."
    )

    st.info(
        "Containers help organize applications."
    )



# ------------------------------------------------------------
# Data Editor
# ------------------------------------------------------------

st.subheader(
    "Interactive Data Editor"
)


sample_table = [

    {
        "Name": "Alice",
        "Score": 95
    },

    {
        "Name": "Bob",
        "Score": 88
    },

    {
        "Name": "Charlie",
        "Score": 76
    }

]


edited_data = st.data_editor(
    sample_table,
    num_rows="dynamic"
)


st.write(
    "Current table:"
)


st.write(
    edited_data
)



# ------------------------------------------------------------
# Random Generator
# ------------------------------------------------------------

st.subheader(
    "Random Generators"
)


random_col1, random_col2 = st.columns(2)



with random_col1:


    if st.button(
        "Roll Dice 🎲"
    ):

        dice = random.randint(
            1,
            6
        )

        st.success(
            f"You rolled {dice}"
        )



with random_col2:


    if st.button(
        "Generate Password 🔐"
    ):


        chars = (
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            "abcdefghijklmnopqrstuvwxyz"
            "0123456789"
        )


        password = ""


        for i in range(12):

            password += random.choice(
                chars
            )


        st.code(
            password
        )



# ------------------------------------------------------------
# Mini Calculator
# ------------------------------------------------------------

st.subheader(
    "Mini Calculator"
)


calc1, calc2 = st.columns(2)



with calc1:

    number_a = st.number_input(
        "Number 1",
        value=10
    )


with calc2:

    number_b = st.number_input(
        "Number 2",
        value=5
    )



operation = st.radio(
    "Operation",
    [
        "Add",
        "Subtract",
        "Multiply",
        "Divide"
    ]
)



if operation == "Add":

    result = number_a + number_b


elif operation == "Subtract":

    result = number_a - number_b


elif operation == "Multiply":

    result = number_a * number_b


else:

    if number_b != 0:

        result = number_a / number_b

    else:

        result = "Cannot divide by zero"



st.success(
    f"Result: {result}"
)



# ------------------------------------------------------------
# Math Demo
# ------------------------------------------------------------

st.subheader(
    "Python Math Demo"
)


angle = st.slider(
    "Angle",
    0,
    360,
    45
)


radians = math.radians(
    angle
)


st.write(
    "Sine:",
    math.sin(radians)
)


st.write(
    "Cosine:",
    math.cos(radians)
)



# ------------------------------------------------------------
# Final Banner
# ------------------------------------------------------------

st.divider()


st.balloons()


st.success(
    """
    🎉 Showcase Complete!

    You have explored many of Streamlit's built-in capabilities
    using only Python and Streamlit.
    """
)


st.caption(
    "End of Python + Streamlit Showcase"
)
