# Energy Commodities Analytics Dashboard

An interactive Streamlit-based analytics dashboard for monitoring **WTI crude oil** and **RBOB gasoline futures**, with derived insights into price dynamics, refining margin proxies, and market volatility.

---

## Overview

This project is an end-to-end commodity analytics tool designed to explore key relationships in energy markets:

+ Crude oil price behaviour (WTI)
+ Gasoline price dynamics (RBOB)
+ Simplified refining margin proxy (yield-adjusted crack spread)
+ Volatility-based risk estimation using rolling returns

The dashboard provides a visual and quantitative lens into short- to medium-term energy market behaviour using a 1-year historical window.

---

## Features

### Price Analytics
+ WTI Crude Oil futures (`CL=F`)
+ RBOB Gasoline futures (`RB=F`)
+ 20-day moving averages for trend analysis

### Refining Margin Proxy
+ Yield-adjusted gasoline crack spread approximation
+ Converts gasoline from $/gallon to $/barrel
+ Applies refinery yield assumption (default: 70%)

> Note: This is a simplified proxy and not a full industry 3:2:1 Crack Spread model.

### Risk & Volatility
+ Daily returns calculation for crude oil
+ Rolling 20-day volatility
+ Annualised volatility (252 trading days convention)

### Interactive Visualisation
+ Plotly-powered interactive charts
+ Clean, responsive Streamlit UI
+ Stat cards for quick market insights

---

## Methodology

### Data Sources
- `yfinance` API for futures data:
  - WTI Crude Oil: `CL=F`
  - RBOB Gasoline: `RB=F`

## Key Transformations

### Gasoline conversion
Gasoline price per barrel is approximated as:

Gasoline (per barrel) = Gasoline price per gallon × 42

---

### Refining margin proxy (yield-adjusted crack spread)

Crack Spread Proxy = (Gasoline per barrel × 0.7) − Crude Oil

Where:
+ 0.7 represents an assumed refinery yield for gasoline output
+ This is a simplified proxy for refining margins (not a full 3:2:1 Crack Spread model)

---

### Volatility (Annualised)

Annualised volatility is computed as:

σ_annualised = σ_20-day × √252

Where:
+ 252 = number of trading days in a year
+ σ_20-day = rolling standard deviation of daily returns

---