import streamlit as st
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

sys.path.append(os.path.dirname(__file__))

from src.agents.orchestrator import Orchestrator
from src.memory.store import MemoryStore

st.set_page_config(
    page_title="NestWell Living",
    page_icon="🛋️",
    layout="wide"
)

# Room & Board inspired styling with more aggressive CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@300;400;600&display=swap');

    /* Global background and layout */
    .stApp {
        background: linear-gradient(135deg, #f8f6f3 0%, #ffffff 100%);
    }

    .main .block-container {
        padding-top: 1rem;
        max-width: 1000px;
        background: white;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin: 2rem auto;
        padding: 2rem 3rem;
    }

    /* Header styling */
    h1 {
        font-family: 'Source Sans Pro', sans-serif !important;
        font-weight: 300 !important;
        font-size: 3rem !important;
        color: #2c2c2c !important;
        text-align: center !important;
        margin-bottom: 0.5rem !important;
        letter-spacing: -1px !important;
    }

    .main .block-container > div:first-child > div:first-child > div:nth-child(2) p {
        text-align: center !important;
        font-size: 1.2rem !important;
        color: #8b7355 !important;
        font-style: normal !important;
        font-weight: 400 !important;
        margin-bottom: 3rem !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
    }

    /* Sidebar styling */
    .css-1d391kg {
        background: #f5f3f0 !important;
        padding: 2rem 1.5rem !important;
    }

    .sidebar .stMarkdown h2 {
        color: #2c2c2c !important;
        font-family: 'Source Sans Pro', sans-serif !important;
        font-size: 1.3rem !important;
        font-weight: 400 !important;
        margin-bottom: 1.5rem !important;
        border-bottom: 2px solid #d4c4a8 !important;
        padding-bottom: 0.5rem !important;
    }

    .sidebar .stMarkdown p {
        font-size: 0.95rem !important;
        line-height: 1.6 !important;
        color: #5a5a5a !important;
        margin-bottom: 0.8rem !important;
    }

    .sidebar .stMarkdown strong {
        color: #8b7355 !important;
        font-weight: 600 !important;
        display: block !important;
        margin-top: 1.5rem !important;
        margin-bottom: 0.5rem !important;
    }

    /* Chat input styling */
    .stChatFloatingInputContainer {
        background: white !important;
        border: 2px solid #d4c4a8 !important;
        border-radius: 25px !important;
        box-shadow: 0 2px 10px rgba(139, 115, 85, 0.1) !important;
    }

    .stChatInput input {
        background: transparent !important;
        border: none !important;
        font-size: 1rem !important;
        padding: 1rem 1.5rem !important;
        color: #2c2c2c !important;
    }

    .stChatInput input::placeholder {
        color: #8b7355 !important;
        font-style: italic !important;
    }

    /* Chat messages */
    .stChatMessage {
        background: #fafafa !important;
        border-radius: 12px !important;
        margin: 1rem 0 !important;
        padding: 1.5rem !important;
        border-left: 4px solid #d4c4a8 !important;
    }

    .stChatMessage[data-testid="user"] {
        background: linear-gradient(135deg, #f0ede8, #faf8f5) !important;
        border-left-color: #8b7355 !important;
    }

    .stChatMessage[data-testid="assistant"] {
        background: linear-gradient(135deg, #f8f6f3, #ffffff) !important;
        border-left-color: #2c2c2c !important;
    }

    /* Buttons */
    .stButton button {
        background: #8b7355 !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 500 !important;
        letter-spacing: 0.5px !important;
        text-transform: uppercase !important;
        font-size: 0.9rem !important;
        transition: all 0.2s ease !important;
    }

    .stButton button:hover {
        background: #6b5a42 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(139, 115, 85, 0.3) !important;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar settings
st.sidebar.header("Settings")
use_graph = st.sidebar.checkbox("Use LangGraph Planner", True)
persona = st.sidebar.selectbox("Persona", ["B2C (Jamie)", "B2B (Alex)"])
user_id = "demo_b2c" if "B2C" in persona else "demo_b2b"

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []

# Display hero image
st.image("https://images.unsplash.com/photo-1586023492125-27b2c045efd7?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&h=400&q=80", use_container_width=True)

# Initialize memory store (needed for both display and message handling)
mem = MemoryStore()

# Memory and profile sidebar - render after user_id is set
if user_id:
    prof = mem.get_profile(user_id)
    traits = prof.get("traits", {})
    hist = prof.get("history", [])

    # Main Profile section - collapsible, expanded if there's any data
    has_data = bool(traits) or bool(hist)
    with st.sidebar.expander(f"👤 User Profile & Memory", expanded=has_data):
        # Basic profile info
        st.markdown("**Basic Info**")
        st.markdown(f"• **User ID:** `{user_id}`")
        st.markdown(f"• **Persona:** {persona}")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Refresh", key="refresh_profile", help="Refresh the display"):
                st.rerun()
        with col2:
            if st.button("🗑️ Clear All", key="clear_profile", help="Clear profile data and chat messages"):
                # Clear the user's profile data
                mem.clear_profile(user_id)
                # Clear the chat history displayed on screen
                st.session_state.history = []
                st.success(f"Cleared profile and chat history for {user_id}")
                st.rerun()

        st.markdown("---")

        # Traits sub-section - collapsible
        with st.expander(f"🏷️ Traits ({len(traits)} recorded)", expanded=bool(traits)):
            if traits:
                for key, value in traits.items():
                    st.markdown(f"• **{key.title()}:** {value}")
            else:
                st.markdown("• _No traits recorded yet_")

        # Recent History sub-section - collapsible
        with st.expander(f"📝 Recent History ({len(hist)} events)", expanded=bool(hist)):
            if hist:
                # Show last 3 interactions
                for i, event in enumerate(hist[-3:]):
                    event_num = len(hist) - len(hist[-3:]) + i + 1
                    st.markdown(f"**Event {event_num}:** {event.get('stage', 'unknown').title()}")
                    if 'tools' in event:
                        st.markdown(f"  - Tools: {', '.join(event['tools'])}")
                    if 'bundle' in event:
                        st.markdown(f"  - Bundle: {len(event['bundle'])} items")
                    if 'quote' in event:
                        st.markdown(f"  - Quote: ${event['quote']['total']:,.2f}")
                    if i < len(hist[-3:]) - 1:  # Don't show separator after last item
                        st.markdown("")
            else:
                st.markdown("• _No history yet_")

# Initialize orchestrator
orc = Orchestrator(use_graph=use_graph)

# Header section
st.markdown("<h1 style='text-align: center; font-size: 3.5rem; color: #2c2c2c; margin: 2rem 0 0.5rem 0;'>🛋️ NestWell Living</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2rem; color: #8b7355; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 3rem;'>AI-optimized customer experiences</p>", unsafe_allow_html=True)

# Category icons in columns
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("<div style='text-align: center;'><div style='font-size: 2.5rem;'>🪑</div><div style='font-size: 0.9rem; color: #6b5a42; font-weight: 500;'>Seating</div></div>", unsafe_allow_html=True)
with col2:
    st.markdown("<div style='text-align: center;'><div style='font-size: 2.5rem;'>🛏️</div><div style='font-size: 0.9rem; color: #6b5a42; font-weight: 500;'>Bedroom</div></div>", unsafe_allow_html=True)
with col3:
    st.markdown("<div style='text-align: center;'><div style='font-size: 2.5rem;'>🪞</div><div style='font-size: 0.9rem; color: #6b5a42; font-weight: 500;'>Decor</div></div>", unsafe_allow_html=True)
with col4:
    st.markdown("<div style='text-align: center;'><div style='font-size: 2.5rem;'>💡</div><div style='font-size: 0.9rem; color: #6b5a42; font-weight: 500;'>Lighting</div></div>", unsafe_allow_html=True)

st.markdown("<hr style='margin: 3rem 0; border: none; height: 1px; background: #d4c4a8;'>", unsafe_allow_html=True)

# Example messages section
st.markdown("### Try messages like:")
st.code(
    "I'm outfitting a team lounge. What bundle do you recommend?\n"
    "We need a quote for 10 units by end of quarter. What's the price?\n"
    "My order is delayed, I might cancel."
)

# Message input and send functionality
msg = st.text_input("Your message", placeholder="Tell us how we can help with your home...")
if st.button("Send", type="primary") and msg:
    with st.spinner("Processing your message..."):
        reply, tags, trace = orc.handle_message(user_id, msg)

        # Add to chat history with improved formatting
        st.session_state.history.append(("You", msg))

        # Format the agent response with clean metadata
        formatted_reply = reply
        if tags or trace:
            metadata_parts = []
            if tags:
                metadata_parts.append(f"**Tags:** {', '.join(tags)}")
            if trace:
                metadata_parts.append(f"**Trace:** `{trace[:8]}...`")

            formatted_reply += f"\n\n---\n<small>{' | '.join(metadata_parts)}</small>"

        st.session_state.history.append(("Agent", formatted_reply))

        # Force a rerun to refresh the memory panel
        st.rerun()

st.divider()

# Display chat history
for role, text in st.session_state.history[-12:]:
    if role == "You":
        st.chat_message("user").markdown(text)
    else:
        st.chat_message("assistant").markdown(text)

# Add helpful sidebar content
st.sidebar.markdown("---")
st.sidebar.markdown("## How can we help?")

st.sidebar.markdown("🎨 **Design consultation**")
st.sidebar.markdown("• 'I need furniture for my living room'")
st.sidebar.markdown("• 'Can you recommend pieces for my home office?'")
st.sidebar.markdown("")

st.sidebar.markdown("💰 **Product & pricing**")
st.sidebar.markdown("• 'What's the price for 5 dining chairs?'")
st.sidebar.markdown("• 'I need a quote for bedroom furniture'")
st.sidebar.markdown("")

st.sidebar.markdown("📦 **Order assistance**")
st.sidebar.markdown("• 'My order status shows delayed'")
st.sidebar.markdown("• 'I need help with a return'")
st.sidebar.markdown("")

st.sidebar.markdown("ℹ️ **Product information**")
st.sidebar.markdown("• 'Tell me about your warranty'")
st.sidebar.markdown("• 'How do I care for leather furniture?'")

st.sidebar.markdown("---")
if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.history = []
    st.rerun()

st.caption("This demo persists memory across touchpoints. Traits and history update as you move through Marketing → Sales → CS.")