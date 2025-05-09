import streamlit as st
from datetime import datetime, timedelta
import hashlib

st.set_page_config(page_title="Hyvinvointikysely", page_icon="💚", layout="centered")

# Väriteema ja napit
st.markdown("""
<style>
body {
    background-color: #2E2E2E;
    color: white;
}
h1, h2, h3, h4 {
    color: white;
}
.stButton > button {
    width: 100%;
    margin-bottom: 1rem;
    background-color: #A8E10C;
    color: white;
    font-weight: bold;
    border-radius: 8px;
    padding: 0.75rem;
}
.stButton > button:hover {
    background-color: #8CCF0C;
}
textarea {
    background-color: #ffffff10 !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# Istunnon tila
if "stage" not in st.session_state:
    st.session_state.stage = "login"
if "email" not in st.session_state:
    st.session_state.email = ""
if "login_timestamps" not in st.session_state:
    st.session_state.login_timestamps = {}

# Apufunktiot
def hash_email(email):
    return hashlib.sha256(email.encode()).hexdigest()

def check_login(email):
    hashed = hash_email(email)
    now = datetime.now()
    last_login = st.session_state.login_timestamps.get(hashed)
    if last_login and now - last_login < timedelta(hours=12):
        return False
    st.session_state.login_timestamps[hashed] = now
    return True

# Vaiheittainen sovellus
def main():
    stage = st.session_state.stage

    if stage == "login":
        st.header("Kirjaudu sähköpostilla")
        email = st.text_input("Sähköposti")
        if st.button("Kirjaudu"):
            if email and check_login(email):
                st.session_state.email = email
                st.session_state.stage = "question"
            else:
                st.error("Olet jo vastannut viimeisen 12 tunnin aikana.")

    elif stage == "question":
        st.header("Miten voit tänään?")
        if st.button("Hyvin"):
            st.session_state.stage = "good"
        elif st.button("Huonosti"):
            st.session_state.stage = "bad"

    elif stage == "good":
        st.success("Mahtava kuulla,
