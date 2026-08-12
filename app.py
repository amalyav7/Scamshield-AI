import streamlit as st
from openai import OpenAI
import json

# -----------------------------
# PAGE SETTINGS
# -----------------------------
st.set_page_config(
    page_title="PackPal AI",
    page_icon="🎒",
    layout="wide"
)
st.title("PackPal")

# -----------------------------
# CONNECT TO OLLAMA
# -----------------------------
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

# -----------------------------
# TITLE
# -----------------------------
st.title("🎒 PackPal AI")
st.subheader("Your Smart Backpack Assistant")

st.write(
    "Enter tomorrow's schedule and let AI build your backpack checklist."
)

st.divider()

# -----------------------------
# INPUTS
# -----------------------------

classes = st.text_input(
    "📚 Tomorrow's Classes",
    placeholder="Math, Biology, English..."
)

assignments = st.text_area(
    "📝 Assignments / Tests",
    placeholder="Algebra Worksheet 4..."
)

activities = st.text_input(
    "⚽ Activities",
    placeholder="Soccer Practice"
)

notes = st.text_area(
    "📌 Special Notes",
    placeholder="Bring permission slip..."
)

# -----------------------------
# BUTTON
# -----------------------------

generate = st.button(
    "🎒 Generate Checklist",
    use_container_width=True
)

# -----------------------------
# GENERATE
# -----------------------------

if generate:

    if (
        classes == ""
        and assignments == ""
        and activities == ""
        and notes == ""
    ):

        st.warning("Please enter some school information.")

    else:

        student_info = f"""
Classes:
{classes}

Assignments:
{assignments}

Activities:
{activities}

Special Notes:
{notes}
"""

        prompt = f"""
You are PackPal, an intelligent backpack assistant.

Your goal is to help students prepare for school tomorrow.

Rules:

- Think like an organized student.
- Only recommend school-related items.
- Do not invent unrelated items.
- Every category must contain ONLY a list of strings.
- If something is uncertain, place it under items_to_confirm.
- Return ONLY valid JSON.

Return exactly this format:

{{
"must_pack": [],
"to_complete": [],
"activity_items": [],
"prepare_tonight": [],
"items_to_confirm": []
}}

Student Information:

{student_info}
"""

        with st.spinner("🤖 PackPal is thinking..."):

            try:

                response = client.chat.completions.create(
                    model="llama3.2",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are PackPal, an AI backpack organizer. Return only valid JSON."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],

                    # Ask Ollama to return JSON instead of Markdown text.
                    response_format={"type": "json_object"},

                    # Lower temperature makes the output more predictable.
                    temperature=0
                )

                result = response.choices[0].message.content

                print("RAW RESPONSE:")
                print(repr(result))

                # Clean the AI response before converting it to JSON.
                # Some models may wrap JSON inside:
                #
                # ```json
                # { ... }
                # ```
                #
                # json.loads() cannot read the backticks, so remove them.
                cleaned_result = result.strip()

                if cleaned_result.startswith("```json"):
                    cleaned_result = cleaned_result[7:]

                elif cleaned_result.startswith("```"):
                    cleaned_result = cleaned_result[3:]

                if cleaned_result.endswith("```"):
                    cleaned_result = cleaned_result[:-3]

                cleaned_result = cleaned_result.strip()

                # Convert the cleaned JSON string into a Python dictionary.
                checklist = json.loads(cleaned_result)

                st.success("Checklist Created!")

                col1, col2 = st.columns(2)

                with col1:

                    st.header("🎒 Must Pack")

                    for item in checklist["must_pack"]:
                        st.checkbox(item)

                    st.header("⚽ Activity Items")

                    for item in checklist["activity_items"]:
                        st.checkbox(item)

                    st.header("❓ Items to Confirm")

                    for item in checklist["items_to_confirm"]:
                        st.write("•", item)

                with col2:

                    st.header("✅ To Complete")

                    for item in checklist["to_complete"]:
                        st.checkbox(item)

                    st.header("🌙 Prepare Tonight")

                    for item in checklist["prepare_tonight"]:
                        st.checkbox(item)

                with st.expander("📄 View JSON"):

                    st.json(checklist)

            except json.JSONDecodeError:

                st.error("AI did not return valid JSON.")

                st.code(result)

            except Exception as e:

                st.error("Unable to connect to Ollama.")

                st.code(str(e))