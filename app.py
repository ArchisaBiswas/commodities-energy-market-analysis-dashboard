import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

# ---------------------------------------
# PAGE CONFIG
# ---------------------------------------

st.set_page_config(
    page_title="Commodity Market Analytics Dashboard",
    layout="wide"
)

# ---------------------------------------
# GLOBAL STYLING  (light theme)
# ---------------------------------------

st.markdown("""
<style>
    .stApp { background-color: #d6e8f7; }
    [data-testid="stAppViewContainer"] { background-color: #d6e8f7; }
    [data-testid="stHeader"] { background-color: #d6e8f7; border-bottom: 1px solid #b0cce8; }
    h1 { color: #0f1f3d !important; font-weight: 800 !important; letter-spacing: -0.5px; }
    h2, h3 { color: #1e3a5f !important; font-weight: 700 !important; }
    hr { border-color: #d0d9e8 !important; }
    [data-testid="stExpander"] {
        background-color: #ffffff !important;
        border: 1px solid #dde3ee !important;
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("Energy Market Analytics Dashboard: Crude Oil, Gasoline & Refining Margins")

# ---------------------------------------
# LOAD DATA
# ---------------------------------------

oil      = yf.download("CL=F", period="1y")
gasoline = yf.download("RB=F", period="1y")

# ---------------------------------------
# CLEAN DATA
# ---------------------------------------

oil = oil[['Close']].copy()
oil.columns = ['Oil']

gasoline = gasoline[['Close']].copy()
gasoline.columns = ['Gasoline']

df = oil.join(gasoline, how='inner').dropna()

# # ---------------------------------------
# # CRACK SPREAD
# # ---------------------------------------

# # df['Crack_Spread'] = df['Gasoline'] - df['Oil']
# # df['Crack_Spread'] = (df['Gasoline'] * 42) - df['Oil']


# gasoline_yield = 0.7

# df['Gasoline_Bbl'] = df['Gasoline'] * 42

# df['Crack_Spread'] = (df['Gasoline_Bbl'] * gasoline_yield) - df['Oil']

# ---------------------------------------
# CRACK SPREAD (REFINING MARGIN PROXY)
# ---------------------------------------

gasoline_yield = 0.7

df['Gasoline_Bbl'] = df['Gasoline'] * 42

df['Crack_Spread'] = (df['Gasoline_Bbl'] * gasoline_yield) - df['Oil']

# ---------------------------------------
# MOVING AVERAGES
# ---------------------------------------

df['Oil_MA_20']      = df['Oil'].rolling(20).mean()
df['Gasoline_MA_20'] = df['Gasoline'].rolling(20).mean()

# ---------------------------------------
# VOLATILITY
# ---------------------------------------

df['Oil_Returns']   = df['Oil'].pct_change()
df['Oil_Volatility'] = df['Oil_Returns'].rolling(20).std() * (252 ** 0.5)

# ---------------------------------------
# STAT CARDS  (top of page)
# ---------------------------------------

latest_oil   = df['Oil'].iloc[-1]
latest_gas   = df['Gasoline'].iloc[-1]
latest_crack = df['Crack_Spread'].iloc[-1]
latest_vol   = df['Oil_Volatility'].iloc[-1]

prev_oil   = df['Oil'].iloc[-2]
prev_gas   = df['Gasoline'].iloc[-2]
prev_crack = df['Crack_Spread'].iloc[-2]
prev_vol   = df['Oil_Volatility'].iloc[-2]

oil_delta   = latest_oil   - prev_oil
gas_delta   = latest_gas   - prev_gas
crack_delta = latest_crack - prev_crack
vol_delta   = latest_vol   - prev_vol


def stat_card(label, value_str, delta, delta_str, accent):
    clr   = "#16a34a" if delta >= 0 else "#dc2626"
    arrow = "▲" if delta >= 0 else "▼"
    sign  = "+" if delta >= 0 else ""
    return (
        f'<div style="background:#ffffff;border:1px solid #dde3ee;'
        f'border-top:3px solid {accent};border-radius:10px;'
        f'padding:20px 22px;box-shadow:0 2px 8px rgba(15,31,61,0.06);">'
        f'<p style="color:#64748b;font-size:11px;letter-spacing:1.5px;'
        f'text-transform:uppercase;margin:0 0 8px 0;font-weight:700;">{label}</p>'
        f'<p style="color:#0f1f3d;font-size:28px;font-weight:800;'
        f'margin:0 0 6px 0;line-height:1.1;font-variant-numeric:tabular-nums;">{value_str}</p>'
        f'<p style="color:{clr};font-size:13px;margin:0;font-weight:600;">'
        f'{arrow} {sign}{delta_str}'
        f'<span style="color:#94a3b8;font-weight:400;"> vs prev day</span></p>'
        f'</div>'
    )


c1 = stat_card("WTI Crude Oil ($/bbl)",  f"${latest_oil:.2f}",   oil_delta,   f"{abs(oil_delta):.2f}",   "#1e4d8c")
c2 = stat_card("RBOB Gasoline ($/gal)",  f"${latest_gas:.4f}",   gas_delta,   f"{abs(gas_delta):.4f}",   "#0e7490")
# c3 = stat_card("Crack Spread ($/bbl)",   f"${latest_crack:.2f}", crack_delta, f"{abs(crack_delta):.2f}", "#7c3aed")
c3 = stat_card("Refining Margin Proxy ($/bbl)", f"${latest_crack:.2f}", crack_delta, f"{abs(crack_delta):.2f}", "#7c3aed")
c4 = stat_card("Annualised Volatility",  f"{latest_vol:.2%}",    vol_delta,   f"{abs(vol_delta):.2%}",   "#b45309")

st.markdown(
    f'<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin:4px 0 24px 0;">'
    f'{c1}{c2}{c3}{c4}'
    f'</div>',
    unsafe_allow_html=True
)

# ---------------------------------------
# PLATFORM OVERVIEW CARD  (light)
# ---------------------------------------

st.markdown("""
<div style="background:#eef4ff;
            border:1px solid #c7d9f5;
            border-left:4px solid #1e4d8c;
            border-radius:10px;
            padding:20px 24px;
            margin-bottom:20px;">
    <p style="color:#1e4d8c;font-size:11px;letter-spacing:1.8px;
              text-transform:uppercase;margin:0 0 10px 0;font-weight:700;">
        Platform Overview
    </p>
    <p style="color:#1e293b;font-size:15px;line-height:1.75;margin:0 0 16px 0;">
        End-to-end commodity analytics dashboard covering WTI crude oil and RBOB 
        gasoline futures. Designed for monitoring price dynamics, yield-adjusted 
        refining margin proxies, and volatility-based risk estimates over a 1-year 
        historical window using 252 trading days for annualisation.
    </p>
    <div style="display:flex;flex-wrap:wrap;gap:8px;">
        <span style="background:rgba(30,77,140,0.08);color:#1e4d8c;
                     border:1px solid rgba(30,77,140,0.2);border-radius:20px;
                     padding:4px 14px;font-size:12px;font-weight:600;">WTI Crude (CL=F)</span>
        <span style="background:rgba(30,77,140,0.08);color:#1e4d8c;
                     border:1px solid rgba(30,77,140,0.2);border-radius:20px;
                     padding:4px 14px;font-size:12px;font-weight:600;">RBOB Gasoline (RB=F)</span>
        <span style="background:rgba(30,77,140,0.08);color:#1e4d8c;
                     border:1px solid rgba(30,77,140,0.2);border-radius:20px;
                     padding:4px 14px;font-size:12px;font-weight:600;">Refining Margin Proxy (Gasoline Yield-Adjusted)</span>
        <span style="background:rgba(30,77,140,0.08);color:#1e4d8c;
                     border:1px solid rgba(30,77,140,0.2);border-radius:20px;
                     padding:4px 14px;font-size:12px;font-weight:600;">20-Day Moving Averages</span>
        <span style="background:rgba(30,77,140,0.08);color:#1e4d8c;
                     border:1px solid rgba(30,77,140,0.2);border-radius:20px;
                     padding:4px 14px;font-size:12px;font-weight:600;">Annualised Volatility (252-day)</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# ---------------------------------------
# SHARED CHART STYLE
# ---------------------------------------

CHART_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='#ffffff',
    font=dict(color='#334155', size=12),
    xaxis=dict(
        gridcolor='#e8edf5',
        linecolor='#cbd5e1',
        title_font=dict(color='#64748b'),
    ),
    yaxis=dict(
        gridcolor='#e8edf5',
        linecolor='#cbd5e1',
        title_font=dict(color='#64748b'),
    ),
    legend=dict(
        bgcolor='rgba(255,255,255,0.8)',
        bordercolor='#dde3ee',
        borderwidth=1,
        font=dict(color='#334155'),
    ),
    margin=dict(t=16, b=40, l=10, r=10),
)

