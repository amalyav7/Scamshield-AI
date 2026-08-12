import json
import streamlit as st
from ollama import Client

# Page settings
st.set_page_config(
    page_title="ScamShield",
    page_icon="🛡️",
    layout="wide"
)

# -----------------------------
# CUSTOM UI STYLES
# -----------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Infant:ital,wght@0,400;0,500;0,600;0,700&display=swap');

    :root {
        /* Base colors from your reference images */
        --butter-yellow: #FDEC80;
        --olive-green: #566B30;

        /* Coordinating shades */
        --page-yellow: #FDF0A0;
        --outer-card: #FFF8D2;
        --header-sage: #E8EDCD;
        --panel-sage: #D7E2B9;
        --input-sage: #EEF2DB;
        --button-sage: #C6D79C;
        --button-sage-hover: #B8CC89;
        --border-sage: #91A566;
        --forest: #566B30;
        --forest-dark: #3F5122;
        --ink: #26331A;
    }

    html, body, .stApp,
    .stApp button, .stApp input, .stApp textarea,
    .stApp [data-baseweb="select"], .stApp label,
    .stApp p, .stApp span, .stApp div {
        font-family: "Cormorant Infant", Georgia, serif !important;
    }

    .stApp {
        background: linear-gradient(180deg, #FFF5B5 0%, var(--butter-yellow) 100%);
        color: var(--ink);
    }

    /* Space above the whole design so it does NOT touch the top */
    .block-container {
        max-width: 1180px;
        padding-top: 4rem;
        padding-bottom: 3.5rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    h1, h2, h3, p, label, .stMarkdown, span {
        color: var(--ink);
    }

    /* OUTER CARD - target by Streamlit key so styling is reliable */
    .st-key-main_card {
        background: var(--outer-card) !important;
        border: 2px solid rgba(86, 107, 48, 0.40) !important;
        border-radius: 30px !important;
        box-shadow: 0 12px 30px rgba(55, 77, 42, 0.08) !important;
        overflow: hidden !important;
    }

    .st-key-main_card > div {
        padding: 0 !important;
    }

    /* HEADER AREA INSIDE OUTER CARD */
    .scam-header {
        background: linear-gradient(180deg, #E5EBC8 0%, #F2F3D8 100%);
        text-align: center;
        padding: 2.4rem 2rem 2rem;
        margin: 0;
    }

    .brand-row {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 0.9rem;
    }

    .brand-icon {
        font-size: 3.2rem;
        line-height: 1;
    }

    .brand-title {
        font-size: clamp(2.8rem, 5vw, 4rem);
        font-weight: 800;
        line-height: 1;
        letter-spacing: -0.025em;
        color: var(--forest-dark);
    }

    .brand-subtitle {
        margin-top: 0.8rem;
        font-size: clamp(1.35rem, 2.4vw, 1.9rem);
        font-weight: 700;
    }

    .brand-copy {
        margin: 1rem auto 0;
        max-width: 760px;
        font-size: 1.12rem;
        line-height: 1.6;
    }

    .header-divider {
        height: 1px;
        background: rgba(86, 107, 48, 0.26);
        margin: 0;
    }

    /* Body space under header */
    .form-spacer {
        height: 1.4rem;
    }

    /* GREEN BOX AROUND MESSAGE TYPE + ANALYZE BUTTON */
    .st-key-input_panel {
        width: calc(100% - 4rem) !important;
        max-width: calc(100% - 4rem) !important;
        margin: 0 auto 2rem auto !important;
        box-sizing: border-box !important;
        background: var(--panel-sage) !important;
        border: 2px solid var(--border-sage) !important;
        border-radius: 24px !important;
        box-shadow: inset 0 0 0 1px rgba(255,255,255,0.28) !important;
        overflow: visible !important;
    }

    .st-key-input_panel > div {
        width: 100% !important;
        box-sizing: border-box !important;
        padding: 2.5rem 2.6rem 2.6rem !important;
    }

    .stSelectbox label,
    .stTextInput label,
    .stTextArea label {
        font-weight: 650 !important;
        color: var(--ink) !important;
        font-size: 1.1rem !important;
    }

    div[data-baseweb="select"] > div,
    .stTextInput input,
    .stTextArea textarea {
        background: var(--input-sage) !important;
        border: 1px solid var(--border-sage) !important;
        border-radius: 9px !important;
        color: var(--ink) !important;
        box-shadow: none !important;
    }

    div[data-baseweb="select"] > div {
        min-height: 58px;
    }

    .stTextInput input {
        min-height: 56px;
    }

    .stTextArea textarea {
        min-height: 220px !important;
    }

    div[data-baseweb="select"] > div:focus-within,
    .stTextInput input:focus,
    .stTextArea textarea:focus {
        border-color: var(--forest) !important;
        box-shadow: 0 0 0 2px rgba(46, 90, 36, 0.08) !important;
    }

    .stButton > button {
        min-height: 56px;
        border-radius: 12px !important;
        font-weight: 800 !important;
        font-size: 1.2rem !important;
        letter-spacing: 0.01em !important;
    }

    /* Analyze button: LIGHT GREEN, as requested */
    .st-key-analyze_button button {
        min-height: 54px !important;
        background: var(--button-sage) !important;
        border: 2px solid var(--border-sage) !important;
        color: var(--forest-dark) !important;
        font-size: 1.7rem !important;
        font-weight: 700 !important;
        box-shadow: 0 6px 14px rgba(86, 107, 48, 0.14) !important;
    }

    .st-key-analyze_button button:hover {
        background: var(--button-sage-hover) !important;
        color: #2F3E1B !important;
        border-color: var(--forest) !important;
    }

    .stButton > button {
        background: linear-gradient(90deg, var(--forest) 0%, var(--forest-dark) 100%) !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 5px 12px rgba(36, 73, 29, 0.16);
    }

    .st-key-analyze_button button {
        min-height: 54px !important;
        background: var(--button-sage) !important;
        border: 2px solid var(--border-sage) !important;
        color: var(--forest-dark) !important;
        font-size: 1.7rem !important;
        font-weight: 700 !important;
        box-shadow: 0 6px 14px rgba(86, 107, 48, 0.14) !important;
    }

    [data-testid="stAlert"] {
        border-radius: 12px !important;
    }

    @media (max-width: 640px) {
        .block-container {
            padding-top: 2rem;
            padding-left: 0.7rem;
            padding-right: 0.7rem;
        }

        .st-key-main_card {
            border-radius: 18px !important;
        }

        .scam-header {
            padding: 1.5rem 1rem 1.25rem;
        }

        .brand-icon {
            font-size: 2.3rem;
        }

        .brand-title {
            font-size: 2.25rem;
        }

        .brand-copy {
            font-size: 0.9rem;
        }

        .st-key-input_panel {
            width: calc(100% - 1.4rem) !important;
            max-width: calc(100% - 1.4rem) !important;
            margin: 0 auto 0.9rem auto !important;
            border-radius: 18px !important;
        }

        .st-key-input_panel > div {
            padding: 1.4rem !important;
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

if "page" not in st.session_state:
    st.session_state.page = "scan"
if "result" not in st.session_state:
    st.session_state.result = None
if "error_message" not in st.session_state:
    st.session_state.error_message = None


def render_header(copy_text):
    st.markdown(
        f"""
        <div class="scam-header">
            <div class="brand-row">
                <div class="brand-icon">🛡️</div>
                <div class="brand-title">ScamShield</div>
            </div>
            <div class="brand-subtitle">AI Scam Message Detector</div>
            <div class="brand-copy">{copy_text}</div>
        </div>
        <div class="header-divider"></div>
        <div class="form-spacer"></div>
        """,
        unsafe_allow_html=True,
    )


# Page 1 - Scan page
def scan_page():
    message_to_analyze = ""

    # REAL Streamlit outer container
    with st.container(border=True, key="main_card"):
        render_header(
            "Enter an email or text message below. ScamShield will analyze it for possible scam warning signs."
        )

        # REAL nested Streamlit container: this is the green box around ALL inputs
        with st.container(border=True, key="input_panel"):
            message_type = st.selectbox(
                "Message Type",
                ["Select Message Type", "Email", "Text Message"],
            )

            if message_type == "Email":
                sender = st.text_input(
                    "From Email Address", placeholder="example@email.com"
                )
                subject = st.text_input("Subject", placeholder="Enter email subject")
                body = st.text_area(
                    "Email Body", placeholder="Paste the email here...", height=200
                )
                attachment = st.selectbox(
                    "Does the email have an attachment?", ["No", "Yes"]
                )

                message_to_analyze = f"""
Message Type: Email
Sender: {sender}
Subject: {subject}
Body: {body}
Attachment: {attachment}
"""

            elif message_type == "Text Message":
                phone_number = st.text_input(
                    "Phone Number", placeholder="555-123-4567"
                )
                message = st.text_area(
                    "Text Message", placeholder="Paste the text message here...", height=200
                )

                message_to_analyze = f"""
Message Type: Text Message
Phone Number: {phone_number}
Message: {message}
"""

            st.markdown("<div style='height:0.35rem'></div>", unsafe_allow_html=True)
            left, center, right = st.columns([1.15, 1.5, 1.15])
            with center:
                analyze_clicked = st.button(
                    "Analyze Message", use_container_width=True, key="analyze_button"
                )

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
    with st.container(border=True):
        render_header("Your scan is complete. Review the results below.")

        with st.container(border=True):
            result = st.session_state.get("result")

            if result is None:
                st.error("No analysis result was found.")
                if st.button("🔄 Back to Scanner", use_container_width=True):
                    st.session_state.page = "scan"
                    st.rerun()
                return

            if isinstance(result, str):
                try:
                    result = json.loads(result)
                except json.JSONDecodeError:
                    st.error("The AI returned an invalid result.")
                    return

            risk_level = str(result.get("risk_level", "UNKNOWN")).upper()
            warning_signs = result.get("warning_signs", [])
            recommendation = result.get(
                "recommendation", "No recommendation available."
            )

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
            left, center, right = st.columns([0.8, 2.2, 0.8])
            with center:
                if st.button("🔍 Scan Another Message", use_container_width=True):
                    st.session_state.result = None
                    st.session_state.error_message = None
                    st.session_state.page = "scan"
                    st.rerun()


# Page 3 - Error page
def error_page():
    with st.container(border=True):
        render_header(
            "ScamShield had a problem communicating with the Ollama AI service."
        )

        with st.container(border=True):
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

            left, center, right = st.columns([0.8, 2.2, 0.8])
            with center:
                if st.button("🔄 Try Again", use_container_width=True):
                    st.session_state.error_message = None
                    st.session_state.result = None
                    st.session_state.page = "scan"
                    st.rerun()


if st.session_state.page == "scan":
    scan_page()
elif st.session_state.page == "result":
    result_page()
elif st.session_state.page == "error":
    error_page()
else:
    st.session_state.page = "scan"
    st.rerun()