# --- Intro Page ---
elif st.session_state.page == "equalizer":
    if "show_intro" not in st.session_state:
        st.session_state.show_intro = True

    if st.session_state.show_intro:
        st.title("🎛️ Welcome to the Digital Music Equalizer")

        st.markdown("""
        This tool lets you enhance your audio with studio-level precision. You can:
        - Upload any **WAV or MP3** file.
        - Boost or cut **bass**, **midrange**, and **treble** frequencies.
        - Instantly listen and download the processed audio.

        👉 Click **Continue to Equalizer** to begin!
        """)

        if st.button("🎚️ Continue to Equalizer"):
            st.session_state.show_intro = False
            st.rerun()

    else:
        st.title("🎚️ Digital Music Equalizer")

        uploaded_file = st.file_uploader("🎵 Upload your audio track (WAV or MP3)", type=["wav", "mp3"])

        if uploaded_file is not None:
            file_size_mb = uploaded_file.size / (1024 * 1024)
            if file_size_mb > 100:
                st.error("⚠️ File size exceeds 100 MB limit. Please upload a smaller file.")
            else:
                data, fs = load_audio(uploaded_file)
                st.audio(uploaded_file)

                st.subheader("🎚️ Adjust the Frequencies")
                bass = st.slider("Bass Boost (60–250 Hz)", 0.0, 2.0, 1.0, 0.1)
                mid = st.slider("Midrange Boost (250 Hz – 4 kHz)", 0.0, 2.0, 1.0, 0.1)
                treble = st.slider("Treble Boost (4–10 kHz)", 0.0, 2.0, 1.0, 0.1)

                output = apply_equalizer(data, fs, [bass, mid, treble])

                # Save and play
                buf = io.BytesIO()
                sf.write(buf, output, fs, format='WAV')
                st.audio(buf, format='audio/wav')
                st.download_button("⬇️ Download Processed Audio", buf.getvalue(), file_name="hotpink_equalized_output.wav")

                # Visualization
                st.subheader("🔊 Original vs. Processed Waveform")
                fig, ax = plt.subplots(figsize=(10, 4))
                time = np.linspace(0, len(data) / fs, num=len(data))
                ax.plot(time, data, color="white", linewidth=0.5, label="Original")
                ax.plot(time, output, color="#ff69b4", linewidth=0.5, label="Processed")
                ax.set_title("Audio Waveform Comparison", fontsize=12, color='white')
                ax.set_xlabel("Time [s]", color='white')
                ax.set_ylabel("Amplitude", color='white')
                ax.set_facecolor("#0a0a0a")
                ax.tick_params(colors='white')
                ax.legend(facecolor="#1a001a", edgecolor='white', labelcolor='white')
                fig.patch.set_facecolor("#0a0a0a")
                st.pyplot(fig)
