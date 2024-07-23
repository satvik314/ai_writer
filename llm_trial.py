import streamlit as st
from portkey_ai import Portkey
from model_config import get_model_config

portkey_api_key = st.secrets['PORTKEY_API_KEY']


portkey = Portkey(api_key= portkey_api_key)

selected_model = "sonnet"  # This could be dynamically chosen
config = get_model_config(selected_model)
messages = [{"role": "user", "content": "How's the weather like in San Francisco?"}]

if config:
    response = portkey.with_options(config=config).chat.completions.create(
        messages=messages,
        max_tokens=1024,
    )
    response_message = response.choices[0].message
    print(response_message)
else:
    st.error(f"Configuration for model '{selected_model}' not found.")