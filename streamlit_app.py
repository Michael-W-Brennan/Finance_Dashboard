import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

##############################################
# Configuration
##############################################

TICKER = "AAPL"
PERIOD = "1y"

##############################################
# Download Data
##############################################

ticker = yf.Ticker(TICKER)

df = ticker.history(period=PERIOD)

info = ticker.info

##############################################
# Indicators
##############################################

df["MA20"] = df["Close"].rolling(20).mean()
df["MA50"] = df["Close"].rolling(50).mean()

##############################################
# Create Dashboard
##############################################

fig = make_subplots(
    rows=3,
    cols=1,
    shared_xaxes=True,
    row_heights=[0.65,0.20,0.15],
    vertical_spacing=0.03,
    specs=[
        [{"type":"candlestick"}],
        [{"type":"bar"}],
        [{"type":"table"}]
    ]
)

########################################################
# Candlestick
########################################################

fig.add_trace(
    go.Candlestick(
        x=df.index,
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        name="Price"
    ),
    row=1,
    col=1
)

########################################################
# Moving Average
########################################################

fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["MA20"],
        line=dict(width=2),
        name="20 MA"
    ),
    row=1,
    col=1
)

fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["MA50"],
        line=dict(width=2),
        name="50 MA"
    ),
    row=1,
    col=1
)

########################################################
# Volume
########################################################

colors = [
    "green" if c >= o else "red"
    for c,o in zip(df["Close"],df["Open"])
]

fig.add_trace(
    go.Bar(
        x=df.index,
        y=df["Volume"],
        marker_color=colors,
        name="Volume"
    ),
    row=2,
    col=1
)

########################################################
# Statistics Table
########################################################

stats = [
    ["Company", info.get("longName","")],
    ["Ticker", TICKER],
    ["Sector", info.get("sector","")],
    ["Industry", info.get("industry","")],
    ["Market Cap", f"${info.get('marketCap',0):,}"],
    ["PE Ratio", info.get("trailingPE","")],
    ["Dividend Yield", info.get("dividendYield","")],
    ["52 Week High", info.get("fiftyTwoWeekHigh","")],
    ["52 Week Low", info.get("fiftyTwoWeekLow","")],
]

labels = [x[0] for x in stats]
values = [x[1] for x in stats]

fig.add_trace(
    go.Table(
        header=dict(
            values=["Statistic","Value"],
            fill_color="royalblue",
            font=dict(color="white",size=14),
            align="left"
        ),
        cells=dict(
            values=[labels,values],
            align="left",
            height=26
        )
    ),
    row=3,
    col=1
)

########################################################
# Layout
########################################################

fig.update_layout(

    title=f"{TICKER} Financial Dashboard",

    template="plotly_dark",

    height=950,

    xaxis_rangeslider_visible=True,

    hovermode="x unified",

    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="left",
        x=0
    )
)

fig.update_yaxes(title="Price", row=1,col=1)
fig.update_yaxes(title="Volume", row=2,col=1)

fig.show()
