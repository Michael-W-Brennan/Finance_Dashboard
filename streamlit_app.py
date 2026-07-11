import streamlit as st
import urllib.parse


# ----------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------

st.set_page_config(
    page_title="Classical Music Explorer",
    page_icon="🎼",
    layout="wide"
)


# ----------------------------------------------------
# CUSTOM CSS
# ----------------------------------------------------

st.markdown("""
<style>

body {
    background-color:#0e1117;
}

.main {
    background-color:#0e1117;
}

h1 {
    color:#f5d76e;
    font-size:45px;
}

h2 {
    color:#f5d76e;
}

h3 {
    color:#d8d8d8;
}

.sidebar .sidebar-content {
    background-color:#111827;
}

div[data-testid="stDataFrame"] {
    border-radius:15px;
}

.stButton button {
    border-radius:20px;
    background:#f5d76e;
    color:black;
    font-weight:bold;
}

.card {
    background:#161b22;
    padding:20px;
    border-radius:15px;
    margin-bottom:15px;
    border:1px solid #30363d;
}

.small {
    color:#bbbbbb;
    font-size:14px;
}

</style>
""", unsafe_allow_html=True)


# ----------------------------------------------------
# DATA
# ----------------------------------------------------

music = {

"Medieval": {

"years":"500 - 1400",

"description":
"Music of the Middle Ages focused heavily on sacred traditions, Gregorian chant, and the development of early notation systems.",

"composers":[

["Hildegard von Bingen",
"Medieval Sacred",
"German abbess and composer known for visionary chants.",
"Ordo Virtutum"],

["Guillaume de Machaut",
"Ars Nova",
"Important French composer who expanded rhythmic complexity.",
"Messe de Nostre Dame"],

["Léonin",
"Early Polyphony",
"One of the first known composers of multi-part music.",
"Viderunt Omnes"]

]

},


"Renaissance": {

"years":"1400 - 1600",

"description":
"Renaissance music emphasized balance, vocal harmony, and expressive polyphony.",

"composers":[

["Josquin des Prez",
"Renaissance Polyphony",
"Master of vocal counterpoint and influential composer.",
"Ave Maria"],

["Giovanni Pierluigi da Palestrina",
"Sacred Choral",
"Famous for elegant church compositions.",
"Missa Papae Marcelli"],

["Thomas Tallis",
"English Renaissance",
"Known for rich and dramatic sacred music.",
"Spem in Alium"]

]

},


"Baroque": {

"years":"1600 - 1750",

"description":
"The Baroque era introduced opera, concerto form, and elaborate musical expression.",

"composers":[

["Johann Sebastian Bach",
"Counterpoint / Organ / Orchestra",
"One of history's greatest composers, famous for mathematical precision.",
"Brandenburg Concertos"],

["George Frideric Handel",
"Opera / Oratorio",
"Known worldwide for Messiah and dramatic works.",
"Messiah"],

["Antonio Vivaldi",
"Violin Concerto",
"Created The Four Seasons and influenced concerto writing.",
"The Four Seasons"]

]

},


"Classical": {

"years":"1750 - 1820",

"description":
"Classical music emphasized clarity, structure, balance, and elegant melodies.",

"composers":[

["Wolfgang Amadeus Mozart",
"Symphony / Opera",
"Child prodigy who created some of the world's most beloved music.",
"Eine kleine Nachtmusik"],

["Joseph Haydn",
"Symphony / String Quartet",
"Father of the symphony and string quartet.",
"Surprise Symphony"],

["Ludwig van Beethoven",
"Symphony / Piano",
"Bridge between Classical and Romantic periods.",
"Symphony No. 9"]

]

},


"Romantic": {

"years":"1820 - 1900",

"description":
"Romantic composers focused on emotion, individuality, larger orchestras, and dramatic storytelling.",

"composers":[

["Frédéric Chopin",
"Piano Romanticism",
"Poet of the piano known for expressive works.",
"Nocturnes"],

["Johannes Brahms",
"Symphonic Romantic",
"Combined classical structure with romantic emotion.",
"Symphony No. 4"],

["Pyotr Tchaikovsky",
"Orchestra / Ballet",
"Famous for emotional melodies and ballet masterpieces.",
"Swan Lake"]

]

},


"Impressionist / Modern": {

"years":"1900 - Present",

"description":
"Modern composers explored new harmonies, unusual structures, and experimental sounds.",

"composers":[

["Claude Debussy",
"Impressionism",
"Created atmospheric music using new harmonic colors.",
"Clair de Lune"],

["Igor Stravinsky",
"Modernism",
"Revolutionized rhythm and orchestral writing.",
"The Rite of Spring"],

["Dmitri Shostakovich",
"20th Century Symphony",
"Known for powerful symphonies and emotional depth.",
"Symphony No. 5"]

]

}

}



# ----------------------------------------------------
# SIDEBAR
# ----------------------------------------------------

st.sidebar.title("🎼 Music Library")

st.sidebar.write(
"""
Explore the major periods of Western classical music.

Select an era:
"""
)


era = st.sidebar.radio(
    "Choose Period",
    list(music.keys())
)


st.sidebar.markdown("---")

st.sidebar.info(
"""
Tip:
Click the YouTube links to hear examples of each composer's style.
"""
)


# ----------------------------------------------------
# MAIN DISPLAY
# ----------------------------------------------------

info = music[era]


st.title("🎼 Classical Music Explorer")

st.subheader(
f"{era} Period ({info['years']})"
)


st.markdown(
f"""
<div class="card">

<h3>About this Era</h3>

<p>{info['description']}</p>

</div>
""",
unsafe_allow_html=True
)



# ----------------------------------------------------
# TABLE
# ----------------------------------------------------

st.subheader("Famous Composers")


table = []

for c in info["composers"]:

    table.append(
        {
        "Composer":c[0],
        "Style":c[1],
        "Notes":c[2],
        "Famous Work":c[3]
        }
    )


st.table(table)



# ----------------------------------------------------
# YOUTUBE LINKS
# ----------------------------------------------------

st.subheader("🎧 Listen")


for composer in info["composers"]:

    name = composer[0]
    piece = composer[3]


    query = urllib.parse.quote(
        f"{name} {piece} classical music"
    )


    youtube = (
        "https://www.youtube.com/results?search_query="
        + query
    )


    st.markdown(
        f"""
        <div class="card">

        <h3>{name}</h3>

        <p>
        Recommended piece:
        <b>{piece}</b>
        </p>

        <a href="{youtube}" target="_blank">
        ▶ Search YouTube
        </a>

        </div>
        """,
        unsafe_allow_html=True
    )



# ----------------------------------------------------
# FOOTER
# ----------------------------------------------------

st.markdown("---")

st.markdown(
"""
<center>

🎻 Classical Music Explorer  
<br>
Built entirely with Python + Streamlit

</center>
""",
unsafe_allow_html=True
)
