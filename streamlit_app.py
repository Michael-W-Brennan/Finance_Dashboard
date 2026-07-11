import streamlit as st
import json
import os
import streamlit.components.v1 as components



# =====================================================
# PAGE SETTINGS
# =====================================================

st.set_page_config(
    page_title="Classical Music Explorer",
    page_icon="🎼",
    layout="wide"
)



# =====================================================
# CUSTOM DESIGN
# =====================================================

st.markdown(
    """

<style>


body {

    background-color:#0b0e14;

}


.main {

    background-color:#0b0e14;

}



/* Main title */

h1 {

    color:#e7c66b;

    font-family:Georgia, serif;

    text-align:center;

}



h2, h3 {

    color:#e7c66b;

    font-family:Georgia, serif;

}



/* Composer card */


.composer-card {

    background:

    linear-gradient(
        135deg,
        #171b26,
        #10131a
    );


    border-radius:18px;


    padding:30px;


    margin-bottom:30px;


    border:

    1px solid rgba(255,255,255,.08);


}



/* Information labels */


.label {

    color:#e7c66b;

    font-weight:bold;

}



/* Era buttons */

section[data-testid="stSidebar"] {

    background-color:#11151d;

}



</style>

""",

unsafe_allow_html=True

)



# =====================================================
# LOAD JSON DATABASE
# =====================================================


@st.cache_data

def load_database():


    if not os.path.exists(
        "composers.json"
    ):

        st.error(
            "Missing composers.json"
        )

        st.stop()



    with open(
        "composers.json",
        "r",
        encoding="utf-8"
    ) as file:


        return json.load(file)




music_database = load_database()



# =====================================================
# HEADER
# =====================================================


st.title(
    "🎼 Classical Music Explorer"
)


st.markdown(
    """
    <center>

    Explore the great composers of Western classical music.

    Choose a historical period from the left menu
    and enter a musical exhibit.

    </center>
    """,

    unsafe_allow_html=True

)



st.divider()



# =====================================================
# LEFT MENU
# =====================================================


st.sidebar.title(
    "🎻 Time Periods"
)



eras = list(
    music_database.keys()
)



selected_era = st.sidebar.radio(

    "Select an era",

    eras

)



# Current era data

era_data = music_database[selected_era]



# Sidebar description

st.sidebar.divider()


st.sidebar.markdown(

f"""

### {selected_era}


**Period**

{era_data["years"]}


---

{era_data["description"]}


"""

)



# =====================================================
# MAIN AREA HEADER
# =====================================================


st.header(
    f"🎼 {selected_era}"
)



st.caption(

era_data["description"]

)
# =====================================================
# COMPOSER EXHIBIT DISPLAY
# =====================================================


for composer in era_data["composers"]:


    st.markdown(
        '<div class="composer-card">',
        unsafe_allow_html=True
    )



    image_column, info_column = st.columns(

        [1, 2]

    )



    # =================================================
    # PORTRAIT
    # =================================================


    with image_column:


        try:

            st.image(

                composer["image"],

                width=260

            )


        except Exception:


            st.warning(

                "Portrait unavailable"

            )



    # =================================================
    # COMPOSER INFORMATION
    # =================================================


    with info_column:


        st.subheader(

            composer["name"]

        )


        st.markdown(

        f"""

        <span class="label">
        Born:
        </span>

        {composer["birth"]}


        <br><br>


        <span class="label">
        Musical Style:
        </span>

        {composer["style"]}


        <br><br>


        {composer["about"]}


        """,

        unsafe_allow_html=True

        )



        st.write("")



        st.markdown(

            "### 🎵 Famous Works"

        )



        for song in composer["songs"]:


            st.write(

                "• " + song["title"]

            )



    st.markdown(

        "</div>",

        unsafe_allow_html=True

    )



    st.divider()
    # =====================================================
# MUSIC LISTENING SECTION
# =====================================================


st.divider()


st.header(
    "🎧 Listen to the Music"
)



st.markdown(

"""
Select a composer above to explore their famous works.
Choose a piece below to play it directly inside the exhibit.

"""

)



# =====================================================
# CREATE GLOBAL MUSIC SELECTOR
# =====================================================


composer_names = [

    composer["name"]

    for composer in era_data["composers"]

]



selected_composer_name = st.selectbox(

    "Choose a composer",

    composer_names

)



selected_composer = next(

    composer

    for composer in era_data["composers"]

    if composer["name"] == selected_composer_name

)



song_names = [

    song["title"]

    for song in selected_composer["songs"]

]



selected_song_name = st.selectbox(

    "Choose a composition",

    song_names

)



selected_song = next(

    song

    for song in selected_composer["songs"]

    if song["title"] == selected_song_name

)



# =====================================================
# YOUTUBE EMBED PLAYER
# =====================================================


video_id = selected_song["video_id"]



components.html(

f"""

<div style="
display:flex;
justify-content:center;
">

<iframe

width="900"

height="500"

src="https://www.youtube.com/embed/{video_id}"

title="Classical Music Player"

frameborder="0"

allow=

"accelerometer;
autoplay;
clipboard-write;
encrypted-media;
gyroscope;
picture-in-picture"

allowfullscreen>

</iframe>


</div>

""",

height=520

)



# =====================================================
# EXTERNAL LINK
# =====================================================


st.markdown(

f"""

▶️

[Open this performance on YouTube]

({selected_song["youtube"]})

"""

)



# =====================================================
# FOOTER
# =====================================================


st.divider()


st.markdown(

"""

<center>

🎼 Classical Music Explorer

<br>

A digital museum of composers and their masterpieces

</center>

""",

unsafe_allow_html=True

)
