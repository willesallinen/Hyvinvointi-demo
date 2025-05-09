import streamlit as st
from datetime import datetime, timedelta
import hashlib

login_timestamps = {}

st.set_page_config(page_title="Hyvinvointikysely", page_icon="💚", layout="centered")

def hash_email(email):
    return hashlib.sha256(email.encode()).hexdigest()

def check_login(email):
    hashed = hash_email(email)
    now = datetime.now()
    last_login = login_timestamps.get(hashed)
    if last_login and now - last_login < timedelta(hours=12):
        return False
    login_timestamps[hashed] = now
    return True

def styled_buttons():
    st.markdown("""
    <style>
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
    </style>
    """, unsafe_allow_html=True)

def main():
    styled_buttons()

    if "stage" not in st.session_state:
        st.session_state.stage = "login"

    if st.session_state.stage == "login":
        with st.form("login_form"):
            email = st.text_input("Syötä sähköpostisi:")
            submitted = st.form_submit_button("Kirjaudu sisään")
            if submitted:
                if email and check_login(email):
                    st.session_state.stage = "question"
                    st.session_state.email = email
                else:
                    st.error("Olet jo vastannut viimeisen 12 tunnin sisällä.")

    elif st.session_state.stage == "question":
        st.header("Miten voit tänään?")
        with st.form("question_form"):
            good = st.form_submit_button("Hyvin")
            bad = st.form_submit_button("Huonosti")
            if good:
                st.session_state.stage = "good"
            elif bad:
                st.session_state.stage = "bad"

    elif st.session_state.stage == "good":
        st.success("Mahtava kuulla, Kiitos että vastasit! 💚")
        # Sähköpostin lähetys voidaan lisätä tähän

    elif st.session_state.stage == "bad":
        st.header("Kerro mihin ongelmasi liittyy?")
        with st.form("bad_form"):
            atmosphere = st.form_submit_button("Työilmapiiri")
            environment = st.form_submit_button("Työympäristö")
            if atmosphere:
                st.session_state.stage = "bad_atmosphere"
            elif environment:
                st.session_state.stage = "bad_environment"

    elif st.session_state.stage == "bad_atmosphere":
        st.subheader("Työilmapiiri")
        with st.form("atmosphere_form"):
            manager = st.form_submit_button("Esihenkilö")
            other = st.form_submit_button("Jokin muu")
            if manager:
                st.session_state.stage = "form_input_atmo_manager"
            elif other:
                st.session_state.stage = "form_input_atmo_other"

    elif st.session_state.stage == "bad_environment":
        st.subheader("Työympäristö")
        with st.form("environment_form"):
            desk = st.form_submit_button("Oma työpiste")
            other = st.form_submit_button("Jokin muu")
            if desk:
                st.session_state.stage = "form_input_env_desk"
            elif other:
                st.session_state.stage = "form_input_env_other"

    elif "form_input" in st.session_state.stage:
        st.subheader("Kuvaile ongelmaasi (max 500 merkkiä)")
        with st.form("feedback_form"):
            msg = st.text_area("Kirjoita viestisi", max_chars=500)
            send = st.form_submit_button("Lähetä")
            if send:
                st.success("Kiitos vastauksestasi!")
                # Tähän lisätään sähköpostin lähetys
                st.session_state.stage = "done"

    elif st.session_state.stage == "done":
        st.success("Vastauksesi on vastaanotettu.")

if __name__ == "__main__":
    main()
