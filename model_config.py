import streamlit as st

MODEL_CONFIGS = {
    "sonnet": {
        "config_name": "sonnet",
        "model": "claude-3-5-sonnet-20240620",
        "provider": "anthropic",
        "api_key": st.secrets['ANTHROPIC_API_KEY']
    },
    "gemini": {
        "config_name": "gemini",
        "model": "gemini-1.5-pro-002",
        "provider": "google",
        "api_key": st.secrets['GOOGLE_API_KEY']
    },
    "gpt_4o_mini": {
        "config_name": "gpt_4o_mini",
        "model": "gpt-4o-mini",
        "provider": "openai",
        "api_key": st.secrets['OPENAI_API_KEY']
    },
    "sonar": {
        "config_name": "sonar",
        "model": "perplexity/llama-3.1-sonar-large-128k-online",
        "provider": "openrouter",
        "api_key": st.secrets['OPENROUTER_API_KEY']
    }
}

def get_model_config(model_name):
    return MODEL_CONFIGS.get(model_name)

def get_model_snug(model_name):
    return MODEL_CONFIGS.get(model_name)['model']
