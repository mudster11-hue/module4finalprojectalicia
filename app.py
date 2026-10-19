import datetime
import streamlit as st
from PIL import Image
from services.api_handler import process_image_edit

st.set_page_config(
    page_title="AI Image Editing Platform MVP",
    page_icon="🎨",
    layout="wide"
)

st.title("🎨 AI-Powered Image Editing Platform")
st.markdown("Next-gen visual editing powered by Natural Language & GenAI APIs.")

# Initialize session state for version history / image library
if "image_history" not in st.session_state:
    st.session_state["image_history"] = []  # List of dicts storing versions

uploaded_file = st.file_uploader("Upload an image to start editing...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # If a new file is uploaded, initialize history if empty or changed
    raw_image = Image.open(uploaded_file)
    
    if not st.session_state["image_history"]:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state["image_history"].append({
            "version_id": 0,
            "title": "Original Upload",
            "image": raw_image,
            "prompt": "Initial Upload",
            "timestamp": timestamp,
            "ai_notes": "Original source image loaded into workspace."
        })

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("🛠️ Edit Controls")
        prompt_text = st.text_input(
            "Natural Language Edit Instruction:", 
            placeholder="e.g., Make it black and white, add blur, increase contrast..."
        )

        if st.button("Apply AI Edit", type="primary"):
            if not prompt_text.strip():
                st.warning("Please enter an edit instruction first.")
            else:
                with st.spinner("AI is interpreting prompt and processing image..."):
                    try:
                        # Get latest active version as input base
                        latest_version = st.session_state["image_history"][-1]["image"]
                        
                        # Process edit via API handler
                        new_image, ai_feedback = process_image_edit(latest_version, prompt_text)
                        
                        # Save to version history timeline
                        new_version_id = len(st.session_state["image_history"])
                        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        
                        st.session_state["image_history"].append({
                            "version_id": new_version_id,
                            "title": f"Edit #{new_version_id}: {prompt_text}",
                            "image": new_image,
                            "prompt": prompt_text,
                            "timestamp": timestamp,
                            "ai_notes": ai_feedback
                        })
                        st.success(f"Successfully created Version #{new_version_id}!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error processing edit: {e}")

        # Quick preset buttons as specified in project core tasks
        st.markdown("### Quick Presets")
        preset_cols = st.columns(3)
        if preset_cols[0].button("Make Black & White"):
            latest_version = st.session_state["image_history"][-1]["image"]
            new_image, ai_feedback = process_image_edit(latest_version, "Convert to black and white")
            new_version_id = len(st.session_state["image_history"])
            st.session_state["image_history"].append({
                "version_id": new_version_id,
                "title": f"Edit #{new_version_id}: Black & White Preset",
                "image": new_image,
                "prompt": "Convert to black and white",
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "ai_notes": ai_feedback
            })
            st.rerun()

        if preset_cols[1].button("Apply Soft Blur"):
            latest_version = st.session_state["image_history"][-1]["image"]
            new_image, ai_feedback = process_image_edit(latest_version, "Apply soft blur")
            new_version_id = len(st.session_state["image_history"])
            st.session_state["image_history"].append({
                "version_id": new_version_id,
                "title": f"Edit #{new_version_id}: Soft Blur Preset",
                "image": new_image,
                "prompt": "Apply soft blur",
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "ai_notes": ai_feedback
            })
            st.rerun()

        if preset_cols[2].button("Boost Contrast"):
            latest_version = st.session_state["image_history"][-1]["image"]
            new_image, ai_feedback = process_image_edit(latest_version, "Increase contrast")
            new_version_id = len(st.session_state["image_history"])
            st.session_state["image_history"].append({
                "version_id": new_version_id,
                "title": f"Edit #{new_version_id}: Boost Contrast Preset",
                "image": new_image,
                "prompt": "Increase contrast",
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "ai_notes": ai_feedback
            })
            st.rerun()

    with col2:
        st.subheader("🖼️ Current Active View")
        latest_item = st.session_state["image_history"][-1]
        st.image(
            latest_item["image"], 
            caption=f"{latest_item['title']} ({latest_item['timestamp']})", 
            use_container_width=True
        )
        st.info(f"**AI Notes:** {latest_item['ai_notes']}")

    # --- VERSION HISTORY TIMELINE (Week 2 Deliverable) ---
    st.divider()
    st.subheader("🕒 Edit Version History Timeline")
    
    history_cols = st.columns(len(st.session_state["image_history"]))
    for idx, version in enumerate(st.session_state["image_history"]):
        with history_cols[idx]:
            st.image(version["image"], use_container_width=True)
            st.caption(f"**v{version['version_id']}**: {version['prompt']}")
            st.text(version["timestamp"])

else:
    st.info("Upload an image above to begin your editing session and track version history.")