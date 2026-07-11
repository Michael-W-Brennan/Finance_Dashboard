import streamlit as st
import json
import os
import streamlit.components.v1 as components


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Classical Music Explorer",
    page_icon="🎼",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================
# CUSTOM STYLE
# =====================================================

st.markdown(
    """
    <style>

    .main {
        background-color: #0e1117;
    }


    h1 {
        color: #f4d03f;
        font-family: Georgia, serif;
    }


    h2, h3 {
        color: #f7dc6f;
        font-family: Georgia, serif;
    }


    .composer-card {

        background:
        linear-gradient(
            145deg,
            #1b1f27,
            #11151c
        );

        border-radius:15px;

        padding:20px;

        margin-bottom:20px;

        box-shadow:
        0px 0px 15px rgba(0,0,0,.5);

    }


    .small-text {

        color:#cccccc;

        font-size:16px;

        line-height:1.5;

    }


    .tag {

        background:#4a235a;

        padding:6px 12px;

        border-radius:20px;

        color:white;

        display:inline-block;

        margin-right:5px;

        font-size:13px;

    }


    </style>
    """,
    unsafe_allow_html=True
)



# =====================================================
# LOAD DATABASE
# =====================================================

@st.cache_data
def load_music_database():

    file_path = "composers.json"

    if not os.path.exists(file_path):

        st.error(
            "Cannot find composers.json. "
            "Place it in the same folder as this script."
        )

        st.stop()


    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)



music = load_music_database()



# =====================================================
# SESSION STORAGE
# =====================================================

if "favorites" not in st.session_state:

    st.session_state.favorites = []



# =====================================================
# HEADER
# =====================================================

st.title("🎼 Classical Music Explorer")

st.markdown(
    """
    Explore the greatest composers in Western music history.

    Select an era from the sidebar to discover composers,
    learn about their style, view portraits, and listen
    to famous works directly inside the app.
    """
)



# =====================================================
# SIDEBAR MENU
# =====================================================

st.sidebar.title("🎻 Music Eras")


eras = list(music.keys())


selected_era = st.sidebar.selectbox(
    "Choose a time period",
    eras
)


era_info = music[selected_era]


st.sidebar.markdown("---")


st.sidebar.info(
    f"""
    **{selected_era}**

    {era_info['years']}

    {era_info['description']}
    """
)


st.sidebar.markdown("---")


search_term = st.sidebar.text_input(
    "🔎 Search composer"
)


st.sidebar.markdown("---")


st.sidebar.write(
    f"⭐ Favorites: {len(st.session_state.favorites)}"
)
# =====================================================
# COMPOSER FILTERING
# =====================================================


composers = era_info["composers"]



# Search filter

if search_term:

    composers = [

        c for c in composers

        if search_term.lower()
        in c["name"].lower()

    ]



# =====================================================
# ERA SUMMARY DASHBOARD
# =====================================================


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Time Period",
        selected_era
    )


with col2:

    st.metric(
        "Years",
        era_info["years"]
    )


with col3:

    st.metric(
        "Composers",
        len(composers)
    )



st.divider()



# =====================================================
# COMPOSER DISPLAY
# =====================================================


