import streamlit as st
import streamlit.components.v1 as components
import json
import os
import random


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Classical Music Explorer",
    page_icon="🎼",
    layout="wide"
)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_database():

    with open(
        "composers.json",
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


music = load_database()



# =========================================================
# SESSION STATE
# =========================================================

if "favorites" not in st.session_state:
    st.session_state.favorites = []



# =========================================================
# CSS
# =========================================================

st.markdown(
"""
<style>

.stApp {

background:
linear-gradient(
135deg,
#090d14,
#121826
);

color:white;

}


h1 {

color:#f4d35e;

font-size:48px;

}


h2 {

color:#f4d35e;

}


.card {

background:

linear-gradient(
145deg,
#171d28,
#10151d
);


padding:25px;

border-radius:20px;

border:1px solid #303846;

margin-bottom:25px;

}



.composer {

font-size:32px;

font-weight:bold;

color:#f4d35e;

}


.badge {

display:inline-block;

background:#273142;

padding:7px 14px;

border-radius:20px;

font-size:13px;

}


.small {

color:#bbbbbb;

}


</style>
""",
unsafe_allow_html=True
)



# =========================================================
# TIMELINE
# =========================================================

timeline = {

    "Medieval":500,
    "Renaissance":1400,
    "Baroque":1600,
    "Classical":1750,
    "Romantic":1820,
    "Modern":1900

}



# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🎼 Music Explorer")


page = st.sidebar.radio(

    "Navigation",

    [
        "Explore",
        "Masterpieces",
        "Statistics"
    ]

)



st.sidebar.divider()



era = st.sidebar.selectbox(

    "Musical Period",

    list(music.keys())

)



search = st.sidebar.text_input(

    "🔎 Search Composer"

)



# collect styles

styles=[]

for period in music.values():

    for composer in period["composers"]:

        styles.append(
            composer["style"]
        )


styles = sorted(set(styles))



style_filter = st.sidebar.multiselect(

    "🎻 Style",

    styles

)



mood_filter = st.sidebar.multiselect(

    "🎭 Mood",

    [
        "Peaceful",
        "Powerful",
        "Dramatic",
        "Romantic"
    ]

)



if st.sidebar.button(
    "🎲 Random Composer"
):

    all_composers=[]

    for period in music.values():

        all_composers.extend(
            period["composers"]
        )


    random_pick=random.choice(
        all_composers
    )


    st.sidebar.success(

        random_pick["name"]

    )



st.sidebar.divider()


st.sidebar.subheader(
    "⭐ Favorites"
)



if st.session_state.favorites:

    for fav in st.session_state.favorites:

        st.sidebar.write(
            "🎵",
            fav
        )

else:

    st.sidebar.write(
        "No favorites yet"
    )



# =========================================================
# MASTERPIECE PAGE
# =========================================================

if page == "Masterpieces":

    st.title(
        "🏆 Classical Masterpieces"
    )


    for period in music.values():

        for composer in period["composers"]:

            for song in composer["songs"]:

                st.write(

                    f"🎵 **{song['title']}** — {composer['name']}"

                )

                st.link_button(

                    "Listen on YouTube",

                    song["youtube"]

                )


    st.stop()



# =========================================================
# STATISTICS PAGE
# =========================================================

if page == "Statistics":


    total_composers=0

    total_songs=0


    for period in music.values():

        total_composers += len(
            period["composers"]
        )


        for composer in period["composers"]:

            total_songs += len(
                composer["songs"]
            )


    st.title(
        "📊 Classical Music Statistics"
    )


    a,b,c = st.columns(3)


    a.metric(
        "Composers",
        total_composers
    )


    b.metric(
        "Music Samples",
        total_songs
    )


    c.metric(
        "Historical Periods",
        len(music)
    )


    st.stop()



# =========================================================
# EXPLORE PAGE
# =========================================================


period = music[era]


st.title(
    "🎼 Classical Music Explorer"
)



st.markdown(

f"""

<div class="card">

<h2>{era}</h2>


<p class="small">

{period['years']}

</p>


<p>

{period['description']}

</p>


</div>

""",

unsafe_allow_html=True

)



# Timeline


st.subheader(
    "📜 Musical Timeline"
)


year = st.slider(

    "Travel through history",

    500,

    2026,

    timeline.get(
        era,
        1750
    )

)


closest=min(

    timeline,

    key=lambda x:

    abs(timeline[x]-year)

)


st.info(

f"{year} is closest to the {closest} era"

)



# =========================================================
# COMPOSERS
# =========================================================


for composer in period["composers"]:


    name = composer["name"]


    if search:

        if search.lower() not in name.lower():

            continue



    if style_filter:

        if composer["style"] not in style_filter:

            continue



    if mood_filter:

        if composer["mood"] not in mood_filter:

            continue



    st.markdown(

    f"""

    <div class="card">


    <div class="composer">

    {name}

    </div>


    <br>


    <span class="badge">

    {composer['style']}

    </span>


    <br><br>


    <p class="small">

    Born: {composer['birth']}

    </p>


    <p>

    {composer['about']}

    </p>


    </div>

    """,

    unsafe_allow_html=True

    )



    # Image support

    image_path = (

        "images/" +

        composer["image"]

    )


    if os.path.exists(image_path):

        st.image(
            image_path,
            width=250
        )



    # Favorite

    if st.button(

        "⭐ Add Favorite",

        key=name

    ):


        if name not in st.session_state.favorites:

            st.session_state.favorites.append(name)



    # Music


    st.subheader(
        "🎧 Listen"
    )


    songs={}


    for song in composer["songs"]:

        songs[
            song["title"]
        ] = song["youtube"]



    selection=st.selectbox(

        "Choose piece",

        list(songs.keys()),

        key="song_"+name

    )


    youtube=songs[selection]



    st.link_button(

        "▶ Open YouTube",

        youtube

    )


    query=youtube.split(
        "search_query="
    )[-1]



    components.html(

    f"""

    <iframe

    width="100%"

    height="400"

    src="https://www.youtube.com/embed?listType=search&list={query}"

    frameborder="0"

    allowfullscreen>

    </iframe>

    """,

    height=420

    )


    st.divider()
