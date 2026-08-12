import json
import streamlit as st
from ollama import Client

# Page settings
st.set_page_config(
    page_title="ScamShield",
    page_icon="🛡️",
    layout="centered"
)

# -----------------------------
# CUSTOM UI STYLES
# -----------------------------
st.markdown(
    """
    <style>
    :root {
        --page-yellow: #FFF8D6;
        --card-yellow: #FFFBEA;
        --header-sage: #EEF2D6;
        --panel-sage: #EEF3D7;
        --input-sage: #E3ECC8;
        --border-sage: #B8C89B;
        --forest: #2E5A24;
        --forest-dark: #24491D;
        --ink: #1F2B1D;
    }

    .stApp {
        background: linear-gradient(180deg, #FFF9DD 0%, var(--page-yellow) 100%);
        color: var(--ink);
    }

    .block-container {
        max-width: 880px;
        padding-top: 4.2rem;
        padding-bottom: 3rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    h1, h2, h3, p, label, .stMarkdown, span {
        color: var(--ink);
    }

    /* ONE OUTER CARD - matches reference image */
    .app-card {
        max-width: 820px;
        margin: 0 auto;
        background: rgba(255, 251, 234, 0.96);
        border: 1.5px solid var(--border-sage);
        border-radius: 24px;
        overflow: hidden;
        box-shadow: 0 8px 22px rgba(55, 77, 42, 0.06);
    }

    .app-card-header {
        background: linear-gradient(180deg, #F0F3D9 0%, #F4F5DE 100%);
        text-align: center;
        padding: 1.5rem 1.25rem 1.35rem;
        border-bottom: 1px solid rgba(184, 200, 155, 0.55);
    }

    .brand-row {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 0.55rem;
        line-height: 1;
    }

    .brand-icon {
        font-size: 2.45rem;
        line-height: 1;
    }

    .brand-title {
        font-size: clamp(2rem, 4.6vw, 3rem);
        line-height: 1;
        font-weight: 800;
        letter-spacing: -0.03em;
        color: var(--forest-dark);
    }

    .brand-subtitle {
        margin-top: 0.55rem;
        font-size: clamp(1.05rem, 2vw, 1.45rem);
        font-weight: 700;
        color: var(--ink);
    }

    .brand-copy {
        max-width: 610px;
        margin: 0.7rem auto 0;
        font-size: 0.98rem;
        line-height: 1.5;
    }

    .app-card-body {
        padding: 1rem 0.95rem 1.05rem;
        background: rgba(255, 251, 234, 0.98);
    }

    .form-panel {
        background: linear-gradient(180deg, #EFF3DA 0%, #EDF2D5 100%);
        border: 1.3px solid #D7E0BE;
        border-radius: 16px;
        padding: 0.95rem 1rem 1rem;
        box-shadow: inset 0 0 0 1px rgba(255,255,255,0.18);
    }

    .stSelectbox label,
    .stTextInput label,
    .stTextArea label {
        font-weight: 700 !important;
        color: var(--ink) !important;
        font-size: 0.98rem !important;
    }

    div[data-baseweb="select"] > div,
    .stTextInput input,
    .stTextArea textarea {
        background: var(--input-sage) !important;
        border: 1px solid #AFC08E !important;
        border-radius: 9px !important;
        color: var(--ink) !important;
        box-shadow: none !important;
    }

    div[data-baseweb="select"] > div {
        min-height: 48px;
    }

    .stTextInput input {
        min-height: 46px;
    }

    .stTextArea textarea {
        min-height: 170px !important;
    }

    div[data-baseweb="select"] > div:focus-within,
    .stTextInput input:focus,
    .stTextArea textarea:focus {
        border-color: var(--forest) !important;
        box-shadow: 0 0 0 2px rgba(46, 90, 36, 0.08) !important;
    }

    .stButton > button {
        min-height: 48px;
        border: none !important;
        border-radius: 8px !important;
        background: linear-gradient(90deg, var(--forest) 0%, var(--forest-dark) 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        box-shadow: 0 5px 12px rgba(36, 73, 29, 0.16);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 7px 15px rgba(36, 73, 29, 0.2);
    }

    [data-testid="stAlert"] {
        border-radius: 12px !important;
    }

    hr {
        border-color: rgba(184, 200, 155, 0.45) !important;
    }

    @media (max-width: 640px) {
        .block-container {
            padding-top: 2.2rem;
            padding-left: 0.65rem;
            padding-right: 0.65rem;
        }

        .app-card {
            border-radius: 18px;
        }

        .app-card-header {
            padding: 1.15rem 0.85rem 1rem;
        }

        .brand-icon {
            font-size: 2rem;
        }

        .brand-title {
            font-size: 2rem;
        }

        .brand-subtitle {
            font-size: 1.05rem;
        }

        .brand-copy {
            font-size: 0.9rem;
            line-height: 1.45;
        }

        .app-card-body {
            padding: 0.75rem;
        }

        .form-panel {
            border-radius: 14px;
            padding: 0.8rem;
        }

        .stButton > button {
            min-height: 50px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Connect to Ollama Cloud
try:
    ollama_api_key = st.secrets["OLLAMA_API_KEY"]
except Exception:
    st.error("OLLAMA_API_KEY was not found. Add it to your Streamlit secrets.")
    st.stop()

client = Client(
    host="https://ollama.com",
    headers={"Authorization": f"Bearer {ollama_api_key}"},
)

# Create session state
if "page" not in st.session_state:
    st.session_state.page = "scan"
if "result" not in st.session_state:
    st.session_state.result = None
if "error_message" not in st.session_state:
    st.session_state.error_message = None


def open_app_card(copy_text):
    st.markdown(
        f"""
        <div class="app-card">
            <div class="app-card-header">
                <div class="brand-row">
                    <div class="brand-icon">🛡️</div>
                    <div class="brand-title">ScamShield</div>
                </div>
                <div class="brand-subtitle">AI Scam Message Detector</div>
                <div class="brand-copy">{copy_text}</div>
            </div>
            <div class="app-card-body">
                <div class="form-panel">
        """,
        unsafe_allow_html=True,
    )


def close_form_panel():
    st.markdown("</div></div></div>", unsafe_allow_html=True)


# Page 1 - Scan page
def scan_page():
    open_app_card(
        "Enter an email or text message below. ScamShield will analyze it for possible scam warning signs."
    )

    message_type = st.selectbox(
        "Message Type",
        ["Select Message Type", "Email", "Text Message"],
    )

    message_to_analyze = ""

    if message_type == "Email":
        sender = st.text_input("From Email Address", placeholder="example@email.com")
        subject = st.text_input("Subject", placeholder="Enter email subject")
        body = st.text_area("Email Body", placeholder="Paste the email here...", height=200)
        attachment = st.selectbox("Does the email have an attachment?", ["No", "Yes"])

        message_to_analyze = f"""
Message Type: Email
Sender: {sender}
Subject: {subject}
Body: {body}
Attachment: {attachment}
"""

    elif message_type == "Text Message":
        phone_number = st.text_input("Phone Number", placeholder="555-123-4567")
        message = st.text_area("Text Message", placeholder="Paste the text message here...", height=200)

        message_to_analyze = f"""
Message Type: Text Message
Phone Number: {phone_number}
Message: {message}
"""

    st.markdown("<div style='height:0.35rem'></div>", unsafe_allow_html=True)
    left, center, right = st.columns([1.15, 1.65, 1.15])
    with center:
        analyze_clicked = st.button("🔍 Analyze Message", use_container_width=True)

    close_form_panel()

    if analyze_clicked:
        if message_type == "Select Message Type":
            st.warning("Please select Email or Text Message.")
            return

        if message_to_analyze.strip() == "":
            st.warning("Please enter a message.")
            return

        prompt = f"""
You are ScamShield, an AI scam message detector.

Analyze the message below.

Return ONLY valid JSON using exactly this format:

{{
    "risk_level": "LOW",
    "warning_signs": [
        "Warning sign 1",
        "Warning sign 2"
    ],
    "recommendation": "Explain what the user should do."
}}

Risk level must be one of:
LOW
MEDIUM
HIGH

LOW means the message appears mostly safe.
MEDIUM means the message contains suspicious warning signs.
HIGH means the message appears likely to be a scam.

For warning_signs, list specific suspicious things such as:
- Urgent language
- Threats
- Suspicious links
- Requests for money
- Requests for passwords
- Requests for personal information
- Suspicious sender address
- Unexpected attachments
- Offers that seem too good to be true

If there are no major warning signs, return:
[
    "No major scam warning signs detected."
]

The recommendation should be short and easy to understand.
Do not include markdown.
Do not include code blocks.
Do not include anything outside the JSON.

Message to analyze:
{message_to_analyze}
"""

        try:
            with st.spinner("ScamShield is analyzing the message..."):
                response = client.chat(
                    model="gemma4:cloud",
                    messages=[{"role": "user", "content": prompt}],
                    format="json",
                    options={"temperature": 0},
                )

            ai_response = response["message"]["content"]
            result = json.loads(ai_response)
            st.session_state.result = result
            st.session_state.page = "result"
            st.rerun()

        except Exception as e:
            st.session_state.error_message = str(e)
            st.session_state.page = "error"
            st.rerun()


# Page 2 - Result page
def result_page():
    open_app_card("Your scan is complete. Review the results below.")

    result = st.session_state.get("result")
    if result is None:
        st.error("No analysis result was found.")
        if st.button("🔄 Back to Scanner", use_container_width=True):
            st.session_state.page = "scan"
            st.rerun()
        close_form_panel()
        return

    if isinstance(result, str):
        try:
            result = json.loads(result)
        except json.JSONDecodeError:
            st.error("The AI returned an invalid result.")
            close_form_panel()
            return

    risk_level = str(result.get("risk_level", "UNKNOWN")).upper()
    warning_signs = result.get("warning_signs", [])
    recommendation = result.get("recommendation", "No recommendation available.")

    st.subheader("🚦 Risk Level")
    if risk_level == "LOW":
        st.success("🟢 LOW RISK")
    elif risk_level == "MEDIUM":
        st.warning("🟡 MEDIUM RISK")
    elif risk_level == "HIGH":
        st.error("🔴 HIGH RISK")
    else:
        st.info(risk_level)

    st.divider()
    st.subheader("⚠️ Warning Signs")
    if isinstance(warning_signs, list):
        for sign in warning_signs:
            st.write(f"• {sign}")
    else:
        st.write(f"• {warning_signs}")

    st.divider()
    st.subheader("🛡️ Recommendation")
    st.info(recommendation)

    st.divider()
    left, center, right = st.columns([1.1, 1.7, 1.1])
    with center:
        if st.button("🔍 Scan Another Message", use_container_width=True):
            st.session_state.result = None
            st.session_state.error_message = None
            st.session_state.page = "scan"
            st.rerun()

    close_form_panel()


# Page 3 - Error page
def error_page():
    open_app_card("ScamShield had a problem communicating with the Ollama AI service.")

    st.error("⚠️ Something Went Wrong")
    st.write("Possible reasons:")
    st.write("• The Ollama API key may be missing or incorrect.")
    st.write("• The selected model may not be available.")
    st.write("• There may be an internet or API connection problem.")
    st.write("• Ollama may have returned an invalid response.")
    st.write("• The AI response may not contain valid JSON.")

    error_message = st.session_state.get("error_message")
    if error_message:
        with st.expander("🔧 Technical Details"):
            st.code(error_message)

    left, center, right = st.columns([1.1, 1.7, 1.1])
    with center:
        if st.button("🔄 Try Again", use_container_width=True):
            st.session_state.error_message = None
            st.session_state.result = None
            st.session_state.page = "scan"
            st.rerun()

    close_form_panel()


# Show correct page
if st.session_state.page == "scan":
    scan_page()
elif st.session_state.page == "result":
    result_page()
elif st.session_state.page == "error":
    error_page()
else:
    st.session_state.page = "scan"
    st.rerun()