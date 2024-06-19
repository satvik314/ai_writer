import streamlit as st
import anthropic

# Load samples from the 'linkedin_posts.txt' file
with open('linkedin_posts.txt', 'r') as file:
    samples = file.read()

# Streamlit app
def main():
    st.title('LinkedIn Post Generator')

    # Get the API key from the user
    api_key = st.secrets['ANTHROPIC_API_KEY']

    # Get the content input from the user
    content = st.text_area('Enter the content to convert into a LinkedIn post:', height=200)

    if st.button('Generate LinkedIn Post'):
        if api_key and content:
            client = anthropic.Anthropic(api_key=api_key)
            message = client.messages.create(
                model="claude-3-sonnet",
                max_tokens=1000,
                temperature=0,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"Convert the below content into a LinkedIn post in my writing style.\n\n{content}\n\n\nHere are my some of my previous LinkedIn posts:\n\n{samples}\n\n\n\n\n"
                            }
                        ]
                    }
                ]
            )
            st.success('LinkedIn Post Generated!')
            
            # Extract plain text from the API response and display it in a scrollable text area
            post_text = message.content.split('text="')[1].split('"}')[0].replace('\\n\\n', '\n\n')
            st.text_area('Generated LinkedIn Post:', value=post_text, height=400)
            
            # Add a button to copy the generated post to clipboard
            if st.button('Copy to Clipboard'):
                st.code(post_text)
                st.success('LinkedIn post copied to clipboard!')
        else:
            st.warning('Please enter both the API key and content.')

if __name__ == '__main__':
    main()
