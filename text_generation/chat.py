from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

my_key = os.getenv("openai_apikey")

client = OpenAI(api_key=my_key)

import streamlit as st

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "system", "content":"Sen yardımsever bir asistansın."})

def generate_response(prompt):
    st.session_state.messages.append({"role": "user", "content": prompt})

    AI_Response = client.chat.completions.create(

        model = "gpt-4-1106-preview",
        messages=st.session_state.messages
    )

    return AI_Response.choices[0].message.content


st.header("İlk Sohbet Botum")
st.divider()

for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Mesajınızı Giriniz"):

    st.chat_message("user").markdown(prompt)

    response = generate_response(prompt)

    with st.chat_message("assistant"):
        st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})

