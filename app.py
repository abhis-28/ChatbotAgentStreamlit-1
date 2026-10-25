import streamlit as st
from langchain_groq import ChatGroq

st.set_page_config(page_title='My AI Persona Chat', layout='centered')

st.title("🤖 The Persona Chatbot")
st.write("An AI assistant with custom system prompt configuration.")

# The Sidebar (API Key & Persona Configuration)
with st.sidebar:
    st.header("⚙️ Configuration")
    user_api_key = st.text_input('Enter the Groq API Key:', type='password')
    
    # System Prompt Injector input box
    system_prompt = st.text_area(
        "Define AI Persona / System Prompt:",
        value="You are a helpful assistant. Answer concisely and clearly.",
        height=100
    )
    # 1. Add the reset button in the sidebar
    if st.button("Reset Chat & Apply Persona"):
        # 2. Clear the vault / message history
        st.session_state.messages = []
        st.success("Chat reset! New persona applied.")
        st.rerun()
    st.info('Your key is required to wake up the AI Brain')


# ------ 2. The Memory Vault -------
if 'messages' not in st.session_state:
    st.session_state.messages = []

# ----- 3. Display History ---------
# Display only user and assistant messages in the chat interface
for msg in st.session_state.messages:
    with st.chat_message(msg['role']):
        st.markdown(msg['content'])

# 4. Chat Input and Logic
if user_query := st.chat_input('Say something to the AI...'):
    if not user_api_key:
        st.error('Please enter your api key in the sidebar first!')
    else:
        # Display the user message instantly
        with st.chat_message('user'):
            st.markdown(user_query)

        # Store the user message to the vault
        st.session_state.messages.append({'role': 'user', 'content': user_query})

        # Initialise the Brain
        llm = ChatGroq(
            model='openai/gpt-oss-20b',
            temperature=0.7,
            api_key=user_api_key
        )

        with st.spinner('AI is thinking....'):
            # THE LOGIC PUZZLE SOLUTION:
            # Prepend the system prompt right before invoking the LLM so it is always 
            # the first message in the payload, without cluttering the chat vault UI.
            full_payload = [{'role': 'system', 'content': system_prompt}] + st.session_state.messages
            
            response = llm.invoke(full_payload)
            bot_answer = response.content

        st.session_state.messages.append({'role': 'assistant', 'content': bot_answer})
        with st.chat_message('assistant'):
            st.markdown(bot_answer)
