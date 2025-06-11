import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="Crazy Wonderland Storm Analyzer", layout="wide")

# Função para simular rodadas
def simulate_game_data(game_name, num_rounds=50):
    now = datetime.now()
    data = []
    for i in range(num_rounds):
        timestamp = now - timedelta(minutes=3*i)
        multiplier = random.choices([1, 2, 5, 10, 50, 100, 200, 500], weights=[40, 20, 15, 10, 5, 4, 3, 1])[0]
        bonus_type = None
        if multiplier >= 50:
            bonus_type = random.choice(['Coin Flip', 'Cash Hunt', 'Pachinko', 'Crazy Time'])
        data.append({
            "timestamp": timestamp,
            "multiplier": multiplier,
            "bonus_type": bonus_type,
            "game": game_name
        })
    return pd.DataFrame(data)

# Simula os dados
crazy_df = simulate_game_data("Crazy Time")
wonderland_df = simulate_game_data("Wonderland")
lightning_df = simulate_game_data("Lightning Storm")

games_data = {
    "Crazy Time": crazy_df,
    "Wonderland": wonderland_df,
    "Lightning Storm": lightning_df
}

# Função de alerta inteligente
def get_alert_label(df):
    last_bonus = df[df['bonus_type'].notna()].head(1)
    rounds_since_bonus = df.index[0] if last_bonus.empty else last_bonus.index[0]

    if rounds_since_bonus >= 25:
        return "🟢 Entrar"
    elif 10 <= rounds_since_bonus < 25:
        return "🟡 Observar"
    else:
        return "🔴 Esperar"

# Layout principal
st.title("🎯 Crazy Wonderland Storm Analyzer")
st.markdown("Visualização simulada das rodadas e lógica do robô de alertas")

for game, df in games_data.items():
    st.subheader(f"🎮 {game}")
    df = df.sort_values(by="timestamp", ascending=False).reset_index(drop=True)

    alert = get_alert_label(df)
    st.markdown(f"### Status: {alert}")

    col1, col2 = st.columns([2, 1])

    with col1:
        fig, ax = plt.subplots(figsize=(10, 3))
        ax.plot(df['timestamp'], df['multiplier'], marker='o', label='Multiplicador')
        for i, row in df.iterrows():
            if row['bonus_type']:
                ax.annotate(row['bonus_type'], (row['timestamp'], row['multiplier']), textcoords="offset points", xytext=(0,10), ha='center', fontsize=8, color='red')
        ax.set_title("Histórico de Multiplicadores")
        ax.set_ylabel("x Multiplicador")
        ax.tick_params(axis='x', labelrotation=45)
        st.pyplot(fig)

    with col2:
        bonus_count = df[df['bonus_type'].notna()].shape[0]
        high_bonus = df[df['multiplier'] >= 200].shape[0]
        st.metric("Rodadas sem bônus", df.index[0])
        st.metric("Bônus nas últimas 50", bonus_count)
        st.metric("Bônus acima de 200x", high_bonus)

    with st.expander("Ver rodadas recentes"):
        st.dataframe(df[['timestamp', 'multiplier', 'bonus_type']])

    st.divider()

st.info("⚠️ Dados simulados. Em breve, integração com leitura em tempo real do CasinoScores.com")