# ---------------------------------------
# PRICE CHARTS
# ---------------------------------------

col1, col2 = st.columns(2)

with col1:
    st.subheader("WTI Crude Oil Prices")

    fig_oil = go.Figure()
    fig_oil.add_trace(go.Scatter(
        x=df.index, y=df['Oil'], name='Oil Price',
        line=dict(color='#1e4d8c', width=1.8)
    ))
    fig_oil.add_trace(go.Scatter(
        x=df.index, y=df['Oil_MA_20'], name='20-Day MA',
        line=dict(color='#f59e0b', width=1.5, dash='dash')
    ))
    fig_oil.update_layout(xaxis_title="Date", yaxis_title="Price ($/bbl)", **CHART_LAYOUT)
    st.plotly_chart(fig_oil, use_container_width=True)

with col2:
    st.subheader("RBOB Gasoline Prices")

    fig_gas = go.Figure()
    fig_gas.add_trace(go.Scatter(
        x=df.index, y=df['Gasoline'], name='Gasoline Price',
        line=dict(color='#0e7490', width=1.8)
    ))
    fig_gas.add_trace(go.Scatter(
        x=df.index, y=df['Gasoline_MA_20'], name='20-Day MA',
        line=dict(color='#f59e0b', width=1.5, dash='dash')
    ))
    fig_gas.update_layout(xaxis_title="Date", yaxis_title="Price ($/gal)", **CHART_LAYOUT)
    st.plotly_chart(fig_gas, use_container_width=True)

