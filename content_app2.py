import streamlit as st
import requests
import json
import os
from youtube_transcript_api import YouTubeTranscriptApi

# Set your API key as an environment variable
os.environ['OPENROUTER_API_KEY'] = st.secrets['OPENROUTER_API_KEY']

# Load samples from the text files
def load_samples(file_name):
    with open(file_name, 'r') as file:
        return file.read()

twitter_samples = load_samples('twitter_posts.txt')
linkedin_samples = load_samples('linkedin_posts.txt')
blog_samples = load_samples('blog_posts.txt')

# Custom CSS
def local_css(file_name):
    with open(file_name, 'r') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Streamlit app
def main():
    st.set_page_config(page_title='Content Generator', page_icon='🚀', layout='wide')
    
    # Apply custom CSS
    
    
    st.sidebar.markdown("<h1 style='text-align: center;'>🎛️ Input</h1>", unsafe_allow_html=True)
    
    # Get the API key from environment variables
    api_key = os.getenv('OPENROUTER_API_KEY')

    # Initialize session state variables
    if 'content' not in st.session_state:
        st.session_state.content = ''
    if 'generated_content' not in st.session_state:
        st.session_state.generated_content = {}
    
    # Sidebar inputs
    st.sidebar.markdown("<h2>📥 Input Type</h2>", unsafe_allow_html=True)
    input_type = st.sidebar.radio("", ("✏️ Text", "🎥 YouTube URL", "🔮 Perplexity Sonar"))

    if "Text" in input_type:
        st.session_state.content = st.sidebar.text_area('Enter your content:', value=st.session_state.content, height=200)
    elif "YouTube" in input_type:
        youtube_url = st.sidebar.text_input('Enter the YouTube URL:')
    else:  # Perplexity Sonar
        recent_topic = st.sidebar.text_input('Enter the recent topic:')

    # Main content area
    st.markdown("<h1 style='text-align: center;'>🚀 Content Generator</h1>", unsafe_allow_html=True)

    # Create tabs for different platforms
    tabs = st.tabs(["🐦 Twitter", "💼 LinkedIn", "📝 Blog"])

    for i, platform in enumerate(["Twitter", "LinkedIn", "Blog"]):
        with tabs[i]:
            emoji = "🐦" if platform == "Twitter" else "💼" if platform == "LinkedIn" else "📝"
            st.markdown(f"<h2 style='text-align: center;'>{emoji} {platform} Content</h2>", unsafe_allow_html=True)

            if st.button(f'Generate {platform} Content 🎨'):
                with st.spinner(f'Generating {platform} content...'):
                    if "Text" in input_type:
                        samples = get_samples(platform)
                        st.session_state.generated_content[platform] = generate_content(api_key, st.session_state.content, samples, platform)
                    elif "YouTube" in input_type:
                        if youtube_url:
                            video_id = youtube_url.split("v=")[1]
                            transcript = YouTubeTranscriptApi.get_transcript(video_id)
                            content = " ".join([entry['text'] for entry in transcript])
                            samples = get_samples(platform)
                            st.session_state.generated_content[platform] = generate_content(api_key, content, samples, platform)
                        else:
                            st.warning("⚠️ Please enter a YouTube URL.")
                    else:  # Perplexity Sonar
                        if recent_topic:
                            content = get_perplexity_sonar_response(recent_topic, platform)
                            samples = get_samples(platform)
                            st.session_state.generated_content[platform] = generate_content(api_key, content, samples, platform)
                        else:
                            st.warning("⚠️ Please enter a recent topic.")

            # Display generated content
            if platform in st.session_state.generated_content:
                st.markdown("<h3>📄 Generated Content</h3>", unsafe_allow_html=True)
                st.text_area('', value=st.session_state.generated_content[platform], height=300)
                
                if st.button(f'Copy {platform} Content to Clipboard 📋'):
                    st.code(st.session_state.generated_content[platform])
                    st.success(f'✅ {platform} content copied to clipboard!')
            else:
                st.info(f'ℹ️ Click "Generate {platform} Content" to create a post or article.')

def get_samples(platform):
    if platform == "Twitter":
        return twitter_samples
    elif platform == "LinkedIn":
        return linkedin_samples
    else:
        return blog_samples

def generate_content(api_key, content, samples, platform):
    if api_key and content:
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        
        prompt = f"Convert the below content into a {platform} "
        prompt += "post in my writing style." if platform != "Blog" else "article in my writing style. Include a title, introduction, main body with subheadings, and conclusion."
        
        data = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                { "role": "user", "content": f"{prompt}\n\n{content}\n\n\nHere are some of my previous {platform} posts/articles:\n\n{samples}\n\n\n\n\n" }
            ]
        }
        
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(data)
        )
        response_data = response.json()
        return response_data['choices'][0]['message']['content']
    else:
        st.warning('⚠️ Please enter both the API key and content.')
        return ''

def get_perplexity_sonar_response(recent_topic, platform):
    api_key = os.getenv('OPENROUTER_API_KEY')

    if api_key and recent_topic:
        headers = {
            "Authorization": f"Bearer {api_key}",
        }

        data = {
            "model": "perplexity/llama-3-sonar-large-32k-online",
            "messages": [
                {
                    "role": "user",
                    "content": f"Generate a {platform} post about '{recent_topic}'",
                },
            ],
        }

        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(data),
        )

        response_data = response.json()
        return response_data['choices'][0]['message']['content']
    else:
        st.warning('⚠️ Please enter both the API key and recent topic.')
        return ''

if __name__ == '__main__':
  main()
