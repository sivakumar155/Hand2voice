"""Touch-based AAC-style phrase board (does not require a trained model)."""
import streamlit as st
import pyttsx3

from communication_phrases import CATEGORIES

st.set_page_config(
    page_title="My Communication Assistant",
    page_icon="💬",
    layout="wide",
)
st.title("💬 My Communication Assistant")
st.caption("Choose a message. The app displays it and can speak it aloud.")

if "message" not in st.session_state:
    st.session_state.message = ""
if "history" not in st.session_state:
    st.session_state.history = []

def choose(message):
    st.session_state.message = message
    st.session_state.history.append(message)

for category, messages in CATEGORIES.items():
    st.header(category)
    cols = st.columns(3)
    for index, message in enumerate(messages):
        with cols[index % 3]:
            if st.button(message, key=f"{category}-{index}", use_container_width=True):
                choose(message)

st.divider()
st.subheader("Your message")
st.info(st.session_state.message or "Choose a message above.")

custom = st.text_input("Or type a custom message")
if st.button("Use custom message", disabled=not custom.strip()):
    choose(custom.strip())
    st.rerun()

left, middle, right = st.columns(3)
with left:
    if st.button("🔊 SPEAK", use_container_width=True,
                 disabled=not bool(st.session_state.message)):
        engine = pyttsx3.init()
        engine.setProperty("rate", 145)
        engine.say(st.session_state.message)
        engine.runAndWait()
        engine.stop()
with middle:
    if st.button("Clear message", use_container_width=True):
        st.session_state.message = ""
        st.rerun()
with right:
    if st.button("Emergency message", use_container_width=True):
        choose("I NEED EMERGENCY HELP")
        st.rerun()

st.divider()
st.subheader("Recent communication")
for item in reversed(st.session_state.history[-10:]):
    st.write(f"• {item}")

st.caption(
    "For emergencies, this prototype only speaks/displays a request. "
    "It does not automatically contact emergency services."
)
