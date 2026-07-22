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
def fetch_treasury_curve_history(years_back: int = 1) -> pd.DataFrame:
    """Fetch the current year's curve plus `years_back` prior years, concatenated.

    Needed because Treasury.gov's CSV feed is scoped to a single calendar
    year, so a true "1 year ago" comparison point requires stitching two
    years together.
    """
    current_year = datetime.now().year
    frames = []
    for yr in range(current_year - years_back, current_year + 1):
        try:
            frames.append(fetch_treasury_par_yield_curve(yr))
        except Exception:
            continue
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True).sort_values("Date").reset_index(drop=True)


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


def get_recession_periods(series: pd.Series) -> list[tuple]:
    """Turn a 0/1 recession-indicator series (e.g. FRED's USREC) indexed by
    date into a list of (start_date, end_date) tuples for each recession."""
    s = series.dropna().sort_index()
    periods = []
    in_recession = False
    start = prev_date = None
    for date, val in s.items():
        if val >= 1 and not in_recession:
            in_recession = True
            start = date
        elif val < 1 and in_recession:
            in_recession = False
            periods.append((start, prev_date))
        prev_date = date
    if in_recession:
        periods.append((start, prev_date))
    return periods


def value_n_months_ago(series: pd.Series, months: int = 6):
    """Nearest observation at least `months` back from the series' latest date."""
    if series.empty:
        return series.iloc[-1] if len(series) else None
    cutoff = series.index.max() - pd.DateOffset(months=months)
    candidates = series[series.index <= cutoff]
    return candidates.iloc[-1] if len(candidates) else series.iloc[0]
