import streamlit as st
import os
# Humne naye function ka naam import kiya hai yahan
from ai_logic import decode_medical_report

# Page Configuration
st.set_page_config(page_title="Medical Guided Gemini", page_icon=None, layout="wide")

# Fixed & Enhanced Ultra-Futuristic CSS
st.markdown("""
    <style>
    /* Main container forcing the sci-fi dark space background */
    .stApp, [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at 50% 50%, #06152d 0%, #020617 100%) !important;
        color: #e2e8f0 !important;
        font-family: 'Inter', sans-serif;
    }

    /* Fixed Continuous Floating Particles Layer */
    [data-testid="stAppViewContainer"]::before {
        content: "";
        position: absolute;
        width: 200%;
        height: 200%;
        top: -50%;
        left: -50%;
        background-image: 
            radial-gradient(#ffffff 1px, transparent 20px),
            radial-gradient(rgba(0, 210, 255, 0.4) 1.5px, transparent 30px),
            radial-gradient(rgba(255, 255, 255, 0.15) 1px, transparent 40px);
        background-size: 400px 400px, 250px 250px, 300px 300px;
        background-position: 0 0, 60px 120px, 130px 200px;
        animation: particleFly 90s linear infinite !important;
        opacity: 0.6;
        z-index: 0;
        pointer-events: none;
    }

    @keyframes particleFly {
        from { transform: translateY(0px) rotate(0deg); }
        to { transform: translateY(-150px) rotate(360deg); }
    }

    /* Bringing all main elements above the particle layer */
    .stMainBlockContainer, [data-testid="stSidebarUserContent"] {
        position: relative;
        z-index: 10;
    }

    /* Sidebar Glassmorphism Fixes */
    [data-testid="stSidebar"] {
        background: rgba(3, 10, 23, 0.75) !important;
        backdrop-filter: blur(25px) !important;
        border-right: 1px solid rgba(0, 210, 255, 0.15) !important;
    }

    /* Cyberpunk Heading Dynamic Neon Text */
    h1 {
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 50%, #00f2fe 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shineText 5s linear infinite;
        text-align: center;
        font-weight: 800;
        font-size: 3.2rem !important;
        letter-spacing: -1px;
        margin-top: 10px;
    }

    @keyframes shineText {
        to { background-position: 200% center; }
    }

    .sub-text {
        text-align: center;
        color: #64748b;
        margin-bottom: 45px;
        font-size: 0.95rem;
        text-transform: uppercase;
        letter-spacing: 4px;
    }

    /* Fixed Glassmorphic Input Area Containers */
    .stTextArea textarea, .stFileUploader section {
        background: rgba(6, 20, 40, 0.5) !important;
        border: 1px solid rgba(0, 210, 255, 0.25) !important;
        border-radius: 14px !important;
        color: #f8fafc !important;
        backdrop-filter: blur(12px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.6);
    }
    
    .stTextArea textarea:focus {
        border-color: #00f2fe !important;
        box-shadow: 0 0 15px rgba(0, 242, 254, 0.4) !important;
    }

    /* Exact Sci-Fi Capsule Glowing Button */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #0052d4 0%, #4facfe 50%, #00f2fe 100%) !important;
        background-size: 200% auto !important;
        color: white !important;
        border: none !important;
        padding: 14px 40px !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        border-radius: 50px !important;
        transition: 0.4s all ease-in-out !important;
        box-shadow: 0 0 20px rgba(79, 172, 254, 0.4) !important;
        width: 100%;
        margin-top: 20px;
    }

    div.stButton > button:first-child:hover {
        background-position: right center !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 0 35px rgba(0, 242, 254, 0.8) !important;
    }

    /* File uploader drag drop text color fixing */
    .stFileUploader section div {
        color: #94a3b8 !important;
    }

    hr {
        border-color: rgba(0, 210, 255, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar Settings Control Panel
with st.sidebar:
    st.markdown("<h2 style='color: #00f2fe; font-size: 1.3rem; letter-spacing: 2px; font-weight:700;'>SYSTEM CONTROL</h2>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748b; font-size: 0.8rem; letter-spacing: 1px;'>HYBRID AI SYSTEM</p>", unsafe_allow_html=True)
    st.info("Primary Engine: Gemini 2.5\n\nBackup Engine: Groq Llama 3 (Auto Switch Active)")

# Main Screen Dashboard
st.markdown("<h1>Ready when you are.</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-text'>Decode complex medical documents effortlessly.</p>", unsafe_allow_html=True)

# Core UI Layout Centering
col1, col2, col3 = st.columns([1, 5, 1])

with col2:
    # Text input block
    st.markdown("<p style='color: #00f2fe; font-size: 0.85rem; font-weight: bold; letter-spacing: 1.5px; margin-bottom:5px;'>USER QUERY</p>", unsafe_allow_html=True)
    user_query = st.text_area(
        "", 
        placeholder="Type your medical query or document summary questions here...",
        height=130
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # File Uploader block
    st.markdown("<p style='color: #00f2fe; font-size: 0.85rem; font-weight: bold; letter-spacing: 1.5px; margin-bottom:5px;'>UPLOAD REPORT IMAGES (PNG/JPG)</p>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["png", "jpg", "jpeg"])
    
    # PRO TIP: File ko local device par save karne ke bajaye seedha bytes read kar rahe hain
    image_bytes = None
    if uploaded_file is not None:
        image_bytes = uploaded_file.getvalue()

    # Action Trigger Button
    if st.button("DECODE JARGON"):
        if not user_query.strip() and image_bytes is None:
            st.warning("Kripya kuch poocho ya report upload karo.")
        else:
            with st.spinner("Analyzing data across Hybrid Engines..."):
                # Naye dual-engine function ko call kiya
                response = decode_medical_report(image_bytes, user_query)
            
            st.markdown("---")
            st.markdown("<h3 style='color: #00f2fe; letter-spacing: 1px; font-weight:600;'>ANALYSIS RESULT</h3>", unsafe_allow_html=True)
            
            # Markdown text rendering inside the Sci-Fi Glowing Output Display Box
            st.markdown(f"""
            <div style="background: rgba(6, 22, 45, 0.65); padding: 25px; border-radius: 14px; border-left: 4px solid #00f2fe; box-shadow: 0 15px 40px rgba(0,0,0,0.6); backdrop-filter: blur(14px); color: #e2e8f0; border-top: 1px solid rgba(0, 210, 255, 0.1); font-size: 1.05rem; line-height: 1.6;">
                {response}
            </div>
            """, unsafe_allow_html=True)
            