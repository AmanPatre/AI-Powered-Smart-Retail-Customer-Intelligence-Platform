"""Streamlit Dashboard for Smart Retail & Customer Intelligence Platform (Crextio Theme Edition)."""

import os
import sys
import requests
import streamlit as st
import pandas as pd
from PIL import Image
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="Crextio Retail | Customer Intelligence Platform",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS matching Crextio Warm Cream & Gold/Yellow Aesthetic
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    /* Global App Background & Typography */
    .stApp {
        background-color: #F6F5F0 !important;
        background-image: 
            radial-gradient(circle at 92% 8%, rgba(253, 224, 71, 0.35) 0%, transparent 45%),
            radial-gradient(circle at 8% 92%, rgba(250, 204, 21, 0.12) 0%, transparent 40%) !important;
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
        color: #18181B !important;
    }

    /* Streamlit Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #ECEBE5 !important;
        border-right: 1px solid rgba(0, 0, 0, 0.05) !important;
        padding-top: 1rem !important;
    }

    /* Sidebar all text visible */
    [data-testid="stSidebar"] * {
        color: #18181B !important;
    }

    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #18181B !important;
        font-weight: 600 !important;
    }

    /* Sidebar radio button labels */
    [data-testid="stSidebar"] [data-testid="stRadio"] label {
        color: #18181B !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
        color: #18181B !important;
        background: rgba(250, 204, 21, 0.2) !important;
        border-radius: 8px !important;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #18181B !important;
        font-weight: 700 !important;
        font-size: 15px !important;
    }

    /* Top Brand Navigation Header Bar */
    .brand-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #FFFFFF;
        border-radius: 9999px;
        padding: 12px 28px;
        margin-bottom: 24px;
        border: 1px solid rgba(0, 0, 0, 0.05);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.02);
    }
    
    .brand-logo {
        font-size: 22px;
        font-weight: 800;
        letter-spacing: -0.6px;
        color: #18181B;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .brand-pill-active {
        background: #18181B;
        color: #FFFFFF;
        padding: 8px 20px;
        border-radius: 9999px;
        font-size: 13px;
        font-weight: 700;
    }

    .brand-pill-light {
        background: #F4F4F5;
        color: #52525B;
        padding: 8px 16px;
        border-radius: 9999px;
        font-size: 13px;
        font-weight: 600;
    }

    /* Crextio Card Containers */
    .crextio-card {
        background: #FFFFFF;
        border-radius: 24px;
        padding: 24px 28px;
        border: 1px solid rgba(0, 0, 0, 0.05);
        box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.03), 0 4px 12px -2px rgba(0, 0, 0, 0.02);
        margin-bottom: 20px;
    }

    .crextio-card-dark {
        background: #18181B;
        color: #FFFFFF;
        border-radius: 24px;
        padding: 24px 28px;
        box-shadow: 0 12px 36px rgba(0, 0, 0, 0.12);
        margin-bottom: 20px;
    }

    /* Metric Badges & Highlight Tags */
    .tag-yellow {
        background: #FACC15;
        color: #18181B;
        font-weight: 800;
        padding: 6px 14px;
        border-radius: 9999px;
        font-size: 12px;
        display: inline-block;
    }

    .tag-dark {
        background: #18181B;
        color: #FFFFFF;
        font-weight: 700;
        padding: 6px 14px;
        border-radius: 9999px;
        font-size: 12px;
        display: inline-block;
    }

    .tag-gray {
        background: #E4E4E7;
        color: #52525B;
        font-weight: 600;
        padding: 6px 14px;
        border-radius: 9999px;
        font-size: 12px;
        display: inline-block;
    }

    /* Crextio Metric Pill Display */
    .metric-pill-val {
        font-size: 38px;
        font-weight: 800;
        color: #18181B;
        letter-spacing: -1px;
        line-height: 1.1;
    }

    .metric-pill-label {
        font-size: 13px;
        font-weight: 600;
        color: #71717A;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
    }

    /* Custom Streamlit Buttons */
    .stButton > button {
        background: #18181B !important;
        color: #FFFFFF !important;
        border-radius: 9999px !important;
        border: none !important;
        padding: 12px 28px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.12) !important;
    }

    .stButton > button:hover {
        background: #FACC15 !important;
        color: #18181B !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(250, 204, 21, 0.45) !important;
    }

    /* Streamlit Metric Overrides */
    [data-testid="stMetricValue"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 800 !important;
        color: #18181B !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 600 !important;
        color: #71717A !important;
    }


    /* Text Inputs & Area */
    .stTextArea textarea, .stTextInput input {
        background-color: #FFFFFF !important;
        border: 1px solid #E4E4E7 !important;
        border-radius: 16px !important;
        color: #18181B !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        padding: 14px !important;
    }

    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #FACC15 !important;
        box-shadow: 0 0 0 3px rgba(250, 204, 21, 0.25) !important;
    }

    /* ============================================
       GLOBAL TEXT VISIBILITY OVERRIDES
       ============================================ */

    /* All paragraph, span, div text in main area = dark */
    .main p, .main span, .main div, .main label {
        color: #18181B !important;
    }

    /* Streamlit markdown text */
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] span,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3 {
        color: #18181B !important;
    }

    /* FILE UPLOADER - drag zone text */
    [data-testid="stFileUploader"] {
        background: #FFFFFF !important;
        border-radius: 20px !important;
        border: 2px dashed #E4E4E7 !important;
    }

    [data-testid="stFileUploader"] * {
        color: #18181B !important;
    }

    [data-testid="stFileUploader"] section {
        background: #FFFFFF !important;
        border-radius: 16px !important;
        border: 2px dashed #D4D4D8 !important;
    }

    [data-testid="stFileUploader"] section > div {
        color: #18181B !important;
    }

    [data-testid="stFileUploaderDropzoneInstructions"] div,
    [data-testid="stFileUploaderDropzoneInstructions"] span {
        color: #18181B !important;
        font-weight: 600 !important;
    }

    [data-testid="stFileUploaderDropzone"] {
        background: #FAFAFA !important;
        border-radius: 16px !important;
    }

    [data-testid="stFileUploaderDropzone"] * {
        color: #18181B !important;
    }

    /* CHAT MESSAGES */
    [data-testid="stChatMessage"] {
        background: #FFFFFF !important;
        border-radius: 16px !important;
        border: 1px solid #E4E4E7 !important;
        margin-bottom: 8px !important;
    }

    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] span,
    [data-testid="stChatMessage"] div {
        color: #18181B !important;
    }

    [data-testid="stChatMessageContent"] p,
    [data-testid="stChatMessageContent"] span {
        color: #18181B !important;
        font-weight: 500 !important;
    }

    /* CHAT INPUT */
    [data-testid="stChatInput"] {
        background: #FFFFFF !important;
        border: 1.5px solid #E4E4E7 !important;
        border-radius: 9999px !important;
    }

    [data-testid="stChatInput"] textarea {
        color: #18181B !important;
        background: transparent !important;
    }

    /* INFO / WARNING / ERROR BOXES */
    [data-testid="stAlert"] {
        border-radius: 14px !important;
    }

    [data-testid="stAlert"] p {
        color: #18181B !important;
        font-weight: 600 !important;
    }

    .stInfo, .stSuccess, .stWarning, .stError {
        border-radius: 14px !important;
    }

    /* LABELS for all widgets */
    .stSelectbox label,
    .stTextInput label,
    .stTextArea label,
    .stFileUploader label,
    .stRadio label,
    .stCheckbox label,
    [data-testid="stWidgetLabel"] p {
        color: #18181B !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    /* DATAFRAME */
    [data-testid="stDataFrame"] * {
        color: #18181B !important;
    }

    /* SPINNER TEXT */
    .stSpinner p {
        color: #18181B !important;
    }

    /* CAPTION TEXT */
    [data-testid="stCaptionContainer"] p {
        color: #71717A !important;
        font-weight: 500 !important;
    }

    /* SUBHEADER AND HEADERS in main */
    .main h1, .main h2, .main h3, .main h4 {
        color: #18181B !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    /* Hide standard header decoration */
    header[data-testid="stHeader"] {
        background: transparent !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Backend API Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
API_KEY = os.getenv("API_KEY", "smart_retail_secret_key_2026")
HEADERS = {"X-API-Key": API_KEY}


def fetch_stats():
    """Fetch dashboard statistics from FastAPI backend."""
    try:
        res = requests.get(f"{API_BASE_URL}/dashboard/stats", headers=HEADERS, timeout=5)
        if res.status_code == 200:
            return res.json()
    except Exception as e:
        st.sidebar.error(f"Backend Offline ({API_BASE_URL})")
    return None


def render_brand_header():
    """Render top nav bar matching Crextio header."""
    st.markdown(
        """
        <div class="brand-header">
            <div class="brand-logo">
                🛍️ Crextio <span class="brand-badge">Retail AI</span>
            </div>
            <div style="display: flex; gap: 10px; align-items: center;">
                <span class="brand-pill-active">Dashboard</span>
                <span class="brand-pill-light">Vision AI</span>
                <span class="brand-pill-light">NLP Analytics</span>
                <span class="brand-pill-light">Chatbot</span>
                <span style="background: #F4F4F5; border-radius: 9999px; padding: 8px; margin-left: 8px;">⚙️</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main():
    render_brand_header()

    # Sidebar Navigation
    st.sidebar.markdown("### 🎛️ Navigation")
    page = st.sidebar.radio(
        "Select View",
        [
            "Overview & Metrics",
            "Product Image Classifier",
            "Face Recognition & Visits",
            "Sentiment Analysis",
            "FAQ Chatbot",
        ],
    )

    stats = fetch_stats()

    if page == "Overview & Metrics":
        render_overview(stats)
    elif page == "Product Image Classifier":
        render_product_classifier()
    elif page == "Face Recognition & Visits":
        render_face_recognition()
    elif page == "Sentiment Analysis":
        render_sentiment_analysis(stats)
    elif page == "FAQ Chatbot":
        render_chatbot()


def render_overview(stats):
    st.markdown("<h1 style='font-weight: 800; letter-spacing: -1px; margin-bottom: 2px;'>Welcome back, Retail Insights</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #71717A; font-weight: 500; font-size: 15px; margin-bottom: 24px;'>Real-time computer vision, NLP sentiment & customer intelligence engine</p>", unsafe_allow_html=True)

    # Top Metric Progress Bar Cards (Matching reference screenshot top row)
    top_col1, top_col2, top_col3, top_col4 = st.columns(4)

    total_customers = stats.get("total_customers", 0) if stats else 0
    total_visits = stats.get("total_visits", 0) if stats else 0
    total_reviews = stats.get("total_reviews", 0) if stats else 0
    total_chats = stats.get("total_chat_queries", 0) if stats else 0

    with top_col1:
        st.markdown(
            f"""
            <div class="crextio-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span class="metric-pill-label">Registered Customers</span>
                    <span class="tag-dark">15% Active</span>
                </div>
                <div class="metric-pill-val" style="margin-top: 10px;">{total_customers}</div>
                <div style="color: #71717A; font-size: 12px; font-weight: 600; margin-top: 6px;">👥 Verified Customer Profiles</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with top_col2:
        st.markdown(
            f"""
            <div class="crextio-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span class="metric-pill-label">Total Store Visits</span>
                    <span class="tag-yellow">60% Traffic</span>
                </div>
                <div class="metric-pill-val" style="margin-top: 10px;">{total_visits}</div>
                <div style="color: #71717A; font-size: 12px; font-weight: 600; margin-top: 6px;">📹 OpenCV Face Check-Ins</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with top_col3:
        st.markdown(
            f"""
            <div class="crextio-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span class="metric-pill-label">Customer Reviews</span>
                    <span class="tag-gray">NLP Active</span>
                </div>
                <div class="metric-pill-val" style="margin-top: 10px;">{total_reviews}</div>
                <div style="color: #71717A; font-size: 12px; font-weight: 600; margin-top: 6px;">💬 TF-IDF Sentiment Feed</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with top_col4:
        st.markdown(
            f"""
            <div class="crextio-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span class="metric-pill-label">FAQ Chatbot Queries</span>
                    <span class="tag-yellow">88% Auto</span>
                </div>
                <div class="metric-pill-val" style="margin-top: 10px;">{total_chats}</div>
                <div style="color: #71717A; font-size: 12px; font-weight: 600; margin-top: 6px;">🤖 Hybrid Intent Engine</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    # Main Grid (Left Analytics + Right Crextio Dark Panel)
    col_main_left, col_main_right = st.columns([2, 1])

    with col_main_left:
        st.markdown(
            """
            <div class="crextio-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                    <h3 style="font-weight: 800; font-size: 18px; margin: 0;">🎭 Customer Sentiment Distribution</h3>
                    <span class="tag-yellow">Real-time NLP</span>
                </div>
            """,
            unsafe_allow_html=True,
        )
        if stats and "sentiment_breakdown" in stats:
            s_data = stats["sentiment_breakdown"]
            df_sent = pd.DataFrame(list(s_data.items()), columns=["Sentiment", "Count"])
            st.bar_chart(df_sent.set_index("Sentiment"), color="#FACC15")
        else:
            st.info("No sentiment metrics available.")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            """
            <div class="crextio-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                    <h3 style="font-weight: 800; font-size: 18px; margin: 0;">🕒 Store Visit Log</h3>
                    <span class="tag-dark">Live Check-ins</span>
                </div>
            """,
            unsafe_allow_html=True,
        )
        if stats and "recent_visits" in stats and stats["recent_visits"]:
            st.dataframe(pd.DataFrame(stats["recent_visits"]), use_container_width=True)
        else:
            st.info("No store visits logged yet.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_main_right:
        # Dark Contrast Card matching the Crextio "Onboarding Task" container in reference image
        st.markdown(
            f"""
            <div class="crextio-card-dark">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                    <span style="font-weight: 800; font-size: 18px; color: #FFFFFF;">Retail Tasks</span>
                    <span style="font-weight: 800; font-size: 20px; color: #FACC15;">4/5</span>
                </div>
                
                <div style="display: flex; align-items: center; justify-content: space-between; background: rgba(255,255,255,0.08); padding: 14px 18px; border-radius: 16px; margin-bottom: 10px;">
                    <div>
                        <div style="font-weight: 700; font-size: 14px; color: #FFFFFF;">MobileNetV2 Vision</div>
                        <div style="font-size: 12px; color: #A1A1AA;">5 Product Categories</div>
                    </div>
                    <span style="background: #FACC15; color: #18181B; border-radius: 9999px; padding: 4px 10px; font-weight: 800; font-size: 13px;">✓</span>
                </div>

                <div style="display: flex; align-items: center; justify-content: space-between; background: rgba(255,255,255,0.08); padding: 14px 18px; border-radius: 16px; margin-bottom: 10px;">
                    <div>
                        <div style="font-weight: 700; font-size: 14px; color: #FFFFFF;">OpenCV Face Encoding</div>
                        <div style="font-size: 12px; color: #A1A1AA;">Euclidean L2 Matcher</div>
                    </div>
                    <span style="background: #FACC15; color: #18181B; border-radius: 9999px; padding: 4px 10px; font-weight: 800; font-size: 13px;">✓</span>
                </div>

                <div style="display: flex; align-items: center; justify-content: space-between; background: rgba(255,255,255,0.08); padding: 14px 18px; border-radius: 16px; margin-bottom: 10px;">
                    <div>
                        <div style="font-weight: 700; font-size: 14px; color: #FFFFFF;">TF-IDF Sentiment Pipeline</div>
                        <div style="font-size: 12px; color: #A1A1AA;">Logistic Regression NLP</div>
                    </div>
                    <span style="background: #FACC15; color: #18181B; border-radius: 9999px; padding: 4px 10px; font-weight: 800; font-size: 13px;">✓</span>
                </div>

                <div style="display: flex; align-items: center; justify-content: space-between; background: rgba(255,255,255,0.08); padding: 14px 18px; border-radius: 16px;">
                    <div>
                        <div style="font-weight: 700; font-size: 14px; color: #FFFFFF;">FAQ Chatbot Intents</div>
                        <div style="font-size: 12px; color: #A1A1AA;">Hybrid Rule + ML Matcher</div>
                    </div>
                    <span style="background: #FACC15; color: #18181B; border-radius: 9999px; padding: 4px 10px; font-weight: 800; font-size: 13px;">✓</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="crextio-card">
                <h3 style="font-weight: 800; font-size: 18px; margin-bottom: 12px;">💬 FAQ Intents Breakdown</h3>
            """,
            unsafe_allow_html=True,
        )
        if stats and "top_intents" in stats:
            i_data = stats["top_intents"]
            df_intents = pd.DataFrame(list(i_data.items()), columns=["Intent Tag", "Queries"])
            st.bar_chart(df_intents.set_index("Intent Tag"), color="#18181B")
        else:
            st.info("No chatbot query data logged yet.")
        st.markdown("</div>", unsafe_allow_html=True)


def render_product_classifier():
    st.markdown("<h1 style='font-weight: 800; letter-spacing: -1px;'>📦 Product Image Classification</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #71717A; font-weight: 500; margin-bottom: 24px;'>MobileNetV2 deep learning transfer model (Apparel, Electronics, Footwear, Groceries, Home Goods)</p>", unsafe_allow_html=True)

    st.markdown('<div class="crextio-card">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload Product Image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        col1, col2 = st.columns([1, 1])
        with col1:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)

        with col2:
            if st.button("Classify Product Category"):
                with st.spinner("Analyzing image features..."):
                    try:
                        bytes_data = uploaded_file.getvalue()
                        files = {"file": (uploaded_file.name, bytes_data, uploaded_file.type)}
                        res = requests.post(
                            f"{API_BASE_URL}/classify-product",
                            headers=HEADERS,
                            files=files,
                            timeout=10,
                        )

                        if res.status_code == 200:
                            data = res.json()
                            st.markdown(f"<div class='tag-yellow' style='font-size: 16px; padding: 8px 18px;'>Predicted: {data['category']}</div>", unsafe_allow_html=True)
                            st.metric("Model Confidence", f"{data['confidence']*100:.1f}%")

                            probs = data.get("probabilities", {})
                            df_probs = pd.DataFrame(list(probs.items()), columns=["Category", "Probability"])
                            st.bar_chart(df_probs.set_index("Category"), color="#FACC15")
                        else:
                            st.error(f"Error classifying image: {res.text}")
                    except Exception as e:
                        st.error(f"Classification failed: {e}")
    st.markdown('</div>', unsafe_allow_html=True)


def render_face_recognition():
    st.markdown("<h1 style='font-weight: 800; letter-spacing: -1px;'>👤 Returning Customer Face Check-In</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #71717A; font-weight: 500; margin-bottom: 24px;'>OpenCV 128-dimensional facial vector extractor & L2 distance matcher</p>", unsafe_allow_html=True)

    st.markdown('<div class="crextio-card">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload Store Camera Frame...", type=["jpg", "jpeg", "png"], key="face_uploader")

    if uploaded_file is not None:
        col1, col2 = st.columns([1, 1])
        with col1:
            image = Image.open(uploaded_file)
            st.image(image, caption="Entrance Camera Snapshot", use_column_width=True)

        with col2:
            if st.button("Process Face Recognition"):
                with st.spinner("Matching face encodings against database..."):
                    try:
                        bytes_data = uploaded_file.getvalue()
                        files = {"file": (uploaded_file.name, bytes_data, uploaded_file.type)}
                        res = requests.post(
                            f"{API_BASE_URL}/recognize-face",
                            headers=HEADERS,
                            files=files,
                            timeout=10,
                        )

                        if res.status_code == 200:
                            data = res.json()
                            st.markdown(f"<span class='tag-gray'>Faces Detected: {data['faces_detected']}</span>", unsafe_allow_html=True)

                            if data["recognized"] and data["customer"]:
                                cust = data["customer"]
                                st.markdown(
                                    f"""
                                    <div class="crextio-card-dark" style="margin-top: 16px;">
                                        <div class="tag-yellow" style="margin-bottom: 10px;">🎉 CUSTOMER RECOGNIZED</div>
                                        <h2 style="color: #FFFFFF; font-weight: 800; margin: 0;">{cust['name']}</h2>
                                        <p style="color: #A1A1AA; font-size: 14px;">{cust.get('email', 'Registered VIP Customer')}</p>
                                        <div style="display: flex; gap: 20px; margin-top: 16px;">
                                            <div>
                                                <div style="font-size: 11px; color: #A1A1AA;">MATCH CONFIDENCE</div>
                                                <div style="font-size: 24px; font-weight: 800; color: #FACC15;">{data['confidence']*100:.1f}%</div>
                                            </div>
                                            <div>
                                                <div style="font-size: 11px; color: #A1A1AA;">VISIT RECORD ID</div>
                                                <div style="font-size: 24px; font-weight: 800; color: #FFFFFF;">#{data['visit_id']}</div>
                                            </div>
                                        </div>
                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )
                            else:
                                st.warning(data["message"])
                        else:
                            st.error(f"Error processing face recognition: {res.text}")
                    except Exception as e:
                        st.error(f"Face recognition failed: {e}")
    st.markdown('</div>', unsafe_allow_html=True)


def render_sentiment_analysis(stats):
    st.markdown("<h1 style='font-weight: 800; letter-spacing: -1px;'>💬 Review Sentiment Analysis</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #71717A; font-weight: 500; margin-bottom: 24px;'>TF-IDF Vectorizer + Logistic Regression Machine Learning Pipeline</p>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="crextio-card">', unsafe_allow_html=True)
        st.markdown("<h3 style='font-weight: 800; font-size: 18px; margin-bottom: 12px;'>Test Review Sentiment</h3>", unsafe_allow_html=True)
        review_input = st.text_area(
            "Enter Customer Review:",
            value="The customer service team was extremely helpful and resolved my issue immediately!",
            height=120,
        )

        if st.button("Analyze Sentiment"):
            if review_input.strip():
                with st.spinner("Evaluating NLP features..."):
                    try:
                        payload = {"review_text": review_input}
                        res = requests.post(
                            f"{API_BASE_URL}/analyze-sentiment",
                            headers=HEADERS,
                            json=payload,
                            timeout=5,
                        )

                        if res.status_code == 200:
                            data = res.json()
                            sentiment = data["sentiment"]
                            confidence = data["confidence"]

                            tag_cls = "tag-yellow" if sentiment == "Positive" else ("tag-gray" if sentiment == "Neutral" else "tag-dark")
                            st.markdown(f"<div class='{tag_cls}' style='font-size: 16px; padding: 8px 18px; margin-top: 12px;'>Sentiment: {sentiment}</div>", unsafe_allow_html=True)
                            st.metric("Confidence Score", f"{confidence*100:.1f}%")
                            st.markdown(f"**Cleaned Text:** `{data['cleaned_text']}`")
                        else:
                            st.error(f"API Error: {res.text}")
                    except Exception as e:
                        st.error(f"Sentiment evaluation failed: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="crextio-card">', unsafe_allow_html=True)
        st.markdown("<h3 style='font-weight: 800; font-size: 18px; margin-bottom: 12px;'>Recent Reviews Feed</h3>", unsafe_allow_html=True)
        if stats and "recent_reviews" in stats and stats["recent_reviews"]:
            for rev in stats["recent_reviews"]:
                tag_cls = "tag-yellow" if rev["sentiment"] == "Positive" else ("tag-gray" if rev["sentiment"] == "Neutral" else "tag-dark")
                st.markdown(
                    f"""
                    <div style="background: #F6F5F0; padding: 14px; border-radius: 16px; margin-bottom: 12px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                            <span style="font-weight: 700; color: #18181B;">{rev['customer_name']}</span>
                            <span class="{tag_cls}">{rev['sentiment']} ({rev['confidence']*100:.0f}%)</span>
                        </div>
                        <div style="color: #3F3F46; font-style: italic; font-size: 13px;">"{rev['review_text']}"</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.info("No recent reviews logged.")
        st.markdown('</div>', unsafe_allow_html=True)


def render_chatbot():
    st.markdown("<h1 style='font-weight: 800; letter-spacing: -1px;'>🤖 Retail FAQ Chatbot</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #71717A; font-weight: 500; margin-bottom: 24px;'>Hybrid Rule-Based + TF-IDF Intent Matching Assistant</p>", unsafe_allow_html=True)

    st.markdown('<div class="crextio-card">', unsafe_allow_html=True)
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            ("bot", "Hello! Welcome to Crextio Smart Retail. How can I assist you today?")
        ]

    for sender, text in st.session_state.chat_history:
        if sender == "user":
            st.chat_message("user").write(text)
        else:
            st.chat_message("assistant").write(text)

    user_message = st.chat_input("Ask a question (e.g., 'What are your store operating hours?')...")

    if user_message:
        st.session_state.chat_history.append(("user", user_message))
        st.chat_message("user").write(user_message)

        try:
            res = requests.post(
                f"{API_BASE_URL}/chatbot",
                headers=HEADERS,
                json={"message": user_message},
                timeout=5,
            )

            if res.status_code == 200:
                data = res.json()
                bot_reply = data["response"]
                intent = data["intent"]
                conf = data["confidence"]

                reply_display = f"{bot_reply}\n\n*(Intent: `{intent}` | Confidence: `{conf*100:.1f}%`)*"
                st.session_state.chat_history.append(("bot", reply_display))
                st.chat_message("assistant").write(reply_display)
            else:
                st.error(f"Chatbot Service Error: {res.text}")
        except Exception as e:
            st.error(f"Chatbot failed to respond: {e}")
    st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
