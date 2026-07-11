import streamlit as st
import json
import os
import requests
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
# DESIGN
# =====================================================

st.markdown(
"""
<style>

body {
    background-color:#0c1018;
}


.main {
    background-color:#0c1018;
}


h1 {

    color:#e8c46a;
    font-family:Georgia, serif;
    text-align:center;

}


h2,h3 {

    color:#e8c46a;
    font-family:Georgia, serif;

}


.composer-card {

    background:
    linear-gradient(
        145deg,
        #171c27,
        #10141d
    );

    border-radius:18px;

    padding:30px;

    margin-bottom:25px;

}


.label {

    color:#e8c46a;
    font-weight:bold;

}


</style>

""",
unsafe_allow_html=True
)



# =====================================================
# LOAD JSON
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
        encoding="utf-8"
    ) as f:

        return json.load(f)



music = load_database()



# =====================================================
# AUTOMATIC PORTRAIT LOOKUP
# =====================================================


@st.cache_data
def get_portrait(person_name):

    try:

        url = (
            "https://en.wikipedia.org/w/api.php"
        )


        params = {

            "action":"query",

            "format":"json",

            "prop":"pageimages",

            "piprop":"original",

            "titles":person_name

        }


        response = requests.get(

            url,

            params=params,

            timeout=5

        )


        data = response.json()



        pages = data["query"]["pages"]



        for page in pages.values():


            if "original" in page:

                return page["original"]["source"]



    except Exception:

        pass



    return None



# =====================================================
# HEADER
# =====================================================


st.title(
    "🎼 Classical Music Explorer"
)


st.markdown(

"""
<center>

A digital museum exploring the composers,
styles, and masterpieces of classical music.

</center>

""",

unsafe_allow_html=True

)



st.divider()



# =====================================================
# SIDEBAR
# =====================================================


st.sidebar.title(
    "🎻 Time Periods"
)



eras = list(
    music.keys()
)



selected_era = st.sidebar.radio(

    "Choose an era",

    eras

)



era = music[selected_era]



st.sidebar.divider()



st.sidebar.write(

era["years"]

)


st.sidebar.caption(

era["description"]

)



st.header(

f"🎼 {selected_era}"

)


st.caption(

era["description"]

)
# =====================================================
# COMPOSER EXHIBITS
# =====================================================


for composer in era["composers"]:


    st.markdown(

        '<div class="composer-card">',

        unsafe_allow_html=True

    )


    image_col, info_col = st.columns(

        [1, 2]

    )


    # =================================================
    # PORTRAIT
    # =================================================


    with image_col:


        portrait = get_portrait(

            composer["name"]

        )


        if portrait:


            st.image(

                portrait,

                width=260

            )


        else:


            st.info(

                "Portrait unavailable"

            )



    # =================================================
    # INFORMATION
    # =================================================


    with info_col:


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
        Style:
        </span>

        {composer["style"]}


        <br><br>


        {composer["about"]}


        """,

        unsafe_allow_html=True

        )



        st.write("")



        st.markdown(

            "### 🎵 Major Works"

        )


        for song in composer["songs"]:


            st.write(

                "🎼 " + song["title"]

            )



    st.markdown(

        "</div>",

        unsafe_allow_html=True

    )


    st.divider()
    # =====================================================
# LISTENING EXPERIENCE
# =====================================================


st.divider()


st.header(
    "🎧 Listen to the Music"
)


st.markdown(

"""
Choose a composer and listen to a featured performance
directly inside the exhibit.

"""

)



# -----------------------------------------------------
# Composer selector
# -----------------------------------------------------


composer_names = [

    composer["name"]

    for composer in era["composers"]

]


chosen_composer_name = st.selectbox(

    "Composer",

    composer_names

)



chosen_composer = next(

    c

    for c in era["composers"]

    if c["name"] == chosen_composer_name

)



# -----------------------------------------------------
# Song selector
# -----------------------------------------------------


song_titles = [

    song["title"]

    for song in chosen_composer["songs"]

]


chosen_song_title = st.selectbox(

    "Composition",

    song_titles

)



chosen_song = next(

    song

    for song in chosen_composer["songs"]

    if song["title"] == chosen_song_title

)



# -----------------------------------------------------
# YouTube Player
# -----------------------------------------------------


video_id = chosen_song["video_id"]



components.html(

f"""

<iframe

width="100%"

height="500"

src="https://www.youtube.com/embed/{video_id}"

frameborder="0"

allow="accelerometer;
autoplay;
clipboard-write;
encrypted-media;
gyroscope;
picture-in-picture"

allowfullscreen>

</iframe>

""",

height=520

)



# -----------------------------------------------------
# YouTube link
# -----------------------------------------------------


st.markdown(

f"""

▶️

[Open this performance directly on YouTube]

({chosen_song["youtube"]})

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

Discover composers. Explore history. Listen.

</center>

""",

unsafe_allow_html=True

)