# ---------------------------------------
# CRACK SPREAD CHART
# ---------------------------------------

# st.subheader("Crack Spread Analysis")

st.subheader("Refining Margin Proxy Analysis")

fig_crack = go.Figure()
fig_crack.add_trace(go.Scatter(
    x=df.index, y=df['Crack_Spread'], name='Crack Spread',
    line=dict(color='#7c3aed', width=1.8),
    fill='tozeroy', fillcolor='rgba(124,58,237,0.06)'
))
fig_crack.update_layout(xaxis_title="Date", yaxis_title="Spread ($/bbl)", **CHART_LAYOUT)
st.plotly_chart(fig_crack, use_container_width=True)

# ---------------------------------------
# VOLATILITY CHART
# ---------------------------------------

st.subheader("Oil Market Volatility")

fig_vol = go.Figure()
fig_vol.add_trace(go.Scatter(
    x=df.index, y=df['Oil_Volatility'], name='20-Day Annualised Vol',
    line=dict(color='#b45309', width=1.8),
    fill='tozeroy', fillcolor='rgba(180,83,9,0.06)'
))
fig_vol.update_layout(xaxis_title="Date", yaxis_title="Volatility (annualised)", **CHART_LAYOUT)
st.plotly_chart(fig_vol, use_container_width=True)

# ---------------------------------------
# RAW DATA
# ---------------------------------------

with st.expander("Show Raw Data"):
    st.dataframe(df.tail(20))
