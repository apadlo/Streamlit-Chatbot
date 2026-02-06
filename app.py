import openai
import streamlit as st



st.title("Hi! I'm Chatty Bot")

openai.api_key = st.secrets["OPENAI_API_KEY"]

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4.1-nano-2025-04-14"

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
        is_gay_question = any(name.lower() in prompt.lower() for name in names_to_check) and "gay" in prompt.lower()

        if is_gay_question:
            # Return the fixed response
            full_response = "Oh, yes he is! Big Gay Al could learn from him!"
        else:
            # Send user message to OpenAI and get response
            response = openai.ChatCompletion.create(
                model=st.session_state["openai_model"],
                messages=st.session_state.messages,
                stream=True,
            )

            for chunk in response:
                chunk_message = chunk["choices"][0]["delta"].get("content", "")
                full_response += chunk_message
                # Update the assistant message placeholder with the new content
                message_placeholder.markdown(full_response + "▌")

        # Replace the placeholder with the full response
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
