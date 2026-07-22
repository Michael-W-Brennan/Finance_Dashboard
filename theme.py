"""Visual theme for the macro terminal: colors, CSS injection, and a shared
Plotly template so every chart in the app looks like one coherent system."""

import streamlit as st
import plotly.graph_objects as go

BG = "#0A0A0A"
PANEL = "#111214"
BORDER = "#1F2023"
ACCENT = "#F5A623"       # amber — primary series, positive-neutral emphasis
ACCENT_2 = "#3DD6F5"     # cyan — secondary series
POSITIVE = "#00D9A3"
NEGATIVE = "#E5484D"
TEXT_PRIMARY = "#E8E8E8"
TEXT_SECONDARY = "#7A7D85"


def inject_css():
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;600&display=swap');

        .stApp {{
            background-color: {BG};
            font-family: 'Inter', sans-serif;
        }}
        #MainMenu, footer, header {{ visibility: hidden; }}
        .block-container {{ padding-top: 2rem; padding-bottom: 3rem; max-width: 1200px; }}

        .terminal-header {{
            display: flex; justify-content: space-between; align-items: baseline;
            border-bottom: 1px solid {BORDER}; padding-bottom: 16px; margin-bottom: 24px;
        }}
        .terminal-title {{
            font-size: 24px; font-weight: 600; color: {TEXT_PRIMARY}; margin: 0;
            letter-spacing: 0.02em;
        }}
        .terminal-subtitle {{ font-size: 13px; color: {TEXT_SECONDARY}; margin-top: 4px; }}
        .regime-line {{
            font-family: 'JetBrains Mono', monospace; font-size: 12px;
            color: {TEXT_SECONDARY}; margin: 6px 0 0 0;
        }}
        .regime-pos {{ color: {POSITIVE}; }}
        .regime-neg {{ color: {NEGATIVE}; }}
        .regime-neutral {{ color: {TEXT_SECONDARY}; }}
        .chart-caption {{
            font-size: 11px; color: {TEXT_SECONDARY}; margin: 4px 0 0 0;
        }}
        .terminal-meta {{
            font-size: 12px; color: {TEXT_SECONDARY}; text-align: right;
            font-family: 'JetBrains Mono', monospace;
        }}

        .live-dot {{
            display: inline-block; width: 7px; height: 7px; border-radius: 50%;
            background: {POSITIVE}; margin-right: 6px; animation: pulse 2s infinite;
        }}
        @keyframes pulse {{
            0% {{ opacity: 1; }} 50% {{ opacity: 0.25; }} 100% {{ opacity: 1; }}
        }}

        .kpi-card {{
            background: {PANEL}; border: 1px solid {BORDER}; border-radius: 8px 8px 0 0;
            padding: 14px 16px; transition: all 0.2s ease; border-bottom: none;
        }}
        .kpi-card:hover {{
            border-color: {ACCENT};
            box-shadow: 0 0 18px rgba(245, 166, 35, 0.12);
        }}
        .kpi-label {{
            font-size: 11px; color: {TEXT_SECONDARY}; text-transform: uppercase;
            letter-spacing: 0.06em; margin: 0 0 6px 0;
        }}
        .kpi-value {{
            font-family: 'JetBrains Mono', monospace; font-size: 23px; font-weight: 500;
            margin: 0; color: {TEXT_PRIMARY};
        }}
        .kpi-delta-pos {{ color: {POSITIVE}; font-family: 'JetBrains Mono', monospace; font-size: 12px; }}
        .kpi-delta-neg {{ color: {NEGATIVE}; font-family: 'JetBrains Mono', monospace; font-size: 12px; }}

        /* the "Expand chart" button sits flush under its kpi-card, styled as one unit */
        div[data-testid="column"] .stButton {{ margin-top: -1px; }}
        .stButton > button {{
            background: {PANEL}; border: 1px solid {BORDER}; border-top: none;
            border-radius: 0 0 8px 8px; color: {TEXT_SECONDARY};
            font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em;
            padding: 6px 0; width: 100%; box-shadow: none;
        }}
        .stButton > button:hover {{
            color: {ACCENT}; border-color: {ACCENT}; background: {PANEL};
        }}
        .stButton > button:focus:not(:active) {{ color: {ACCENT}; border-color: {ACCENT}; }}

        .panel {{
            background: {PANEL}; border: 1px solid {BORDER}; border-radius: 8px;
            padding: 18px 20px; margin-bottom: 16px;
        }}
        .panel-title {{
            font-size: 12px; font-weight: 600; color: {TEXT_PRIMARY};
            text-transform: uppercase; letter-spacing: 0.05em; margin: 0 0 12px 0;
        }}
        .panel-close-wrap .stButton > button {{
            border-radius: 4px; border: 1px solid {BORDER}; font-size: 11px;
        }}

        .curve-alert {{
            background: rgba(229, 72, 77, 0.08); border-left: 3px solid {NEGATIVE};
            border-radius: 0; padding: 10px 14px; font-size: 12px;
            color: {NEGATIVE}; margin-bottom: 14px; font-family: 'JetBrains Mono', monospace;
        }}

        .footer-note {{
            font-size: 11px; color: {TEXT_SECONDARY}; text-align: center;
            border-top: 1px solid {BORDER}; padding-top: 16px; margin-top: 8px;
        }}
        .footer-note a {{
            color: {TEXT_SECONDARY}; text-decoration: none; border-bottom: 1px solid {BORDER};
        }}
        .footer-note a:hover {{ color: {ACCENT}; border-bottom-color: {ACCENT}; }}

        /* tighten the gap Streamlit leaves above embedded plotly charts */
        div[data-testid="stPlotlyChart"] {{ margin-top: -8px; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def plotly_layout(fig: go.Figure, height: int = 320) -> go.Figure:
    """Apply the shared dark/mono terminal styling to any Plotly figure."""
    fig.update_layout(
        paper_bgcolor=PANEL,
        plot_bgcolor=PANEL,
        font=dict(family="JetBrains Mono, monospace", size=11, color=TEXT_SECONDARY),
        height=height,
        margin=dict(l=10, r=10, t=10, b=10),
        hoverlabel=dict(
            bgcolor=BG,
            bordercolor=ACCENT,
            font=dict(family="JetBrains Mono, monospace", color=TEXT_PRIMARY, size=11),
        ),
        xaxis=dict(
            gridcolor=BORDER, zerolinecolor=BORDER,
            showspikes=True, spikecolor=ACCENT, spikethickness=1, spikemode="across",
        ),
        yaxis=dict(gridcolor=BORDER, zerolinecolor=BORDER),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT_SECONDARY, size=11)),
        hovermode="x unified",
    )
    return fig

