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
    aspect_ratio = st.selectbox("Aspect Ratio", ["16:9", "9:16", "1:1"])

prompt = st.text_area("Describe your scene...", placeholder="A futuristic robot cyberpunk city, heavy rain, camera panning down...")

if st.button("🎬 Render Video", type="primary"):
    if not replicate_key:
        st.error("Please enter your Replicate API Token in the sidebar!")
    elif not prompt:
        st.warning("Please type a prompt first!")
    else:
        with st.spinner("Generating video via Lightricks LTX-Video Cloud... (takes ~15-30 seconds)..."):
            try:
                os.environ["REPLICATE_API_TOKEN"] = replicate_key
                
                # Using the official public stable model path
                output = replicate.run(
                    "lightricks/ltx-video",
                    input={
                        "prompt": prompt,
                        "aspect_ratio": aspect_ratio
                    }
                )
                
                st.success("Render complete!")
                
                # Handle output list or single URL string correctly
                video_url = output[0] if isinstance(output, list) else output
                st.video(video_url)
                
            except Exception as e:
                st.error(f"Error occurred during generation: {e}")
