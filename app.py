import openai
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

st.title("Hi! I'm Chatty Bot")

# in case of call to OpenAI API, you can set the API key and model name in the .env file
# openai.api_key = os.getenv("OPENAI_API_KEY", "")
# MODEL = "gpt-4.1-nano-2025-04-14"

BASE_URL = os.getenv("BASE_URL")
MODEL = os.getenv("LLM_MODEL_NAME")


if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = MODEL

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask me anything"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # Check for specific names asking if they are gay
        names_to_check = ["Gabriel", "Orzech", "Konrad", "Konradek", "Mirek", "Miro"]
        prompt_lower = prompt.lower()

        # Check for English question
        is_gay_question_en = any(name.lower() in prompt_lower for name in names_to_check) and "gay" in prompt_lower

        # Check for Polish question (czy...jest gejem/pederastą or similar variations)
        is_gay_question_pl = any(name.lower() in prompt_lower for name in names_to_check) and any(
            word in prompt_lower for word in ["gej", "gejowski", "gejem", "peda", "pederast", "homoseksualn"]
        )

        if is_gay_question_en:
            # Return the fixed response in English
            full_response = "Oh, yes he is! Big Gay Al could learn from him!"
        elif is_gay_question_pl:
            # Return the fixed response in Polish
            full_response = "Pewnie! Jeszcze jak"
        else:
            # Send user message to OpenAI and get response
            client = openai.OpenAI(
                base_url=BASE_URL,
                api_key="ollama"  # dummy value
            )
            try:
                response = client.chat.completions.create(
                    model=st.session_state["openai_model"],
                    messages=st.session_state.messages,
                    stream=True,
                )
                for chunk in response:
                    chunk_message = chunk.choices[0].delta.content or ""
                    if chunk_message is not None:
                        full_response += chunk_message
                        # Update the assistant message placeholder with the new content
                        message_placeholder.markdown(full_response + "▌")
            except openai.NotFoundError:
                full_response = f"Model '{MODEL}' not found on the local LLM server. Please check the model name and availability."

        # Replace the placeholder with the full response
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
