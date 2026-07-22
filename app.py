import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

import data as d
from theme import inject_css, plotly_layout, sparkline, ACCENT, ACCENT_2

st.set_page_config(
    page_title="Macro Terminal",
    page_icon="▪",
    layout="wide",
    initial_sidebar_state="collapsed",
)
inject_css()

# ---------------------------------------------------------------- header ---
st.markdown(
    f"""
    <div class="terminal-header">
        <div>
            <p class="terminal-title">MACRO TERMINAL</p>
            <p class="terminal-subtitle">US rates, inflation and growth — free public data, no API keys</p>
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
    unemployment = d.fetch_fred_series(d.FRED_SERIES["unemployment"])
    dgs10 = d.fetch_fred_series(d.FRED_SERIES["dgs10"])
    dgs2 = d.fetch_fred_series(d.FRED_SERIES["dgs2"])
    fred_ok = True
except Exception as e:
    fred_ok = False
    st.warning(f"FRED data unavailable right now: {e}")

try:
    sp500 = d.fetch_sp500()
    sp_ok = True
except Exception:
    sp_ok = False

try:
    curve = d.fetch_treasury_par_yield_curve()
    curve_ok = True
except Exception:
    curve_ok = False


# ----------------------------------------------------------------- KPIs ---
def kpi_card(col, label, value, delta, fmt="{:.2f}", suffix="", spark_values=None, invert_color=False):
    with col:
        is_up = (delta or 0) >= 0
        pos = is_up if not invert_color else not is_up
        delta_class = "kpi-delta-pos" if pos else "kpi-delta-neg"
        arrow = "▲" if is_up else "▼"
        value_str = fmt.format(value) if value is not None else "—"
        delta_str = fmt.format(abs(delta)) if delta is not None else "—"
        st.markdown(
            f"""
            <div class="kpi-card">
                <p class="kpi-label">{label}</p>
                <p class="kpi-value">{value_str}{suffix if value is not None else ""}</p>
                <span class="{delta_class}">{arrow} {delta_str}{suffix if delta is not None else ""}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if spark_values is not None and len(spark_values) > 2:
            st.plotly_chart(
                sparkline(spark_values),
                use_container_width=True,
                config={"displayModeBar": False},
            )


c1, c2, c3, c4, c5 = st.columns(5)

if fred_ok:
    spread = (dgs10.set_index("date")["value"] - dgs2.set_index("date")["value"]).dropna()
    kpi_card(
        c1, "10Y – 2Y Spread", spread.iloc[-1], spread.iloc[-1] - spread.iloc[-2],
        suffix="%", spark_values=spread.tail(60).tolist(), invert_color=True,
    )

    ff_val, ff_delta = d.latest_value(fed_funds)
    kpi_card(c2, "Fed Funds Rate", ff_val, ff_delta, suffix="%", spark_values=fed_funds["value"].tail(60).tolist())

    cpi_yoy = cpi.set_index("date")["value"].pct_change(12).dropna() * 100
    kpi_card(
        c3, "CPI YoY", cpi_yoy.iloc[-1], cpi_yoy.iloc[-1] - cpi_yoy.iloc[-2],
        suffix="%", spark_values=cpi_yoy.tail(60).tolist(),
    )

    u_val, u_delta = d.latest_value(unemployment)
    kpi_card(
        c4, "Unemployment", u_val, u_delta, suffix="%",
        spark_values=unemployment["value"].tail(60).tolist(), invert_color=True,
    )
else:
    for col, label in zip([c1, c2, c3, c4], ["10Y – 2Y Spread", "Fed Funds Rate", "CPI YoY", "Unemployment"]):
        kpi_card(col, label, None, None)

if sp_ok:
    kpi_card(
        c5, "S&P 500", sp500["Close"].iloc[-1], sp500["Close"].iloc[-1] - sp500["Close"].iloc[-2],
        fmt="{:,.0f}", spark_values=sp500["Close"].tail(60).tolist(),
    )
else:
    kpi_card(c5, "S&P 500", None, None)

st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

# ---------------------------------------------------------- hero: curve ---
st.markdown('<div class="panel">', unsafe_allow_html=True)
st.markdown('<p class="panel-title">Treasury par yield curve</p>', unsafe_allow_html=True)

if curve_ok:
    maturities = [m for m in d.TREASURY_MATURITIES if m in curve.columns]
    latest_row = curve.iloc[-1]
    cutoff = curve["Date"].max() - pd.Timedelta(days=90)
    prior_candidates = curve[curve["Date"] <= cutoff]
    prior_row = prior_candidates.iloc[-1] if len(prior_candidates) else latest_row

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=maturities, y=[prior_row[m] for m in maturities],
        mode="lines+markers", name="3 months ago",
        line=dict(color=ACCENT_2, width=1.5, dash="dot"), marker=dict(size=5),
    ))
    fig.add_trace(go.Scatter(
        x=maturities, y=[latest_row[m] for m in maturities],
        mode="lines+markers", name="Today",
        line=dict(color=ACCENT, width=2.5), marker=dict(size=6),
    ))
    st.plotly_chart(plotly_layout(fig, height=340), use_container_width=True, config={"displayModeBar": False})
else:
    st.markdown('<p style="color:#7A7D85; font-size:13px;">Yield curve data unavailable right now.</p>', unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------- secondary charts ---
col_a, col_b = st.columns(2)

with col_a:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<p class="panel-title">Inflation, CPI year-over-year</p>', unsafe_allow_html=True)
    if fred_ok:
        fig2 = go.Figure()
        window = cpi_yoy.tail(120)
        fig2.add_trace(go.Scatter(
            x=window.index, y=window.values, mode="lines",
            line=dict(color=ACCENT, width=2),
            fill="tozeroy", fillcolor="rgba(245,166,35,0.06)",
        ))
        st.plotly_chart(plotly_layout(fig2, height=260), use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

with col_b:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<p class="panel-title">Fed funds rate, history</p>', unsafe_allow_html=True)
    if fred_ok:
        fig3 = go.Figure()
        window = fed_funds.tail(240)
        fig3.add_trace(go.Scatter(
            x=window["date"], y=window["value"], mode="lines",
            line=dict(color=ACCENT_2, width=2),
            fill="tozeroy", fillcolor="rgba(61,214,245,0.06)",
        ))
        st.plotly_chart(plotly_layout(fig3, height=260), use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------------- footer ---
st.markdown(
    """
    <p class="footer-note">
    Data sourced from FRED (Federal Reserve Bank of St. Louis) and Treasury.gov ·
    No API keys required · Cached hourly
    </p>
    """,
    unsafe_allow_html=True,
)
