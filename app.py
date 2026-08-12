import json
import streamlit as st
from ollama import Client

st.set_page_config(
    page_title="ScamShield",
    page_icon="🛡️",
    layout="wide"
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Infant:wght@400;500;600;700&display=swap');

    :root {
        --page-yellow: #FDFAE8;
        --page-yellow-soft: #FDFAE8;
        --outer-card: #F7EFAF;
        --section-fill: #E6E9CC;
        --section-fill-2: #E9ECD3;
        --input-fill: #E7EBCF;
        --olive: #566B30;
        --olive-dark: #405123;
        --border: #AAB689;
        --text: #223015;
    }

    html, body, .stApp,
    .stApp button, .stApp input, .stApp textarea,
    .stApp [data-baseweb="select"], .stApp label,
    .stApp p, .stApp span, .stApp div {
        font-family: "Cormorant Infant", Georgia, serif !important;
    }

    .stApp {
        background: linear-gradient(180deg, var(--page-yellow-soft) 0%, var(--page-yellow) 100%);
        color: var(--text);
    }

    .block-container {
        max-width: 1220px;
        padding-top: 3.5rem;
        padding-bottom: 2.8rem;
        padding-left: 1.2rem;
        padding-right: 1.2rem;
    }

    .st-key-main_card {
        background: var(--outer-card) !important;
        border: 1.5px solid rgba(86,107,48,0.32) !important;
        border-radius: 22px !important;
        overflow: hidden !important;
        box-shadow: 0 6px 18px rgba(64,81,35,0.06) !important;
    }

    .st-key-main_card > div {
        padding: 0 !important;
    }

    .header-section {
        background: linear-gradient(180deg, var(--section-fill) 0%, var(--section-fill-2) 100%);
        text-align: center;
        padding: 1.55rem 1rem 1.3rem;
        margin: 0;
    }

    .brand-row {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 0.75rem;
        line-height: 1;
    }

    .brand-icon {
        font-size: 2.7rem;
        color: var(--olive-dark);
    }

    .brand-title {
        font-size: clamp(2.45rem, 4vw, 3.55rem);
        font-weight: 700;
        letter-spacing: -0.02em;
        color: var(--olive-dark);
    }

    .brand-subtitle {
        font-size: clamp(1.25rem, 2vw, 1.8rem);
        font-weight: 700;
        margin-top: 0.55rem;
        color: var(--text);
    }

    .brand-copy {
        max-width: 670px;
        margin: 0.8rem auto 0;
        font-size: 1rem;
        line-height: 1.45;
        font-weight: 600;
        color: #2c3a1d;
    }

    .divider-line {
        height: 1px;
        background: rgba(86,107,48,0.22);
        margin: 0;
    }

    .body-space {
        height: 0.9rem;
        background: transparent;
    }

    .st-key-input_panel {
        width: calc(100% - 1.6rem) !important;
        max-width: calc(100% - 1.6rem) !important;
        margin: 0 auto 0.9rem auto !important;
        background: linear-gradient(180deg, var(--section-fill-2) 0%, #E5E8CB 100%) !important;
        border: 1.5px solid rgba(170,182,137,0.95) !important;
        border-radius: 18px !important;
        box-shadow: inset 0 0 0 1px rgba(255,255,255,0.18) !important;
        overflow: hidden !important;
    }

    .st-key-input_panel > div {
        padding: 0.95rem 1rem 1.1rem !important;
    }

    .stSelectbox label,
    .stTextInput label,
    .stTextArea label {
        font-size: 1.03rem !important;
        font-weight: 700 !important;
        color: var(--text) !important;
    }

    div[data-baseweb="select"] > div,
    .stTextInput input,
    .stTextArea textarea {
        background: linear-gradient(180deg, var(--input-fill) 0%, #E2E7C5 100%) !important;
        border: 1.4px solid var(--border) !important;
        border-radius: 8px !important;
        color: var(--text) !important;
        box-shadow: none !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
    }

    div[data-baseweb="select"] > div {
        min-height: 48px;
    }

    .stTextInput input {
        min-height: 48px;
    }

    .stTextArea textarea {
        min-height: 185px !important;
    }

    div[data-baseweb="select"] > div:focus-within,
    .stTextInput input:focus,
    .stTextArea textarea:focus {
        border-color: var(--olive) !important;
        box-shadow: 0 0 0 2px rgba(86,107,48,0.08) !important;
    }

    .stButton > button {
        border-radius: 10px !important;
        font-weight: 700 !important;
        letter-spacing: 0 !important;
    }

    .st-key-analyze_button button {
        min-height: 42px !important;
        width: 290px !important;
        max-width: 100% !important;
        background: linear-gradient(90deg, #43601F 0%, #2B5317 100%) !important;
        color: #F2F1E8 !important;
        border: 1px solid rgba(63,81,35,0.50) !important;
        box-shadow: 0 5px 12px rgba(58,79,31,0.16) !important;
        font-size: 1.36rem !important;
        font-weight: 700 !important;
    }

    .st-key-analyze_button button:hover {
        background: linear-gradient(90deg, #4C6925 0%, #315C1A 100%) !important;
        color: #FAFAF3 !important;
    }

    .st-key-main_card .stButton:not(.st-key-analyze_button) > button {
        background: linear-gradient(90deg, var(--olive) 0%, var(--olive-dark) 100%) !important;
        color: white !important;
        border: none !important;
    }

    [data-testid="stAlert"] {
        border-radius: 12px !important;
    }

    @media (max-width: 640px) {
        .block-container {
            padding-top: 1.3rem;
            padding-left: 0.55rem;
            padding-right: 0.55rem;
        }

        .st-key-main_card {
            border-radius: 16px !important;
        }

        .header-section {
            padding: 1.15rem 0.9rem 1rem;
        }

        .brand-icon {
            font-size: 2.1rem;
        }

        .brand-title {
            font-size: 2rem;
        }

        .brand-subtitle {
            font-size: 1.1rem;
        }

        .brand-copy {
            font-size: 0.9rem;
            margin-top: 0.6rem;
        }

        .st-key-input_panel {
            width: calc(100% - 0.9rem) !important;
            max-width: calc(100% - 0.9rem) !important;
            border-radius: 14px !important;
            margin: 0 auto 0.7rem auto !important;
        }

        .st-key-input_panel > div {
            padding: 0.85rem 0.8rem 0.95rem !important;
        }

        .st-key-analyze_button button {
            width: 100% !important;
            min-height: 44px !important;
            font-size: 1.22rem !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

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


def render_header(copy_text: str):
    st.markdown(
        f"""
        <div class="header-section">
            <div class="brand-row">
                <div class="brand-icon">🛡️</div>
                <div class="brand-title">ScamShield</div>
            </div>
            <div class="brand-subtitle">AI Scam Message Detector</div>
            <div class="brand-copy">{copy_text}</div>
        </div>
        <div class="divider-line"></div>
        <div class="body-space"></div>
        """,
        unsafe_allow_html=True,
    )


def scan_page():
    message_to_analyze = ""
    analyze_clicked = False
    message_type = "Select Message Type"

    with st.container(border=True, key="main_card"):
        render_header(
            "Enter an email or text message below. ScamShield will analyze it for possible scam warning signs."
        )

        with st.container(border=True, key="input_panel"):
            message_type = st.selectbox(
                "Message Type",
                ["Select Message Type", "Email", "Text Message"],
            )

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

            st.markdown("<div style='height:0.25rem'></div>", unsafe_allow_html=True)
            left, center, right = st.columns([1.3, 1.0, 1.3])
            with center:
                analyze_clicked = st.button("Analyze Message", use_container_width=True, key="analyze_button")

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


def result_page():
    with st.container(border=True, key="main_card"):
        render_header("Your scan is complete. Review the results below.")
        with st.container(border=True, key="input_panel"):
            result = st.session_state.get("result")
            if result is None:
                st.error("No analysis result was found.")
                return
            if isinstance(result, str):
                try:
                    result = json.loads(result)
                except json.JSONDecodeError:
                    st.error("The AI returned an invalid result.")
                    return
            risk_level = str(result.get("risk_level", "UNKNOWN")).upper()
            warning_signs = result.get("warning_signs", [])
            recommendation = result.get("recommendation", "No recommendation available.")

            st.subheader("Risk Level")
            if risk_level == "LOW":
                st.success("LOW RISK")
            elif risk_level == "MEDIUM":
                st.warning("MEDIUM RISK")
            elif risk_level == "HIGH":
                st.error("HIGH RISK")
            else:
                st.info(risk_level)

            st.divider()
            st.subheader("Warning Signs")
            if isinstance(warning_signs, list):
                for sign in warning_signs:
                    st.write(f"• {sign}")
            else:
                st.write(f"• {warning_signs}")

            st.divider()
            st.subheader("Recommendation")
            st.info(recommendation)

            st.divider()
            l, c, r = st.columns([1.3, 1.0, 1.3])
            with c:
                if st.button("Scan Another Message", use_container_width=True):
                    st.session_state.result = None
                    st.session_state.error_message = None
                    st.session_state.page = "scan"
                    st.rerun()


def error_page():
    with st.container(border=True, key="main_card"):
        render_header("ScamShield had a problem communicating with the Ollama AI service.")
        with st.container(border=True, key="input_panel"):
            st.error("Something Went Wrong")
            st.write("Possible reasons:")
            st.write("• The Ollama API key may be missing or incorrect.")
            st.write("• The selected model may not be available.")
            st.write("• There may be an internet or API connection problem.")
            st.write("• Ollama may have returned an invalid response.")
            st.write("• The AI response may not contain valid JSON.")
            error_message = st.session_state.get("error_message")
            if error_message:
                with st.expander("Technical Details"):
                    st.code(error_message)
            l, c, r = st.columns([1.3, 1.0, 1.3])
            with c:
                if st.button("Try Again", use_container_width=True):
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