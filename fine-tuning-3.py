import openai
import streamlit as st
from dotenv import load_dotenv
import os

# Lade Umgebungsvariablen
load_dotenv()

# API-Schlüssel aus der Umgebungsvariablen lesen
openai.api_key = os.getenv('OPENAI_API_KEY')

# LiveFresh-Logo
logo_path = 'logolivefresh.png'

# Titel und Logo der Streamlit Seite/App
st.image(logo_path, width=200) 
st.title('LiveFresh Berater')

# CSS für den Chat anpassen
st.markdown(
    """
    <style>
        .chat-message {
            border-radius: 25px;
            padding: 10px;
            margin: 5px 0;
        }
        .user-message {
            background-color: #FFAFBD;
            margin-left: 20%;
            text-align: right;
        }
        .assistant-message {
            background-color: #A0E7E5;
            margin-right: 20%;
            text-align: left;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialisiere den Chatverlauf und den Texteingabewert, wenn nicht vorhanden
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Funktion, um eine Antwort vom OpenAI-Assistenten zu erhalten
def get_response(question):
    response = openai.ChatCompletion.create(
        model="ft:gpt-3.5-turbo-1106:personal:lf-gpt-3:92Poyhqy",
        messages=[{"role": "system", "content": "Du bist ein hilfreicher LiveFresh Assistent für Produkt- und Gesundheitsberatung."},
                  *st.session_state['messages'],
                  {"role": "user", "content": question}],
    )
    return response.choices[0].message['content']

# Funktion, die ausgeführt wird, wenn der Senden-Button gedrückt wird
def on_send():
    if st.session_state.user_input:  # Stellt sicher, dass die Eingabe nicht leer ist
        answer = get_response(st.session_state.user_input)
        # Füge die neue Nachricht und Antwort am Anfang der Liste hinzu
        st.session_state['messages'].insert(0, {"role": "assistant", "content": answer})
        st.session_state['messages'].insert(0, {"role": "user", "content": st.session_state.user_input})
        st.session_state.user_input = ""  # Texteingabefeld leeren

# Texteingabefeld für die Nutzereingabe
st.text_input("Deine Nachricht:", key="user_input", on_change=on_send)

# Button, um die Nachricht zu senden
st.button('Senden', on_click=on_send)

# Anzeigen des Chatverlaufs
for message in st.session_state['messages']:
    role_class = "user-message" if message["role"] == "user" else "assistant-message"
    role_label = "Du:" if message["role"] == "user" else "Assistent:"
    st.markdown(f'<div class="chat-message {role_class}"><b>{role_label}</b> {message["content"]}</div>', unsafe_allow_html=True)
