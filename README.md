# Macro Terminal

A slick, dark, "Bloomberg terminal"-inspired macro dashboard built with
Streamlit. Shows the Treasury yield curve, inflation, Fed funds rate,
unemployment, and the S&P 500 — all from free public data with **no API
keys required**.

## Data sources
- **FRED** (Federal Reserve Bank of St. Louis) — pulled via the public
  `fredgraph.csv` endpoint, no key needed.
- **Treasury.gov** — daily par yield curve rates via their public CSV feed.
- **yfinance** — S&P 500 index history.

## Run locally

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL Streamlit prints (usually `http://localhost:8501`).

## Deploy for free (Streamlit Community Cloud)
1. Push this folder to a public GitHub repo.
2. Go to [share.streamlit.io](https://share.streamlit.io), sign in with
   GitHub, and click "New app."
3. Point it at your repo and `app.py`. No secrets/API keys needed.

## Project structure
```
app.py       # page layout and orchestration
data.py      # all data fetching, cached hourly via st.cache_data
theme.py     # dark "terminal" CSS + shared Plotly styling
requirements.txt
.streamlit/config.toml   # native dark theme fallback
```

## Notes / known rough edges
- The Treasury.gov CSV endpoint's URL shape has changed before — if the
  yield curve panel errors out, check the current path at
  home.treasury.gov's Interest Rate Data page and update the URL in
  `data.py::fetch_treasury_par_yield_curve`.
- All fetches are cached for 1 hour (`ttl=3600` in `data.py`). Lower this
  while iterating locally if you want fresher pulls, raise it before a
  demo to avoid hammering the source sites.
- Every panel degrades gracefully (shows a placeholder instead of
  crashing) if a given source is unreachable.
