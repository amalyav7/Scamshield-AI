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
        --baby-yellow: #F8F1C5;
        --baby-yellow-2: #FBF7DA;
        --sage: #E4EBCF;
        --sage-soft: #EEF2DE;
        --sage-input: #DEE8BE;
        --border: rgba(117, 143, 92, 0.38);
        --forest: #315B2A;
        --forest-dark: #23451F;
        --ink: #1E2A1B;
    }

    .stApp {
        background: linear-gradient(180deg, var(--baby-yellow-2) 0%, var(--baby-yellow) 100%);
        color: var(--ink);
    }

    .block-container {
        max-width: 920px;
        padding-top: 2rem;
        padding-bottom: 3rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    h1, h2, h3, p, label, .stMarkdown, span {
        color: var(--ink);
    }

    .scamshield-hero {
        max-width: 820px;
        margin: 0 auto 1.2rem;
        border-radius: 30px;
        border: 1px solid var(--border);
        background: linear-gradient(180deg, rgba(228, 235, 207, 0.95) 0%, rgba(240, 244, 222, 0.93) 100%);
        box-shadow: 0 12px 28px rgba(56, 83, 45, 0.08);
        padding: 1.45rem 1.3rem 1.25rem;
        text-align: center;
    }

    .brand-row {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.8rem;
        flex-wrap: wrap;
        line-height: 1;
    }

    .brand-icon {
        font-size: 3rem;
        line-height: 1;
        filter: saturate(0.8);
    }

    .brand-title {
        font-size: clamp(2.2rem, 5vw, 3.4rem);
        font-weight: 800;
        letter-spacing: -0.03em;
        color: var(--forest-dark);
    }

    .brand-subtitle {
        margin-top: 0.35rem;
        font-size: clamp(1.2rem, 2.4vw, 1.9rem);
        font-weight: 700;
        color: var(--ink);
    }

    .brand-copy {
        margin: 0.7rem auto 0;
        max-width: 630px;
        line-height: 1.55;
        font-size: 1rem;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(231, 236, 207, 0.76) !important;
        border: 1px solid var(--border) !important;
        border-radius: 28px !important;
        box-shadow: 0 10px 24px rgba(56, 83, 45, 0.06);
    }

    [data-testid="stVerticalBlockBorderWrapper"] > div {
        padding: 0.45rem 0.55rem 0.7rem;
    }

    [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(243, 246, 230, 0.94) !important;
        border-radius: 24px !important;
        box-shadow: none !important;
    }

    [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stVerticalBlockBorderWrapper"] > div {
        padding: 0.7rem 0.75rem 0.85rem;
    }

    .panel-copy {
        text-align: center;
        max-width: 560px;
        margin: 0.15rem auto 0.8rem;
        line-height: 1.55;
    }

    .field-caption {
        font-size: 1.02rem;
        font-weight: 700;
        margin: 0.1rem 0 0.35rem 0.1rem;
        color: var(--ink);
    }

    .stSelectbox label,
    .stTextInput label,
    .stTextArea label {
        font-weight: 700 !important;
        color: var(--ink) !important;
    }

    div[data-baseweb="select"] > div,
    .stTextInput input,
    .stTextArea textarea {
        background: var(--sage-input) !important;
        border: 1px solid rgba(115, 142, 90, 0.45) !important;
        border-radius: 12px !important;
        color: var(--ink) !important;
        box-shadow: none !important;
    }

    div[data-baseweb="select"] > div {
        min-height: 50px;
    }

    .stTextInput input {
        min-height: 48px;
    }

    .stTextArea textarea {
        min-height: 170px !important;
    }

    div[data-baseweb="select"] > div:focus-within,
    .stTextInput input:focus,
    .stTextArea textarea:focus {
        border-color: var(--forest) !important;
        box-shadow: 0 0 0 2px rgba(49, 91, 42, 0.10) !important;
    }

    .stButton > button {
        min-height: 54px;
        border-radius: 14px !important;
        border: none !important;
        background: linear-gradient(90deg, var(--forest) 0%, var(--forest-dark) 100%) !important;
        color: white !important;
        font-weight: 800 !important;
        font-size: 1.08rem !important;
        box-shadow: 0 8px 18px rgba(35, 69, 31, 0.18);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 10px 22px rgba(35, 69, 31, 0.24);
    }

    hr {
        border-color: rgba(117, 143, 92, 0.25) !important;
    }

    [data-testid="stAlert"] {
        border-radius: 16px !important;
    }

    .result-card {
        background: rgba(243, 246, 230, 0.92);
        border: 1px solid var(--border);
        border-radius: 24px;
        padding: 1rem 1rem 0.2rem;
        margin-top: 0.6rem;
    }

    @media (max-width: 640px) {
        .block-container {
            padding-top: 1.2rem;
            padding-left: 0.85rem;
            padding-right: 0.85rem;
        }

        .scamshield-hero {
            border-radius: 22px;
            padding: 1.1rem 0.95rem 1rem;
        }

        .brand-row {
            gap: 0.5rem;
        }

        .brand-icon {
            font-size: 2.3rem;
        }

        [data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: 22px !important;
        }

        [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: 18px !important;
        }

        .stButton > button {
            min-height: 52px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def page_hero(
    subtitle="AI Scam Message Detector",
    copy="Enter an email or text message below. ScamShield will analyze it for possible scam warning signs.",
):
    st.markdown(
        f"""
        <div class="scamshield-hero">
            <div class="brand-row">
                <div class="brand-icon">🛡️</div>
                <div class="brand-title">ScamShield</div>
            </div>
            <div class="brand-subtitle">{subtitle}</div>
            <div class="brand-copy">{copy}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# Connect to Ollama Cloud
try:
    ollama_api_key = st.secrets["OLLAMA_API_KEY"]
except Exception:
    st.error(
        "OLLAMA_API_KEY was not found. "
        "Add it to your Streamlit secrets."
    )
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


# Page 1 - Scan page
def scan_page():
    page_hero()

    message_to_analyze = ""

    with st.container(border=True):
        st.markdown(
            '<div class="panel-copy">Clean, easy to read, and responsive on both mobile and desktop.</div>',
            unsafe_allow_html=True,
        )

        with st.container(border=True):
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
        left, center, right = st.columns([1.05, 1.6, 1.05])
        with center:
            analyze_clicked = st.button("🔍 Analyze Message", use_container_width=True)

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
    page_hero(copy="Your scan is complete. Review the risk level, warning signs, and recommendation below.")

    result = st.session_state.get("result")
    if result is None:
        st.error("No analysis result was found.")
        if st.button("🔄 Back to Scanner"):
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
    recommendation = result.get("recommendation", "No recommendation available.")

    with st.container(border=True):
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
        left, center, right = st.columns([1.05, 1.6, 1.05])
        with center:
            if st.button("🔍 Scan Another Message", use_container_width=True):
                st.session_state.result = None
                st.session_state.error_message = None
                st.session_state.page = "scan"
                st.rerun()


# Page 3 - Error page
def error_page():
    page_hero(copy="ScamShield had a problem communicating with the Ollama AI service.")

    with st.container(border=True):
        st.error("⚠️ Something Went Wrong")
        st.subheader("We couldn't analyze your message.")
        st.write("Possible reasons:")
        st.write("• The Ollama API key may be missing or incorrect.")
        st.write("• The selected model may not be available.")
        st.write("• There may be an internet or API connection problem.")
        st.write("• Ollama may have returned an invalid response.")
        st.write("• The AI response may not contain valid JSON.")
        st.info("Check your Ollama API key and model settings, then try again.")

        error_message = st.session_state.get("error_message")
        if error_message:
            with st.expander("🔧 Technical Details"):
                st.code(error_message)

        left, center, right = st.columns([1.05, 1.6, 1.05])
        with center:
            if st.button("🔄 Try Again", use_container_width=True):
                st.session_state.error_message = None
                st.session_state.result = None
                st.session_state.page = "scan"
                st.rerun()


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