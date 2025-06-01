
import streamlit as st
import numpy as np

st.set_page_config(page_title="Aviator Crash Tracker", layout="centered")

st.title("🛩️ Aviator Crash Tracker")

st.markdown("Paste crash multipliers from the game (e.g. `1.01 1.20 1.00 50.25`) and get smart stats.")

input_data = st.text_area("📋 Paste Crash Multipliers Below (Space-separated)", height=150)

if input_data:
    try:
        # Parse numbers from pasted string
        rounds = [float(x) for x in input_data.strip().split() if x.replace('.', '', 1).isdigit()]
        total = len(rounds)
        above_2x = sum(1 for x in rounds if x >= 2)
        below_2x = total - above_2x
        avg_multiplier = round(sum(rounds) / total, 2)

        # Detect streaks under 2.0x
        streaks = []
        current_streak = 0
        for value in rounds:
            if value < 2:
                current_streak += 1
            else:
                if current_streak > 0:
                    streaks.append(current_streak)
                current_streak = 0
        if current_streak > 0:
            streaks.append(current_streak)

        longest_streak = max(streaks) if streaks else 0
        high_multipliers = [x for x in rounds if x >= 50]

        st.subheader("📊 Results Summary")
        st.write(f"Total Rounds: {total}")
        st.write(f"Average Multiplier: {avg_multiplier}")
        st.write(f"Rounds ≥ 2.00x: {above_2x} ({round(above_2x/total*100, 1)}%)")
        st.write(f"Rounds < 2.00x: {below_2x} ({round(below_2x/total*100, 1)}%)")
        st.write(f"🚨 Longest Streak < 2.00x: {longest_streak}")

        if high_multipliers:
            st.success(f"🎯 High Multipliers (50x+): {', '.join(map(str, high_multipliers))}")
        else:
            st.info("No high multipliers (50x+) in this set.")
    except Exception as e:
        st.error(f"Error processing input: {str(e)}")
else:
    st.info("Paste your multipliers above to get started.")
