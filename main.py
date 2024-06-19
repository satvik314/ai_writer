import streamlit as st
import anthropic
from utils import calculate_api_price
# Load samples from the 'linkedin_posts.txt' file
with open('linkedin_posts.txt', 'r') as file:
    samples = file.read()

# Streamlit app
def main():
    st.set_page_config(page_title='LinkedIn Post Generator', page_icon=':memo:', layout='wide')
    
    st.markdown("<h1 style='text-align: center;'>LinkedIn Post Generator</h1>", unsafe_allow_html=True)

    # Get the API key from the user
    api_key = st.secrets['ANTHROPIC_API_KEY']

    # Initialize session state variable for content
    if 'content' not in st.session_state:
        st.session_state.content = ''

    # Get the content input from the user
    st.session_state.content = st.text_area('Enter the content to convert into a LinkedIn post:', value=st.session_state.content, height=200)

    if st.button('Generate LinkedIn Post'):
        if api_key and st.session_state.content:
            client = anthropic.Anthropic(api_key=api_key)
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
                                "text": f"Convert the below content into a LinkedIn post in my writing style.\n\n{st.session_state.content}\n\n\nHere are my some of my previous LinkedIn posts:\n\n{samples}\n\n\n\n\n"
                            }
                        ]
                    }
                ]
            )
            st.success('LinkedIn Post Generated!')
            
            # Extract plain text from the API response and display it in a scrollable text area
            post_text = message.content[0].text
            st.text_area('Generated LinkedIn Post:', value=post_text, height=400)
            
            # Add a button to copy the generated post to clipboard
            if st.button('Copy to Clipboard'):
                st.code(post_text)
                st.success('LinkedIn post copied to clipboard!')
            
            # Calculate and display the API cost
            total_price, input_tokens, input_price, output_tokens, output_price, total_tokens = calculate_api_price(message)
            
            st.markdown(f"<h3>API Cost Breakdown:</h3>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            col1.metric("Input Tokens", input_tokens)
            col2.metric("Output Tokens", output_tokens)
            col3.metric("Total Tokens", total_tokens)
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Input Cost", f"${input_price:.2f}")
            col2.metric("Output Cost", f"${output_price:.2f}")
            col3.metric("Total Cost", f"${total_price:.2f}")
        else:
            st.warning('Please enter both the API key and content.')

if __name__ == '__main__':
    main()