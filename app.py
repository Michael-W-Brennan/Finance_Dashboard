import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

import data as d
from theme import inject_css, plotly_layout, ACCENT, ACCENT_2, NEGATIVE

st.set_page_config(
    page_title="Macro Terminal",
    page_icon="▪",
    layout="wide",
    initial_sidebar_state="collapsed",
)
inject_css()

if "selected_metric" not in st.session_state:
    st.session_state["selected_metric"] = None

# ---------------------------------------------------------------- header ---
st.markdown(
    f"""
    <div class="terminal-header">
        <div>
            <p class="terminal-title">MACRO TERMINAL</p>
            <p class="terminal-subtitle">US rates, inflation and growth</p>
        </div>
        <div class="terminal-meta">
            <span class="live-dot"></span>LIVE&nbsp;&nbsp;·&nbsp;&nbsp;{datetime.now().strftime('%b %d, %Y  %H:%M')}
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------- load data ---
try:
    cpi = d.fetch_fred_series(d.FRED_SERIES["cpi"])
    fed_funds = d.fetch_fred_series(d.FRED_SERIES["fed_funds"])
    dgs10 = d.fetch_fred_series(d.FRED_SERIES["dgs10"])
    dgs2 = d.fetch_fred_series(d.FRED_SERIES["dgs2"])
    fred_ok = True
except Exception as e:
    fred_ok = False
    st.warning(f"FRED data unavailable right now: {e}")

try:
    recession = d.fetch_fred_series("USREC")
    recession_periods = d.get_recession_periods(recession.set_index("date")["value"])
    recession_ok = True
except Exception:
    recession_ok = False
    recession_periods = []

try:
    curve = d.fetch_treasury_curve_history(years_back=1)
    curve_ok = not curve.empty
except Exception:
    curve_ok = False

# ----------------------------------------------------------------- KPIs ---
metrics_meta = {}
if fred_ok:
    spread = (dgs10.set_index("date")["value"] - dgs2.set_index("date")["value"]).dropna()
    fed_funds_series = fed_funds.set_index("date")["value"]
    cpi_yoy = cpi.set_index("date")["value"].pct_change(12).dropna() * 100

    metrics_meta = {
        "spread": {"title": "10Y \u2013 2Y treasury spread", "series": spread, "color": ACCENT},
        "fed_funds": {"title": "Fed funds rate", "series": fed_funds_series, "color": ACCENT_2},
        "cpi_yoy": {"title": "CPI, year-over-year", "series": cpi_yoy, "color": ACCENT},
    }

    # ---- regime one-liner ----
    spread_now = spread.iloc[-1]
    cpi_now, cpi_ago = cpi_yoy.iloc[-1], d.value_n_months_ago(cpi_yoy, 6)
    ff_now, ff_ago = fed_funds_series.iloc[-1], d.value_n_months_ago(fed_funds_series, 6)

    tags = []
    if spread_now < 0:
        tags.append(("Curve inverted", "neg"))
    elif spread_now > 1.0:
        tags.append(("Curve steep", "pos"))
    else:
        tags.append(("Curve near flat", "neutral"))

    if cpi_now < cpi_ago - 0.1:
        tags.append(("Inflation cooling", "pos"))
    elif cpi_now > cpi_ago + 0.1:
        tags.append(("Inflation rising", "neg"))
    else:
        tags.append(("Inflation steady", "neutral"))

    if ff_now > ff_ago + 0.05:
        tags.append(("Fed hiking", "neg"))
    elif ff_now < ff_ago - 0.05:
        tags.append(("Fed cutting", "pos"))
    else:
        tags.append(("Fed on hold", "neutral"))

    regime_html = " &nbsp;\u00b7&nbsp; ".join(f'<span class="regime-{cls}">{text}</span>' for text, cls in tags)
    st.markdown(f'<p class="regime-line">{regime_html}</p>', unsafe_allow_html=True)


def kpi_card(col, key, label, value, delta, invert_color=False):
    with col:
        is_up = (delta or 0) >= 0
        pos = is_up if not invert_color else not is_up
        delta_class = "kpi-delta-pos" if pos else "kpi-delta-neg"
        arrow = "\u25b2" if is_up else "\u25bc"
        value_str = f"{value:.2f}%" if value is not None else "\u2014"
        delta_str = f"{arrow} {abs(delta):.2f}%" if delta is not None else "\u2014"
        st.markdown(
            f"""
            <div class="kpi-card">
                <p class="kpi-label">{label}</p>
                <p class="kpi-value">{value_str}</p>
                <span class="{delta_class}">{delta_str}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if value is not None and st.button("Expand chart \u2197", key=f"btn_{key}"):
            st.session_state["selected_metric"] = key


if fred_ok:
    c1, c2, c3 = st.columns(3)
    kpi_card(c1, "spread", "10Y \u2013 2Y Spread", spread.iloc[-1], spread.iloc[-1] - spread.iloc[-2], invert_color=True)
    ff_val, ff_delta = d.latest_value(fed_funds)
    kpi_card(c2, "fed_funds", "Fed Funds Rate", ff_val, ff_delta)
    kpi_card(c3, "cpi_yoy", "CPI YoY", cpi_yoy.iloc[-1], cpi_yoy.iloc[-1] - cpi_yoy.iloc[-2])

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

# ------------------------------------------------ expanded metric panel ---
selected = st.session_state.get("selected_metric")
if selected and selected in metrics_meta:
    meta = metrics_meta[selected]
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    title_col, close_col = st.columns([6, 1])
    with title_col:
        st.markdown(f'<p class="panel-title">{meta["title"]}</p>', unsafe_allow_html=True)
    with close_col:
        st.markdown('<div class="panel-close-wrap">', unsafe_allow_html=True)
        if st.button("\u2715 Close", key="close_expand"):
            st.session_state["selected_metric"] = None
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    series = meta["series"]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=series.index, y=series.values, mode="lines",
        line=dict(color=meta["color"], width=2),
        fill="tozeroy", fillcolor="rgba(245,166,35,0.06)",
    ))
    if recession_ok:
        for start, end in recession_periods:
            if end >= series.index.min() and start <= series.index.max():
                fig.add_vrect(x0=start, x1=end, fillcolor="rgba(122,125,133,0.14)", line_width=0, layer="below")
    st.plotly_chart(plotly_layout(fig, height=320), use_container_width=True, config={"displayModeBar": False})
    if recession_ok:
        st.markdown('<p class="chart-caption">Shaded bands: US recessions (NBER, via FRED)</p>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------- hero: curve ---
st.markdown('<div class="panel">', unsafe_allow_html=True)
st.markdown('<p class="panel-title">Treasury par yield curve</p>', unsafe_allow_html=True)

if curve_ok:
    maturities = [m for m in d.TREASURY_MATURITIES if m in curve.columns]

    latest_row = curve.iloc[-1]
    cutoff_3m = curve["Date"].max() - pd.Timedelta(days=90)
    cutoff_1y = curve["Date"].max() - pd.Timedelta(days=365)

    prior_3m_candidates = curve[curve["Date"] <= cutoff_3m]
    prior_3m_row = prior_3m_candidates.iloc[-1] if len(prior_3m_candidates) else None

    prior_1y_candidates = curve[curve["Date"] <= cutoff_1y]
    prior_1y_row = prior_1y_candidates.iloc[-1] if len(prior_1y_candidates) else None

    insights = {
        "1 Mo": "Tracks the Fed's current overnight policy rate almost exactly.",
        "2 Mo": "Very short end, dominated by near-term Fed expectations.",
        "3 Mo": "Closely watched proxy for current Fed policy stance.",
        "4 Mo": "Bridges current policy and the next few FOMC meetings.",
        "6 Mo": "Prices in the expected Fed path over the next two meetings.",
        "1 Yr": "Reflects where markets expect the Fed funds rate to be in a year.",
        "2 Yr": "Key point for gauging near-term rate-cut or hike expectations.",
        "3 Yr": "Transition zone between policy expectations and growth outlook.",
        "5 Yr": "Balances near-term policy with medium-term growth expectations.",
        "7 Yr": "Less liquid point, often used as a curve-smoothing reference.",
        "10 Yr": "Benchmark long-term rate; anchors mortgages and corporate borrowing.",
        "20 Yr": "Longer-dated supply-sensitive point, can trade cheap to 10Y and 30Y.",
        "30 Yr": "Reflects long-run growth and inflation expectations.",
    }
    customdata_today = [insights.get(m, "Point on the Treasury par yield curve.") for m in maturities]

    fig = go.Figure()

    if prior_1y_row is not None:
        fig.add_trace(go.Scatter(
            x=maturities, y=[prior_1y_row[m] for m in maturities],
            mode="lines+markers", name="1 year ago",
            line=dict(color="#5A5D66", width=1.5, dash="dash"), marker=dict(size=4),
            hovertemplate="<b>%{x}</b><br>1yr ago: %{y:.2f}%<extra></extra>",
        ))

    if prior_3m_row is not None:
        fig.add_trace(go.Scatter(
            x=maturities, y=[prior_3m_row[m] for m in maturities],
            mode="lines+markers", name="3 months ago",
            line=dict(color=ACCENT_2, width=1.5, dash="dot"), marker=dict(size=5),
            hovertemplate="<b>%{x}</b><br>3mo ago: %{y:.2f}%<extra></extra>",
        ))

    fig.add_trace(go.Scatter(
        x=maturities, y=[latest_row[m] for m in maturities],
        mode="lines+markers", name="Today",
        line=dict(color=ACCENT, width=2.5), marker=dict(size=6),
        customdata=customdata_today,
        hovertemplate="<b>%{x}</b><br>Today: %{y:.2f}%<br><i>%{customdata}</i><extra></extra>",
    ))

    st.plotly_chart(plotly_layout(fig, height=360), use_container_width=True, config={"displayModeBar": False})

    if fred_ok and spread.iloc[-1] < 0:
        st.markdown(
            f"""
            <div class="curve-alert">
                Curve inverted \u2014 the 2Y is yielding {abs(spread.iloc[-1]):.2f} pts more than the 10Y.
                Inversions like this have preceded most US recessions since 1970, typically with a
                lag of 12\u201324 months.
            </div>
            """,
            unsafe_allow_html=True,
        )
else:
    st.markdown('<p style="color:#7A7D85; font-size:13px;">Yield curve data unavailable right now.</p>', unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------------- footer ---
st.markdown(
    """
    <p class="footer-note">
    Sources:
    <a href="https://fred.stlouisfed.org" target="_blank">FRED</a> ·
    <a href="https://home.treasury.gov/resource-center/data-chart-center/interest-rates" target="_blank">U.S. Treasury</a>
    &nbsp;·&nbsp; Cached hourly
    </p>
    """,
    unsafe_allow_html=True,
)
