import streamlit as st
from datetime import datetime, timedelta
import hashlib

# Tallennetaan käyttäjien kirjautumisajat (vain muistissa demoa varten)
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

def main():
    st.markdown(
        """
        <style>
        .stButton > button {
            width: 100%;
            margin-bottom: 1rem;
            background-color: #A8E10C;
            color: #ffffff;
            font-weight: bold;
            border-radius: 8px;
            padding: 0.75rem;
        }
        .stButton > button:hover {
            background-color: #8CCF0C;
        }
        body {
            background-color: #1f1f1f;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("💚 Päivittäinen hyvinvointikysely")

    if "stage" not in st.session_state:
        st.session_state.stage = "login"

    if st.session_state.stage == "login":
        email = st.text_input("Syötä sähköpostisi:")
        if st.button("Kirjaudu sisään"):
            if email and check_login(email):
                st.session_state.stage = "question"
            else:
                st.error("Olet jo vastannut viimeisen 12 tunnin sisällä.")

    elif st.session_state.stage == "question":
        st.header("Miten voit tänään?")
        if st.button("Hyvin"):
            st.session_state.stage = "good"
        if st.button("Huonosti"):
            st.session_state.stage = "bad"

    elif st.session_state.stage == "good":
        st.success("Mahtava kuulla, Kiitos että vastasit! 💚")

    elif st.session_state.stage == "bad":
        st.header("Kerro mihin ongelmasi liittyy?")
        if st.button("Työilmapiiri"):
            st.info("Kiitos palautteesta liittyen työilmapiiriin.")
        if st.button("Työympäristö"):
            st.info("Kiitos palautteesta liittyen työympäristöön.")

if __name__ == "__main__":
    main()
