import streamlit as st
import anthropic
from utils import calculate_api_price

# Load samples from the 'linkedin_posts.txt' file
with open('linkedin_posts.txt', 'r') as file:
    linkedin_samples = file.read()
    twitter_samples = file.read()
    blog_samples = file.read()
# TODO: Load twitter_samples and blog_samples 

# Streamlit app
def main():
    st.set_page_config(page_title='Social Media Post Generator', layout='wide')
    
    # Get the API key from the user
    api_key = st.secrets['ANTHROPIC_API_KEY']
    
    # Add tabs for different platforms
    platform = st.tabs(["LinkedIn", "Twitter", "Blog"])
    
    for i, p in enumerate(platform):
        with p:
            # Get content type and input in sidebar
            content_type = st.sidebar.selectbox("Content Type", ["Text", "Image", "Video"], key=f"type_{i}")
            content = st.sidebar.text_area(f'Enter {content_type} to convert into a {p.title} post:', height=200, key=f"content_{i}")
            
            if st.sidebar.button('Generate Post', key=f"button_{i}"):
                if api_key and content:
                    client = anthropic.Anthropic(api_key=api_key)
                    
                    if p.title == "LinkedIn":
                        samples = linkedin_samples
                    elif p.title == "Twitter":
                        samples = twitter_samples
                    else:
                        samples = blog_samples
                    
                    message = client.messages.create(
                        model="claude-3-opus-20240229",
                        max_tokens=1000,
                        temperature=0,
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": f"Convert the below {content_type} into a {p.title} post in my writing style.\n\n{content}\n\n\nHere are some of my previous {p.title} posts:\n\n{samples}\n\n\n\n\n"
                                    }
                                ]
                            }
                        ]
                    )
                    
                    # Extract and display generated post
                    post_text = message.content[0].text
                    st.text_area(f'Generated {p.title} Post:', value=post_text, height=400)
                    
                    # Copy button
                    if st.button('Copy to Clipboard', key=f"copy_{i}"):
                        st.code(post_text)
                        st.success(f'{p.title} post copied to clipboard!')
                    
                    # Calculate and display API cost
                    total_price, input_tokens, input_price, output_tokens, output_price, total_tokens = calculate_api_price(message)
                    
                    st.sidebar.markdown(f"<h3>API Cost:</h3>", unsafe_allow_html=True)
                    st.sidebar.text(f"Total Cost: ${total_price:.2f}")
                    
                else:
                    st.warning('Please enter both the API key and content.')

if __name__ == '__main__':
    main()