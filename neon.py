import streamlit as st
import numpy as np
import soundfile as sf
from scipy.signal import firwin, lfilter
import io
import librosa
import matplotlib.pyplot as plt

# --- Hot Pink DJ Theme Styling ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500&display=swap');

    .stApp {
        background: linear-gradient(135deg, #0a0a0a, #1a001a);
        color: white;
        font-family: 'Orbitron', sans-serif;
    }

    h1, h2, h3 {
        color: white;
        text-shadow: 0 0 15px #ff69b4;
    }

    .stSlider > div {
        background-color: #111;
        border-radius: 10px;
        padding: 0.5em;
    }

    .stSlider input[type=range]::-webkit-slider-thumb {
        background: #ff69b4;
        box-shadow: 0 0 12px #ff69b4;
    }

    .stSlider input[type=range]::-webkit-slider-runnable-track {
        background: #333;
    }

    .css-1cpxqw2, .css-14r9z6v {
        background-color: #111 !important;
    }

    .css-1cpxqw2:hover {
        background-color: #ff69b4 !important;
        color: black !important;
    }

    audio {
        filter: drop-shadow(0 0 10px #ff69b4aa);
    }

    .stDownloadButton button {
        background: #ff69b4;
        color: black;
        font-weight: bold;
        border-radius: 10px;
        border: none;
        box-shadow: 0 0 12px #ff69b4;
    }

    .stDownloadButton button:hover {
        background: #ff85c1;
        color: #000;
    }
    </style>
""", unsafe_allow_html=True)

# --- Audio Functions ---
def load_audio(file):
    try:
        y, sr = librosa.load(file, sr=None, mono=True)
        return y, sr
    except Exception as e:
        st.error(f"Could not load audio: {e}")
        return None, None

def bandpass_filter(data, lowcut, highcut, fs, numtaps=101):
    taps = firwin(numtaps, [lowcut, highcut], pass_zero=False, fs=fs)
    return lfilter(taps, 1.0, data)

def apply_equalizer(data, fs, gains):
    bands = [(60, 250), (250, 4000), (4000, 10000)]  # Bass, Mid, Treble
    processed = np.zeros_like(data)
    for (low, high), gain in zip(bands, gains):
        filtered = bandpass_filter(data, low, high, fs)
        processed += filtered * gain
    return processed

# --- Sidebar Navigation ---
st.sidebar.title("🎧 Navigation")
page = st.sidebar.radio("Go to", ["🏠 Home", "🎛️ Equalizer"])

# --- Home Page ---
if page == "🏠 Home":
    st.title("🌟 Welcome to Hot Pink DJ Equalizer")
    st.markdown("""
    ### 🎵 Customize your sound. Look cool doing it.
    This app lets you:
    - 🎚️ Adjust Bass, Midrange, and Treble
    - 🎧 Preview audio instantly
    - 📉 See waveforms for original and processed tracks
    - 💾 Download your remixed sound

    ---
    #### 🔧 Supported Formats:
    - `.wav`, `.mp3` (max size: 100 MB)

    ---
    ### 👉 Get started by clicking "🎛️ Equalizer" in the sidebar!
    """)
    st.image("https://media.giphy.com/media/3o6Zt481isNVuQI1l6/giphy.gif", use_column_width=True)

# --- Equalizer Page ---
elif page == "🎛️ Equalizer":
    st.title("🎛️ Digital Music Equalizer")

    uploaded_file = st.file_uploader("🎵 Upload your audio track (WAV or MP3)", type=["wav", "mp3"])

    if uploaded_file is not None:
        file_size_mb = uploaded_file.size / (1024 * 1024)
        if file_size_mb > 100:
            st.error("⚠️ File size exceeds 100 MB limit. Please upload a smaller file.")
        else:
            data, fs = load_audio(uploaded_file)
            if data is not None:
                st.audio(uploaded_file)

                st.subheader("🎚️ Adjust the Frequencies")
                bass = st.slider("Bass Boost (60–250 Hz)", 0.0, 2.0, 1.0, 0.1)
                mid = st.slider("Midrange Boost (250 Hz – 4 kHz)", 0.0, 2.0, 1.0, 0.1)
                treble = st.slider("Treble Boost (4–10 kHz)", 0.0, 2.0, 1.0, 0.1)

                output = apply_equalizer(data, fs, [bass, mid, treble])

                # Save and play
                buf = io.BytesIO()
                sf.write(buf, output, fs, format='WAV')
                buf.seek(0)
                st.audio(buf, format='audio/wav')
                st.download_button("⬇️ Download Processed Audio", buf.getvalue(), file_name="hotpink_equalized_output.wav")

                # --- Before and After Waveform ---
                st.subheader("🔊 Original vs Processed Audio Waveforms")

                fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
                time = np.linspace(0, len(data) / fs, num=len(data))

                ax1.plot(time, data, color="#ffffff", linewidth=0.5)
                ax1.set_title("Original Audio", fontsize=12, color='#ffffff')
                ax1.set_ylabel("Amplitude", color='white')
                ax1.set_facecolor("#0a0a0a")
                ax1.tick_params(colors='white')

                ax2.plot(time, output, color="#ff69b4", linewidth=0.5)
                ax2.set_title("Processed Audio", fontsize=12, color='#ff69b4')
                ax2.set_xlabel("Time [s]", color='white')
                ax2.set_ylabel("Amplitude", color='white')
                ax2.set_facecolor("#0a0a0a")
                ax2.tick_params(colors='white')

                fig.patch.set_facecolor("#0a0a0a")
                plt.tight_layout()
                st.pyplot(fig)
