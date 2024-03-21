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
st.image(logo_path, width=200)  # Logo-Größe anpassen
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
        }
        .assistant-message {
            background-color: #A0E7E5;
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
        model="ft:gpt-3.5-turbo-1106:personal:lf-gpt-3:92Poyhqy",  # Fine-tuning Model ID (Name)
        messages=[{"role": "system", "content": "Du bist ein hilfreicher LiveFresh Assistent für Produkt- und Gesundheitsberatung."},
                  *st.session_state['messages'],
                  {"role": "user", "content": question}],
    )
    return response.choices[0].message['content']

# Texteingabefeld für die Nutzereingabe
user_input = st.text_input("Deine Nachricht:", key="user_input")

# Funktion, die ausgeführt wird, wenn der Senden-Button gedrückt wird
def on_send():
    if st.session_state.user_input:  # Stellt sicher, dass die Eingabe nicht leer ist
        # Erhalte die Antwort vom Fine-Tuning Model und füge sie zum Chatverlauf hinzu
        answer = get_response(st.session_state.user_input)
        st.session_state['messages'].append({"role": "user", "content": st.session_state.user_input})
        st.session_state['messages'].append({"role": "assistant", "content": answer})
        # Bereite das Texteingabefeld für die nächste Nachricht vor
        st.session_state.user_input = ""

# Button, um die Nachricht zu senden
send_button = st.button('Senden', on_click=on_send)

# Anzeigen des Chatverlaufs
for index, message in enumerate(st.session_state['messages']):
    role = "Du:" if message["role"] == "user" else "Assistent:"
    # Verwende nur den Index für den Schlüssel
    st.text_area(label=role, value=message["content"], height=75, key=f"msg_{index}")
