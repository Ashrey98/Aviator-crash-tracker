
import streamlit as st
import pytesseract
from PIL import Image
import numpy as np
import re

st.set_page_config(page_title="Aviator Crash Tracker", layout="centered")
st.title("🛩️ Aviator Crash Tracker")

st.markdown("""
Upload a screenshot of the crash history from Aviator (Betpawa), or paste the multipliers below.
We'll extract and analyze them for you.
""")

# Image upload section
uploaded_image = st.file_uploader("📷 Upload Screenshot of Crash History (PNG, JPG)", type=["png", "jpg", "jpeg"])

input_data = ""
if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    try:
        text = pytesseract.image_to_string(image)
        input_data = " ".join(re.findall(r"[0-9]+\.[0-9]+", text))
        st.success("✅ Multipliers extracted from image.")
        st.write(f"📋 Extracted Data: {input_data}")
    except Exception as e:
        st.error(f"Failed to read image: {e}")

# Manual input fallback
input_data = st.text_area("✍️ Or paste multipliers manually (e.g. 1.02 2.40 50.10)", value=input_data, height=150)

if input_data:
    try:
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
    st.info("Upload a screenshot or paste your multipliers above.")
