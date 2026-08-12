import streamlit as st
import json
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
        --baby-yellow: #FFF7C7;
        --sage: #DDE8C5;
        --sage-deep: #B8C99A;
        --forest: #315B2A;
        --forest-dark: #23451F;
        --ink: #1F2F1E;
        --soft-border: rgba(49, 91, 42, 0.18);
    }

    .stApp {
        background: linear-gradient(180deg, #FFF9D8 0%, var(--baby-yellow) 100%);
        color: var(--ink);
    }

    .block-container {
        max-width: 860px;
        padding-top: 1.25rem;
        padding-bottom: 2.5rem;
    }

    h1, h2, h3, p, label, .stMarkdown {
        color: var(--ink);
    }

    h1 {
        font-size: clamp(2rem, 5vw, 3.25rem) !important;
        font-weight: 800 !important;
        letter-spacing: -0.03em;
        margin-bottom: 0.1rem !important;
    }

    h2, h3 {
        font-weight: 700 !important;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 24px !important;
        border: 1px solid var(--soft-border) !important;
        background: rgba(221, 232, 197, 0.82) !important;
        box-shadow: 0 10px 28px rgba(49, 91, 42, 0.08);
    }

    div[data-baseweb="select"] > div,
    .stTextInput input,
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.74) !important;
        border: 1px solid rgba(49, 91, 42, 0.24) !important;
        border-radius: 14px !important;
        color: var(--ink) !important;
        min-height: 48px;
        box-shadow: none !important;
    }

    .stTextArea textarea {
        min-height: 180px !important;
    }

    div[data-baseweb="select"] > div:focus-within,
    .stTextInput input:focus,
    .stTextArea textarea:focus {
        border-color: var(--forest) !important;
        box-shadow: 0 0 0 2px rgba(49, 91, 42, 0.10) !important;
    }

    .stButton > button {
        width: 100%;
        min-height: 50px;
        border: none !important;
        border-radius: 14px !important;
        background: linear-gradient(180deg, var(--forest) 0%, var(--forest-dark) 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        box-shadow: 0 8px 18px rgba(35, 69, 31, 0.18);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 10px 22px rgba(35, 69, 31, 0.24);
    }

    hr {
        border-color: rgba(49, 91, 42, 0.14) !important;
    }

    [data-testid="stAlert"] {
        border-radius: 16px !important;
    }

    .scamshield-hero {
        background: rgba(221, 232, 197, 0.88);
        border: 1px solid var(--soft-border);
        border-radius: 26px;
        padding: 1.4rem 1.4rem 1.2rem;
        text-align: center;
        box-shadow: 0 12px 30px rgba(49, 91, 42, 0.09);
        margin-bottom: 1rem;
    }

    .scamshield-hero .shield {
        font-size: 2.1rem;
        margin-bottom: 0.2rem;
    }

    .scamshield-hero .title {
        font-size: clamp(2rem, 5vw, 3rem);
        font-weight: 800;
        color: var(--forest-dark);
        line-height: 1.05;
    }

    .scamshield-hero .subtitle {
        margin-top: 0.35rem;
        font-size: clamp(1rem, 2.4vw, 1.2rem);
        font-weight: 700;
    }

    .scamshield-hero .copy {
        margin: 0.55rem auto 0;
        max-width: 620px;
        font-size: 0.96rem;
        line-height: 1.55;
    }

    .section-card {
        background: rgba(221, 232, 197, 0.86);
        border: 1px solid var(--soft-border);
        border-radius: 22px;
        padding: 1rem 1rem 0.35rem;
        margin: 0.75rem 0 1rem;
        box-shadow: 0 10px 25px rgba(49, 91, 42, 0.07);
    }

    @media (max-width: 640px) {
        .block-container {
            padding-left: 0.8rem;
            padding-right: 0.8rem;
            padding-top: 0.75rem;
        }

        .scamshield-hero {
            border-radius: 20px;
            padding: 1.1rem 0.9rem;
        }

        .section-card {
            border-radius: 18px;
            padding: 0.8rem 0.75rem 0.25rem;
        }

        .stButton > button {
            min-height: 52px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

def page_hero(title="ScamShield", subtitle="AI Scam Message Detector", copy=""):
    copy_html = f'<div class="copy">{copy}</div>' if copy else ""
    st.markdown(
        f"""
        <div class="scamshield-hero">
            <div class="shield">🛡️</div>
            <div class="title">{title}</div>
            <div class="subtitle">{subtitle}</div>
            {copy_html}
        </div>
        """,
        unsafe_allow_html=True
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
    headers={
        "Authorization": f"Bearer {ollama_api_key}"
    }
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
    page_hero(
        copy=(
            "Enter an email or text message below. "
            "ScamShield will analyze it for possible scam warning signs."
        )
    )

    # Ask for message type
    with st.container(border=True):
        message_type = st.selectbox(
            "Message Type",
            [
                "Select Message Type",
                "Email",
                "Text Message"
            ]
        )

    message_to_analyze = ""

    # Email inputs
    if message_type == "Email":
        with st.container(border=True):
            sender = st.text_input(
                "From Email Address",
                placeholder="example@email.com"
            )

            subject = st.text_input(
                "Subject",
                placeholder="Enter email subject"
            )

            body = st.text_area(
                "Email Body",
                placeholder="Paste the email here...",
                height=200
            )

            attachment = st.selectbox(
                "Does the email have an attachment?",
                ["No", "Yes"]
            )

            message_to_analyze = f"""
Message Type: Email
Sender: {sender}
Subject: {subject}
Body: {body}
Attachment: {attachment}
"""

    # Text message inputs
    elif message_type == "Text Message":
        with st.container(border=True):
            phone_number = st.text_input(
                "Phone Number",
                placeholder="555-123-4567"
            )

            message = st.text_area(
                "Text Message",
                placeholder="Paste the text message here...",
                height=200
            )

            message_to_analyze = f"""
Message Type: Text Message
Phone Number: {phone_number}
Message: {message}
"""

    st.divider()

    # Analyze button
    if st.button(
        "🔍 Analyze Message",
        use_container_width=True
    ):
        if message_type == "Select Message Type":
            st.warning("Please select Email or Text Message.")
            return

        if message_to_analyze.strip() == "":
            st.warning("Please enter a message.")
            return

        # Create AI prompt
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

        # Call Ollama AI
        try:
            with st.spinner("ScamShield is analyzing the message..."):
                response = client.chat(
                    model="gemma4:cloud",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    format="json",
                    options={
                        "temperature": 0
                    }
                )

            # Get AI response
            ai_response = response["message"]["content"]

            # Convert JSON response into a dictionary
            result = json.loads(ai_response)

            # Save result and go to result page
            st.session_state.result = result
            st.session_state.page = "result"
            st.rerun()

        except Exception as e:
            st.session_state.error_message = str(e)
            st.session_state.page = "error"
            st.rerun()

# Page 2 - Result page
def result_page():
    page_hero(subtitle="AI Scam Message Detector")
    st.success("✅ Analysis Complete")
    st.header("Scan Result")
    st.divider()

    # Get saved result
    result = st.session_state.get("result")

    if result is None:
        st.error("No analysis result was found.")

        if st.button("🔄 Back to Scanner"):
            st.session_state.page = "scan"
            st.rerun()

        return

    # Make sure result is a dictionary
    if isinstance(result, str):
        try:
            result = json.loads(result)
        except json.JSONDecodeError:
            st.error("The AI returned an invalid result.")
            return

    # Get result values
    risk_level = result.get(
        "risk_level",
        "UNKNOWN"
    )

    warning_signs = result.get(
        "warning_signs",
        []
    )

    recommendation = result.get(
        "recommendation",
        "No recommendation available."
    )

    risk_level = str(risk_level).upper()

    # Display risk level
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

    # Display warning signs
    st.subheader("⚠️ Warning Signs")

    if isinstance(warning_signs, list):
        for sign in warning_signs:
            st.write(f"• {sign}")
    else:
        st.write(f"• {warning_signs}")

    st.divider()

    # Display recommendation
    st.subheader("🛡️ Recommendation")
    st.info(recommendation)
    st.divider()

    # Scan another message
    if st.button(
        "🔍 Scan Another Message",
        use_container_width=True
    ):
        st.session_state.result = None
        st.session_state.error_message = None
        st.session_state.page = "scan"
        st.rerun()

# Page 3 - Error page
def error_page():
    page_hero(subtitle="AI Scam Message Detector")
    st.error("⚠️ Something Went Wrong")
    st.header("We couldn't analyze your message.")

    st.write(
        "ScamShield had a problem communicating "
        "with the Ollama AI service."
    )

    st.divider()

    # Possible reasons
    st.subheader("Possible Reasons")
    st.write("• The Ollama API key may be missing or incorrect.")
    st.write("• The selected model may not be available.")
    st.write("• There may be an internet or API connection problem.")
    st.write("• Ollama may have returned an invalid response.")
    st.write("• The AI response may not contain valid JSON.")

    st.divider()

    st.info(
        "Check your Ollama API key and model settings, "
        "then try again."
    )

    # Show technical error
    error_message = st.session_state.get("error_message")

    if error_message:
        with st.expander("🔧 Technical Details"):
            st.code(error_message)

    st.divider()

    # Try again
    if st.button(
        "🔄 Try Again",
        use_container_width=True
    ):
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