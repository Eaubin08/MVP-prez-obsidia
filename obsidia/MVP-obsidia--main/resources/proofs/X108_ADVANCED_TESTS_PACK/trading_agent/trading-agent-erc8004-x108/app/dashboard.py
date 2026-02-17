import json
import pandas as pd
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="ERC-8004 X-108 Trading Agent", layout="wide")
st.title("ERC-8004 X-108 Trading Agent — Dashboard (logs)")

logs_dir = Path("logs")
decision = logs_dir/"decision_log.jsonl"
orders = logs_dir/"orders_log.jsonl"
roi = logs_dir/"roi_log.jsonl"

def read_jsonl(p):
    if not p.exists():
        return pd.DataFrame()
    rows = []
    for line in p.read_text(encoding="utf-8").splitlines():
        try:
            rows.append(json.loads(line))
        except Exception:
            pass
    return pd.DataFrame(rows)

col1, col2 = st.columns(2)
with col1:
    st.subheader("Decisions")
    df = read_jsonl(decision)
    st.dataframe(df.tail(200), use_container_width=True)
with col2:
    st.subheader("ROI decisions")
    df2 = read_jsonl(roi)
    st.dataframe(df2.tail(200), use_container_width=True)

st.subheader("Orders")
df3 = read_jsonl(orders)
st.dataframe(df3.tail(200), use_container_width=True)

# Equity curve from decision log if present
if not df.empty and "equity" in df.columns:
    st.subheader("Equity curve")
    st.line_chart(df.dropna(subset=["equity"]).set_index("step")["equity"])
