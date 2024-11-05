import requests
import streamlit as st

st.title("ChatGPT-like clone with Hugging Face API")

# Hugging Face API Key from Streamlit secrets
HUGGINGFACE_API_KEY = st.secrets["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"]

# Define the model ID you want to use
model_id = "mistralai/Mistral-7B-Instruct-v0.1"

# System prompt
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are an expert at rhyming and poems. "
                "You will always answer using rhyming words or sentences. "
                "You will never break character."
            ),
        }
    ]

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Maximum allowed messages
max_messages = 20  # 10 user-assistant exchanges

if len(st.session_state.messages) >= max_messages:
    st.info(
        """Notice: The maximum message limit for this demo version has been reached.
        We encourage you to experience further interactions by building your own application."""
    )
else:
    # User input
    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response using Hugging Face API
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            # Hugging Face API request
            headers = {
                "Authorization": f"Bearer {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}"
            }
            data = {
                "inputs": [
                    {
                        "role": m["role"],
                        "content": m["content"]
                    }
                    for m in st.session_state.messages
                ]
            }

            response = requests.post(
                f"https://api-inference.huggingface.co/models/{model_id}",
                headers=headers,
                json=data,
                stream=True
            )

            if response.status_code == 200:
                # Process response and display it
                for chunk in response.iter_lines():
                    if chunk:
                        full_response += chunk.decode("utf-8")
                        message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
                st.session_state.messages.append(
                    {"role": "assistant", "content": full_response}
                )
            else:
                st.error(f"Error: {response.status_code}, {response.text}")

