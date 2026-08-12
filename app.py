import streamlit as st
import json
from ollama import Client

# Page settings
st.set_page_config(
    page_title="ScamShield",
    page_icon="🛡️",
    layout="centered"
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
    st.title("🛡️ ScamShield")
    st.subheader("AI Scam Message Detector")
    st.write(
        "Enter an email or text message below. "
        "ScamShield will analyze it for possible scam warning signs."
    )
    st.divider()

    # Ask for message type
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
                    model="kimi-k2.5:cloud",
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
    st.title("🛡️ ScamShield")
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
    st.title("🛡️ ScamShield")
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