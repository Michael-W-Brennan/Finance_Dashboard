"""All data fetching for the macro terminal.

Every source here is free and requires no API key:
- FRED series are pulled via the public fredgraph.csv endpoint.
- Treasury par yield curve rates are pulled from Treasury.gov's own CSV feed.
- S&P 500 comes from yfinance.

Everything is cached with st.cache_data so a page rerun doesn't re-hit
these endpoints; adjust ttl if you want fresher or lazier updates.
"""

import io
from datetime import datetime

import pandas as pd
import requests
import streamlit as st
import yfinance as yf

FRED_SERIES = {
    "cpi": "CPIAUCSL",
    "pce": "PCEPI",
    "fed_funds": "FEDFUNDS",
    "unemployment": "UNRATE",
    "dgs10": "DGS10",
    "dgs2": "DGS2",
}

TREASURY_MATURITIES = [
    "1 Mo", "2 Mo", "3 Mo", "4 Mo", "6 Mo",
    "1 Yr", "2 Yr", "3 Yr", "5 Yr", "7 Yr", "10 Yr", "20 Yr", "30 Yr",
]


@st.cache_data(ttl=3600)
def fetch_fred_series(series_id: str) -> pd.DataFrame:
    """Pull a FRED series via the free public CSV endpoint (no API key needed)."""
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    df = pd.read_csv(io.StringIO(resp.text))
    df.columns = ["date", "value"]
    df["date"] = pd.to_datetime(df["date"])
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    return df.dropna().sort_values("date").reset_index(drop=True)


@st.cache_data(ttl=3600)
def fetch_treasury_par_yield_curve(year: int | None = None) -> pd.DataFrame:
    """Pull daily Treasury par yield curve rates for a given year (no API key needed)."""
    year = year or datetime.now().year
    url = (
        "https://home.treasury.gov/resource-center/data-chart-center/"
        "interest-rates/daily-treasury-rates.csv/"
        f"{year}/all?type=daily_treasury_yield_curve&field_tdr_date_value={year}&page&_format=csv"
    )
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    df = pd.read_csv(io.StringIO(resp.text))
    df["Date"] = pd.to_datetime(df["Date"])
    return df.sort_values("Date").reset_index(drop=True)


@st.cache_data(ttl=3600)
def fetch_sp500(period: str = "1y") -> pd.DataFrame:
    """Pull S&P 500 index history via yfinance (no API key needed)."""
    df = yf.Ticker("^GSPC").history(period=period)
    df = df.reset_index()[["Date", "Close"]]
    return df


def latest_value(df: pd.DataFrame, value_col: str = "value"):
    """Return (latest value, change vs prior observation) for a FRED-style df."""
    if df.empty:
        return None, None
    latest = df.iloc[-1][value_col]
    prior = df.iloc[-2][value_col] if len(df) > 1 else latest
    return latest, latest - prior
