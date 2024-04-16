from openai import OpenAI
import assemblyai as aai
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

my_key_openai = os.getenv("openai_apikey")
my_key_assemblyai = os.getenv("assemblyai_apikey")

client = OpenAI(
    api_key=my_key_openai
)

def create_speech_from_text(prompt, speech_file_name, voice_type="alloy"):

    AI_Response = client.audio.speech.create(
        model="tts-1",
        voice=voice_type,
        response_format="mp3",
        input=prompt
    )

    AI_Response.stream_to_file(speech_file_name)

    return "Seslendirme İşlemi Tamamlandı"

def transcribe_with_whisper(audio_file_name):

    audio_file = open(audio_file_name, "rb")

    AI_generated_transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        language="tr"
    )

    return AI_generated_transcript.text

def translate_with_whisper(audio_file_name):

    audio_file = open(audio_file_name, "rb")

    AI_generated_translation = client.audio.translations.create(
        model="whisper-1",
        file=audio_file
    )

    return AI_generated_translation.text

def transcribe_with_conformer(audio_file_name):

    aai.settings.api_key = my_key_assemblyai
    transcriber = aai.Transcriber()

    AI_generated_text = transcriber.transcribe(audio_file_name)

    return AI_generated_text.text






tab_TTS, tab_whisper, tab_translation, tab_conformer = st.tabs(
    [
     "TTS ile Ses Sentezleme", 
     "Whisper ile Transkripsiyon", 
     "Whisper ile Tercüme", 
     "Conformer ile Transkripsiyon"
     ]
)

with tab_TTS:
    st.subheader("TTS-1 Modeli ile Konuşma Sentezleme")
    st.divider()

    prompt = st.text_input("Seslendirmek istediğiniz metni giriniz", key="prompt_tts")
    voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
    voice_type = st.selectbox(label="Ses tercihiniz:", options=voices, key="voice_tts")
    generate_btn = st.button("Ses Sentezle", key="button_tts")

    if generate_btn:
        
        status = create_speech_from_text(prompt=prompt, speech_file_name="speech.mp3", voice_type=voice_type)
        st.success(status)

        audio_file = open("speech.mp3", "rb")
        audio_bytes = audio_file.read()

        st.audio(data=audio_bytes, format="audio/mp3")
        st.balloons()

with tab_whisper:

    st.subheader("Whisper Modeli ile Transkripsiyon")
    st.divider()

    selected_file = st.file_uploader("Bir ses dosyası seçiniz", type=["mp3"], key="file_whisper")

    if selected_file:

        audio_file = open(selected_file.name, "rb")
        audio_bytes = audio_file.read()
        st.audio(data=audio_bytes, format="audio/mp3")

    transcribe_btn = st.button("Metne Dönüştür", key="button_whisper")

    if transcribe_btn:
        
        generated_text = transcribe_with_whisper(audio_file_name=selected_file.name)

        st.divider()
        st.info(f"TRANSKRİPSİYON: {generated_text}")
        st.balloons()

with tab_translation:

    st.subheader("Whisper Modeli ile Tercüme")
    st.divider()

    selected_file = st.file_uploader("Bir ses dosyası seçiniz", type=["mp3"], key="file_translation")

    if selected_file:

        audio_file = open(selected_file.name, "rb")
        audio_bytes = audio_file.read()
        st.audio(data=audio_bytes, format="audio/mp3")

    translate_btn = st.button("Tercüme Et", key="button_translation")

    if translate_btn:
        
        translated_text = translate_with_whisper(audio_file_name=selected_file.name)

        st.divider()
        st.info(f"TERCÜME: {translated_text}")
        st.balloons()

with tab_conformer:

    st.subheader("Conformer Modeli ile Transkripsiyon")
    st.divider()

    selected_file = st.file_uploader("Bir ses dosyası seçiniz", type=["mp3"], key="file_conformer")

    if selected_file:

        audio_file = open(selected_file.name, "rb")
        audio_bytes = audio_file.read()
        st.audio(data=audio_bytes, format="audio/mp3")

    transcribe_btn = st.button("Metne Dönüştür", key="button_conformer")

    if transcribe_btn:
        
        generated_text = transcribe_with_conformer(audio_file_name=selected_file.name)

        st.divider()
        st.info(f"TRANSKRİPSİYON: {generated_text}")
        st.balloons()