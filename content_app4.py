import streamlit as st
import os
from youtube_transcript_api import YouTubeTranscriptApi
from portkey_ai import Portkey
from model_config import get_model_config

# Set API key from Streamlit secrets
portkey_api_key = st.secrets['PORTKEY_API_KEY']
portkey = Portkey(api_key=portkey_api_key)

# Load sample posts
def load_samples(file_name):
    with open(file_name, 'r') as file:
        return file.read()

twitter_samples = load_samples('twitter_posts.txt')
linkedin_samples = load_samples('linkedin_posts.txt')
blog_samples = load_samples('blog_posts.txt')

def get_samples(platform):
    if platform == "Twitter":
        return twitter_samples
    elif platform == "LinkedIn":
        return linkedin_samples
    else:
        return blog_samples

def generate_content(content, samples, platform):
    if not content:
        st.warning('⚠️ Please enter content.')
        return ''

    prompt = f"Convert the below content into a {platform} "
    prompt += "post in my writing style." if platform != "Blog" else "article in my writing style. Include a title, introduction, main body with subheadings, and conclusion."
    
    messages = [
        {"role": "user", "content": f"{prompt}\n\n{content}\n\n\nHere are some of my previous {platform} posts/articles:\n\n{samples}\n\n\n\n\n"}
    ]
    print(content)
    config = get_model_config("sonnet") 
    if config:
        response = portkey.with_options(config=config).chat.completions.create(
            messages=messages,
            max_tokens=1024,
        )
        return response.choices[0].message.content
    else:
        st.error("Configuration for model 'sonnet' not found.")
        return ''

def get_perplexity_sonar_response(recent_topic):
    if not recent_topic:
        st.warning('⚠️ Please enter a recent topic.')
        return ''

    messages = [
        {"role": "user", "content": f"Give the latest news on '{recent_topic}'"}
    ]

    config = get_model_config("sonar")  
    if config:
        response = portkey.with_options(config=config).chat.completions.create(
            messages=messages,
            max_tokens=1024,
        )
        return response.choices[0].message.content
    else:
        st.error("Configuration for model 'sonar' not found.")
        return ''

def get_youtube_transcript(youtube_url):
    video_id = youtube_url.split("v=")[1]
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return " ".join([entry['text'] for entry in transcript])

def setup_sidebar():
    st.sidebar.markdown("<h1 style='text-align: center;'>🎛️ Input</h1>", unsafe_allow_html=True)
    st.sidebar.markdown("<h2>📥 Input Type</h2>", unsafe_allow_html=True)
    input_type = st.sidebar.radio("", ("✏️ Text", "🎥 YouTube URL", "🔮 Perplexity Sonar"))
    
    content = ""
    if "Text" in input_type:
        content = st.sidebar.text_area('Enter your content:', value=st.session_state.get('content', ''), height=200)
        st.session_state.content = content
    elif "YouTube" in input_type:
        content = st.sidebar.text_input('Enter the YouTube URL:')
    else:  # Perplexity Sonar
        content = st.sidebar.text_input('Enter the recent topic:')
    
    return input_type, content

def display_generated_content(platform, generated_content):
    st.markdown("<h3>📄 Generated Content</h3>", unsafe_allow_html=True)
    st.text_area('', value=generated_content, height=300)
    
    if st.button(f'Copy {platform} Content to Clipboard 📋'):
        st.code(generated_content)
        st.success(f'✅ {platform} content copied to clipboard!')

def main():
    st.set_page_config(page_title='Content Generator', page_icon='🚀', layout='wide')

    if 'generated_content' not in st.session_state:
        st.session_state.generated_content = {}

    input_type, content = setup_sidebar()

    st.markdown("<h1 style='text-align: center;'>🚀 Content Generator</h1>", unsafe_allow_html=True)

    tabs = st.tabs(["🐦 Twitter", "💼 LinkedIn", "📝 Blog"])

    for i, platform in enumerate(["Twitter", "LinkedIn", "Blog"]):
        with tabs[i]:
            emoji = "🐦" if platform == "Twitter" else "💼" if platform == "LinkedIn" else "📝"
            st.markdown(f"<h2 style='text-align: center;'>{emoji} {platform} Content</h2>", unsafe_allow_html=True)

            if st.button(f'Generate {platform} Content 🎨'):
                with st.spinner(f'Generating {platform} content...'):
                    samples = get_samples(platform)
                    if "Text" in input_type:
                        generated_content = generate_content(content, samples, platform)
                    elif "YouTube" in input_type:
                        if content:
                            youtube_content = get_youtube_transcript(content)
                            generated_content = generate_content(youtube_content, samples, platform)
                        else:
                            st.warning("⚠️ Please enter a YouTube URL.")
                            continue
                    else:  # Perplexity Sonar
                        if content:
                            sonar_content = get_perplexity_sonar_response(content)
                            print(sonar_content)
                            generated_content = generate_content(sonar_content, samples, platform)
                        else:
                            st.warning("⚠️ Please enter a recent topic.")
                            continue
                    
                    st.session_state.generated_content[platform] = generated_content

            if platform in st.session_state.generated_content:
                display_generated_content(platform, st.session_state.generated_content[platform])
            else:
                st.info(f'ℹ️ Click "Generate {platform} Content" to create a post or article.')

if __name__ == '__main__':
    main()