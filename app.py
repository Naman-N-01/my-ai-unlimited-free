import streamlit as st
import replicate
import os

st.set_page_config(page_title="OpenHiggs Studio", layout="wide", page_icon="🎬")
st.title("🎬 OpenHiggs Cinema Studio")
st.caption("Generate cinematic AI videos instantly from your public link.")

with st.sidebar:
    st.header("Settings")
    replicate_key = st.text_input("Enter Replicate API Token", type="password")
    st.markdown("---")
    st.markdown("### Camera Controls")
    motion = st.slider("Motion Intensity", 1, 10, 5)

prompt = st.text_area("Describe your scene...", placeholder="A futuristic robot cyberpunk city, heavy rain, camera panning down...")

if st.button("🎬 Render Video", type="primary"):
    if not replicate_key:
        st.error("Please enter your Replicate API Token in the sidebar!")
    elif not prompt:
        st.warning("Please type a prompt first!")
    else:
        with st.spinner("Generating video (takes ~15-30 seconds)..."):
            try:
                os.environ["REPLICATE_API_TOKEN"] = replicate_key
                
                # Runs a completely free/open-source light video model pipeline
                output = replicate.run(
                    "fofr/ltx-video:3d9c727",
                    input={
                        "prompt": prompt,
                        "num_frames": 32
                    }
                )
                
                st.success("Render complete!")
                st.video(output)
            except Exception as e:
                st.error(f"Error occurred during generation: {e}")