for composer in composers:


    with st.container():


        st.markdown(
            '<div class="composer-card">',
            unsafe_allow_html=True
        )



        left, right = st.columns(
            [1, 3]
        )



        # ---------------------------------------------
        # IMAGE
        # ---------------------------------------------

        with left:

            try:

                st.image(
                    composer["image"],
                    width=220
                )

            except Exception:

                st.write(
                    "🖼️ Image unavailable"
                )



        # ---------------------------------------------
        # DETAILS
        # ---------------------------------------------

        with right:


            st.subheader(
                composer["name"]
            )


            st.markdown(
                f"""
                <div class="small-text">

                <b>Born:</b> {composer["birth"]}

                <br>

                <b>Style:</b> 
                <span class="tag">
                {composer["style"]}
                </span>


                <br><br>

                {composer["about"]}

                </div>
                """,

                unsafe_allow_html=True

            )



            st.write("")



            # -----------------------------------------
            # FAVORITES
            # -----------------------------------------


            fav_key = (
                composer["name"]
                +
                "_favorite"
            )


            if composer["name"] in st.session_state.favorites:


                if st.button(
                    "⭐ Remove Favorite",
                    key=fav_key
                ):

                    st.session_state.favorites.remove(
                        composer["name"]
                    )

                    st.rerun()



            else:


                if st.button(
                    "☆ Add Favorite",
                    key=fav_key
                ):

                    st.session_state.favorites.append(
                        composer["name"]
                    )

                    st.rerun()



        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )



        # =================================================
        # MUSIC PLAYER SECTION
        # =================================================


        st.markdown(
            "### 🎧 Listen"
        )


        song_titles = [

            song["title"]

            for song in composer["songs"]

        ]



        selected_song = st.selectbox(

            "Choose a composition",

            song_titles,

            key=composer["name"]

        )



        selected_song_data = next(

            song

            for song in composer["songs"]

            if song["title"] == selected_song

        )



        video_id = selected_song_data["video_id"]



        # Embedded YouTube player


        components.html(

            f"""

            <iframe

            width="100%"

            height="400"

            src="https://www.youtube.com/embed/{video_id}"

            title="YouTube player"

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

            height=420

        )



        st.divider()
        # =====================================================
# LOWER DASHBOARD SECTION
# =====================================================

st.divider()

st.header("🎼 Explorer Dashboard")



# -----------------------------------------------------
# Collect statistics
# -----------------------------------------------------


all_composers = []


for era in music.values():

    for composer in era["composers"]:

        all_composers.append(composer)



total_composers = len(all_composers)



styles = {}


for composer in all_composers:

    style = composer["style"]

    styles[style] = styles.get(style, 0) + 1



# -----------------------------------------------------
# Dashboard metrics
# -----------------------------------------------------


dash1, dash2, dash3 = st.columns(3)



with dash1:

    st.metric(
        "Total Composers",
        total_composers
    )


with dash2:

    st.metric(
        "Historical Periods",
        len(music)
    )


with dash3:

    st.metric(
        "Favorite Composers",
        len(st.session_state.favorites)
    )



st.divider()



# =====================================================
# RANDOM COMPOSER FEATURE
# =====================================================


st.header("🎲 Discover a Composer")



import random



if st.button(
    "Find Random Composer"
):

    random_composer = random.choice(
        all_composers
    )


    st.session_state.random_composer = (
        random_composer
    )



if "random_composer" in st.session_state:


    rc = st.session_state.random_composer



    col_a, col_b = st.columns(
        [1,3]
    )


    with col_a:

        st.image(
            rc["image"],
            width=180
        )


    with col_b:

        st.subheader(
            rc["name"]
        )

        st.write(
            f"""
            **Born:** {rc["birth"]}

            **Style:** {rc["style"]}

            {rc["about"]}
            """
        )



st.divider()



# =====================================================
# FAVORITES SECTION
# =====================================================


st.header("⭐ My Favorite Composers")



if len(st.session_state.favorites) == 0:


    st.info(
        "You have not selected any favorites yet."
    )



else:


    favorite_data = [

        c

        for c in all_composers

        if c["name"]
        in st.session_state.favorites

    ]



    fav_columns = st.columns(3)



    for index, composer in enumerate(favorite_data):


        with fav_columns[index % 3]:


            st.image(
                composer["image"],
                width=150
            )


            st.subheader(
                composer["name"]
            )


            st.caption(
                composer["style"]
            )



st.divider()



# =====================================================
# STYLE EXPLORER
# =====================================================


st.header("🎻 Musical Styles")


selected_style = st.selectbox(

    "Explore composers by style",

    sorted(
        styles.keys()
    )

)



matching = [

    c

    for c in all_composers

    if selected_style
    in c["style"]

]



for composer in matching:


    st.write(
        f"🎼 **{composer['name']}** — {composer['style']}"
    )
    # =====================================================
# HISTORICAL TIMELINE
# =====================================================

st.divider()

st.header("📜 Classical Music Timeline")



timeline_data = []


for era_name, era in music.items():

    timeline_data.append(

        {
            "Era": era_name,
            "Years": era["years"],
            "Description": era["description"]
        }

    )



for item in timeline_data:


    with st.expander(

        f"🎼 {item['Era']}  |  {item['Years']}"

    ):

        st.write(
            item["Description"]
        )



st.divider()



# =====================================================
# APP INFORMATION
# =====================================================


st.header("🎼 About Classical Music Explorer")


st.markdown(

"""
### Purpose

Classical Music Explorer is an interactive digital museum
for discovering the history of Western classical music.

### Features

- 🎻 Browse major musical eras
- 🖼️ View composer portraits
- 🎧 Listen to famous works
- ⭐ Save favorite composers
- 🔎 Search composers
- 🎲 Discover random composers
- 📚 Explore musical styles

### Covered Periods

- Medieval
- Renaissance
- Baroque
- Classical
- Romantic
- Impressionist
- 20th Century
- Modern

---

Built with:

🐍 Python  
🌐 Streamlit  
🎼 Classical music history data

"""

)



# =====================================================
# FOOTER
# =====================================================


st.markdown(

"""
<br><br>

<center>

🎼 <b>Classical Music Explorer</b><br>

Explore. Listen. Discover.

</center>

""",

unsafe_allow_html=True

)
