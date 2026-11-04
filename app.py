import streamlit as st
import fal_client
import os

st.set_page_config(page_title="OpenHiggs Studio", layout="wide", page_icon="🎬")
st.title("🎬 OpenHiggs Cinema Studio")
st.caption("Generate cinematic AI videos instantly from your public link.")

with st.sidebar:
    st.header("Settings")
    fal_key = st.text_input("Enter Fal.ai API Key", type="password")
    st.markdown("---")
    st.markdown("### Camera Controls")
    motion = st.slider("Motion Intensity", 1, 10, 5)
    aspect_ratio = st.selectbox("Aspect Ratio", ["16:9", "9:16", "1:1"])

prompt = st.text_area("Describe your scene...", placeholder="A futuristic robot cyberpunk city, heavy rain, camera panning down...")

if st.button("🎬 Render Video", type="primary"):
    if not fal_key:
        st.error("Please enter a Fal.ai API Key in the sidebar to generate videos!")
    elif not prompt:
        st.warning("Please type a prompt first!")
    else:
        with st.spinner("Generating video (takes ~15 seconds)..."):
            try:
                # Tell the system your key before running the model
                os.environ["FAL_KEY"] = fal_key
                
                handler = fal_client.submit(
                    "fal-ai/kling-video/v1/standard/text-to-video", 
                    arguments={
                        "prompt": prompt,
                        "aspect_ratio": aspect_ratio,
                    }
                )
                result = handler.get()
                video_url = result['video']['url']
                st.success("Render complete!")
                st.video(video_url)
            except Exception as e:
                st.error(f"Error occurred during generation: {e}")
