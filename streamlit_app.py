
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(page_title="Aviator Crash Tracker", layout="wide")
st.title("✈️ Aviator Crash Tracker - by Ashraf")

st.write("""
Enter each round's crash multiplier (e.g., 1.05, 2.00, 50.00). This tool will:
- Flag long losing streaks below 2.00x
- Highlight high multipliers
- Track win rate stats
""")

# Input Section
data_input = st.text_area("Paste multipliers here (comma-separated):", "1.05, 1.80, 1.20, 1.00, 1.50, 2.10, 1.00, 1.01, 1.95, 2.30, 2.00")
try:
    multipliers = [float(x.strip()) for x in data_input.split(",") if x.strip() != ""]
except ValueError:
    st.error("Please enter only numbers separated by commas.")
    st.stop()

# Analysis
streaks = []
current_streak = 0
wins = 0
losses = 0
highlight_rounds = []

for i, val in enumerate(multipliers):
    if val < 2.0:
        losses += 1
        current_streak += 1
    else:
        wins += 1
        if current_streak >= 3:
            streaks.append((i - current_streak, i - 1, current_streak))
        current_streak = 0
    if val >= 5.0:
        highlight_rounds.append(i)

if current_streak >= 3:
    streaks.append((len(multipliers) - current_streak, len(multipliers) - 1, current_streak))

# Stats
st.subheader("📊 Stats")
st.markdown(f"**Total Rounds:** {len(multipliers)}")
st.markdown(f"**Wins (≥ 2.00x):** {wins}")
st.markdown(f"**Losses (< 2.00x):** {losses}")
st.markdown(f"**Win Rate:** {wins / len(multipliers) * 100:.2f}%")

if streaks:
    st.warning(f"⚠️ {len(streaks)} streak(s) of 3+ losses found!")
else:
    st.success("✅ No long streaks of losses detected.")

# Chart
st.subheader("📈 Multiplier Chart")
fig, ax = plt.subplots(figsize=(12, 5))
x = list(range(1, len(multipliers) + 1))
ax.plot(x, multipliers, marker='o', label='Multiplier')
ax.axhline(y=2.0, color='red', linestyle='--', label='2.00x Threshold')

for start, end, length in streaks:
    ax.axvspan(start + 1, end + 1, color='orange', alpha=0.3)

for i in highlight_rounds:
    ax.plot(i + 1, multipliers[i], 'go', markersize=10)

ax.set_xlabel("Round Number")
ax.set_ylabel("Crash Multiplier (x)")
ax.set_title("Crash Multiplier Over Time")
ax.grid(True)
ax.legend()
st.pyplot(fig)

st.caption("Made for Ashraf ✊")
