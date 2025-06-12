import streamlit as st
import numpy as np
import soundfile as sf
from scipy.signal import firwin, lfilter
import io
import librosa
import matplotlib.pyplot as plt

# --- Initialize session state for page switching ---
if "page" not in st.session_state:
    st.session_state.page = "home"

# --- Hot Pink Homepage Styling ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500&display=swap');

    .stApp {
        background: linear-gradient(to bottom, #000000, #1a001a);
        color: white;
        font-family: 'Orbitron', sans-serif;
        text-align: center;
    }

    h1 {
        font-size: 3em;
        color: white;
        margin-top: 2em;
        text-shadow: 0 0 20px #ff69b4;
    }

    .subtitle {
        font-size: 1.2em;
        margin-bottom: 2em;
        color: #ccc;
    }

    .start-button {
        background: linear-gradient(to right, #ff5fcb, #9f6eff);
        padding: 0.8em 2.5em;
        font-size: 1.1em;
        border-radius: 30px;
        color: white;
        border: none;
        box-shadow: 0 0 20px #ff69b4;
        cursor: pointer;
        transition: all 0.3s ease-in-out;
    }

    .start-button:hover {
        background: linear-gradient(to right, #ff85d1, #b287ff);
        transform: scale(1.05);
    }
    </style>
""", unsafe_allow_html=True)

# --- Homepage ---
if st.session_state.page == "home":
    st.markdown("<h1>🎧 Digital Music Equalizer</h1>", unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Shape your sound with studio-level precision.</div>', unsafe_allow_html=True)
    if st.button("Start Now", key="start", help="Go to Equalizer", type="primary"):
        st.session_state.page = "equalizer"
        st.experimental_rerun()
