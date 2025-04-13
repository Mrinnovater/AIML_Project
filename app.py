import streamlit as st
import json
import random
import time

# Load the dataset
try:
    with open("SRU_DATASET.json", "r", encoding="utf-8") as file:
        data = json.load(file)
except FileNotFoundError:
    st.error("Error: SRU_DATASET.json file not found.")
    data = {"intents": []}

# Function to calculate similarity between user input and patterns
def similar(a, b):
    # Normalize strings: lowercase and remove extra spaces
    a, b = a.lower().strip(), b.lower().strip()
    # Exact or near-exact match gets higher score
    if a == b:
        return 1.0
    # Split into words and compute Jaccard similarity
    words_a, words_b = set(a.split()), set(b.split())
    intersection = len(words_a & words_b)
    union = len(words_a | words_b)
    return intersection / union if union > 0 else 0.0

# Function to get bot response based on query
def get_bot_response(user_input):
    user_input = user_input.lower().strip()
    best_match = None
    best_score = 0.0
    best_pattern = None

    # Loop through all intents and find the best match
    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            score = similar(user_input, pattern.lower())
            if score > best_score:
                best_score = score
                best_match = intent
                best_pattern = pattern

    # If the score is high enough, return a response from the best matching intent
    if best_score > 0.3:  # Lowered threshold to improve matching
        response = random.choice(best_match["responses"])
        # Debug: Log the matched intent and pattern
        st.write(f"Debug: Matched intent '{best_match['tag']}' with pattern '{best_pattern}' (score: {best_score:.2f})")
        return response
    return "I'm sorry, I didn't quite understand that. Could you please clarify?"

# Streamlit interface
st.set_page_config(page_title="SRU Chatbot", page_icon="🤖", layout="centered")

# Title and description
st.title("SRU Chatbot 🤖")
st.subheader("Ask your queries 💬 and get responses from the bot!")

# Initialize session state for messages
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Function to render chat bubbles for user and bot messages
def chat_bubble(message, role):
    if role == "user":
        st.markdown(
            f"""
            <div style='background-color:#1976D2; color:white; padding:10px 15px; border-radius:10px; margin:5px 0; text-align:right; max-width:70%; float:right; clear:both;'>
                <b>You:</b> {message}
            </div>
            """, unsafe_allow_html=True)
    else:
        # Render bot message with explicit Markdown processing
        st.markdown(
            f"""
            <div style='background-color:#F0F0F0; color:#222; padding:10px 15px; border-radius:10px; margin:5px 0; text-align:left; max-width:70%; float:left; clear:both;'>
                <b>Bot:</b> <span>{message}</span>
            </div>
            """, unsafe_allow_html=True)
        # Render the message again as pure Markdown to ensure links are clickable
        st.markdown(message, unsafe_allow_html=False)

# User input form
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your query here:👇")
    submit_button = st.form_submit_button("Send")

# Process user input
if submit_button and user_input:
    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Simulate bot thinking
    with st.spinner("Bot is thinking..."):
        time.sleep(1)  # Simulate delay
        bot_response = get_bot_response(user_input)

    # Save bot response
    st.session_state.messages.append({"role": "bot", "content": bot_response})

# Display chat history (after processing)
# Reverse the order to show the latest message at the top
for message in reversed(st.session_state.messages):
    chat_bubble(message["content"], message["role"])