
# crazy_wonderland_storm_analyzer/streamlit_app.py

import streamlit as st
import pandas as pd
import datetime

# Simulated data for now
data = {
    "Crazy Time": [
        {"timestamp": "2025-06-11 17:10", "bonus": "Coin Flip", "multiplier": 75},
        {"timestamp": "2025-06-11 16:42", "bonus": "Crazy Time", "multiplier": 500},
        {"timestamp": "2025-06-11 15:23", "bonus": "Pachinko", "multiplier": 210},
    ],
    "Wonderland": [
        {"timestamp": "2025-06-11 17:02", "bonus": "Magic Dice", "multiplier": 220},
        {"timestamp": "2025-06-11 15:45", "bonus": "Wonder Spins", "multiplier": 60},
    ],
    "Lightning Storm": [
        {"timestamp": "2025-06-11 16:15", "bonus": "Lightning Bonus", "multiplier": 340},
        {"timestamp": "2025-06-11 13:10", "bonus": "Lightning Reels", "multiplier": 95},
    ]
}

st.set_page_config(page_title="Bonus Analyzer", layout="wide")
st.title("🎰 Casino Bonus Tracker - Últimos Bônus > 200x")

for game, records in data.items():
    st.subheader(f"🎯 {game}")
    df = pd.DataFrame(records)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df_filtered = df[df['multiplier'] >= 200]

    if not df_filtered.empty:
        st.success(f"{len(df_filtered)} bônus acima de 200x nas últimas 24h")
        st.dataframe(df_filtered.sort_values(by="timestamp", ascending=False), use_container_width=True)
        last_bonus = df_filtered.sort_values(by="timestamp", ascending=False).iloc[0]
        delta = datetime.datetime.now() - last_bonus['timestamp'].to_pydatetime()
        st.info(f"⏰ Último BIG bônus: {last_bonus['bonus']} ({last_bonus['multiplier']}x), há {delta.seconds//60} minutos")
    else:
        st.warning("⚠️ Nenhum bônus acima de 200x nas últimas 24 horas")

    st.markdown("---")
