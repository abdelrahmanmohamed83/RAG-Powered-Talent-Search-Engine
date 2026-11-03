import streamlit as st

from agent import recruiter_agent


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Recruiter",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

    /* =========================
       GLOBAL
       ========================= */

    .stApp {
        background: #0b0f14;
        color: #e6e9ef;
    }

    .main .block-container {
        max-width: 1100px;
        padding-top: 2.2rem;
        padding-bottom: 7rem;
    }

    /* Remove default Streamlit chrome */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }


    /* =========================
       SIDEBAR
       ========================= */

    [data-testid="stSidebar"] {
        background: #0f141b;
        border-right: 1px solid #202732;
    }

    [data-testid="stSidebar"] .block-container {
        padding-top: 2rem;
    }

    .brand-title {
        font-size: 21px;
        font-weight: 700;
        color: #f3f5f8;
        letter-spacing: -0.3px;
    }

    .brand-subtitle {
        margin-top: 4px;
        color: #7f8998;
        font-size: 13px;
    }

    .sidebar-label {
        margin-top: 30px;
        margin-bottom: 10px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        color: #697384;
    }

    .sidebar-text {
        color: #929baa;
        font-size: 13px;
        line-height: 1.7;
    }


    /* =========================
       HEADER
       ========================= */

    .top-status {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 6px 11px;
        margin-bottom: 18px;

        background: #11171f;
        border: 1px solid #27303c;
        border-radius: 18px;

        color: #9ca5b3;
        font-size: 12px;
    }

    .status-dot {
        width: 6px;
        height: 6px;
        background: #45c78b;
        border-radius: 50%;
    }

    .page-title {
        margin: 0;
        color: #f4f6f8;
        font-size: 38px;
        font-weight: 750;
        letter-spacing: -1px;
        line-height: 1.1;
    }

    .page-subtitle {
        margin-top: 8px;
        margin-bottom: 28px;

        color: #8791a0;
        font-size: 15px;
        line-height: 1.6;
    }


    /* =========================
       CHAT AREA
       ========================= */

    [data-testid="stChatMessage"] {
        background: transparent !important;
        border: none !important;
        padding-top: 8px;
        padding-bottom: 8px;
    }

    [data-testid="stChatMessageContent"] {
        border-radius: 14px;
        padding: 14px 18px;
    }

    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-user"]
    ) [data-testid="stChatMessageContent"] {
        background: #171d26;
        border: 1px solid #252d38;
    }

    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-assistant"]
    ) [data-testid="stChatMessageContent"] {
        background: #10161e;
        border: 1px solid #202832;
    }


    /* =========================
       CHAT INPUT
       ========================= */

    [data-testid="stChatInput"] {
        border-top: none !important;
    }

    [data-testid="stChatInput"] > div {
        background: #10161e !important;
        border: 1px solid #29323f !important;
        border-radius: 14px !important;
        box-shadow: none !important;
    }

    [data-testid="stChatInput"] textarea {
        color: #f3f5f8 !important;
        background: transparent !important;
        font-size: 14px !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #6f7988 !important;
    }


    /* =========================
       BUTTONS
       ========================= */

    .stButton button {
        width: 100%;
        min-height: 42px;

        background: #141a22;
        border: 1px solid #29323e;
        border-radius: 9px;

        color: #dce1e8;
        font-size: 13px;
        font-weight: 500;
    }

    .stButton button:hover {
        background: #1a212b;
        border-color: #3b4655;
        color: #ffffff;
    }


    /* =========================
       DIVIDER
       ========================= */

    .section-divider {
        height: 1px;
        background: #202732;
        margin: 20px 0;
    }


    /* =========================
       EMPTY STATE
       ========================= */

    .empty-state {
        margin-top: 90px;
        text-align: center;
    }

    .empty-title {
        color: #e8ebef;
        font-size: 24px;
        font-weight: 650;
    }

    .empty-subtitle {
        margin-top: 8px;
        color: #788291;
        font-size: 14px;
    }


    /* =========================
       SPINNER
       ========================= */

    .stSpinner > div {
        border-top-color: #8a93a3 !important;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="brand-title">AI Recruiter</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="brand-subtitle">'
        'RAG-powered talent search'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-label">System</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-text">'
        'Semantic resume search<br>'
        'Candidate evaluation<br>'
        'Resume retrieval<br>'
        'Candidate comparison<br>'
        'Conversational reasoning'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-label">Data</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-text">'
        '536 unique candidates<br>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-label">Session</div>',
        unsafe_allow_html=True
    )

    if st.button("Clear conversation"):

        st.session_state.messages = []

        import agent

        agent.conversation_history.clear()
        agent.current_candidates.clear()

        st.rerun()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="top-status">
        <span class="status-dot"></span>
        Agent online
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '<div class="page-title">AI Talent Search</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="page-subtitle">'
    'Search, evaluate, and compare candidates using natural language.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# CHAT HISTORY
# ============================================================

if not st.session_state.messages:

    st.markdown(
        """
        <div class="empty-state">
            <div class="empty-title">
                Start a conversation
            </div>

            
                Describe the type of candidate you are looking for.
          
        </div>
        """,
        unsafe_allow_html=True
    )


for message in st.session_state.messages:

    role = message["role"]

    with st.chat_message(role):

        st.markdown(message["content"])


# ============================================================
# CHAT INPUT
# ============================================================

user_message = st.chat_input(
    "Search for candidates or ask about a candidate..."
)


if user_message:

    # -------------------------
    # User message
    # -------------------------

    st.session_state.messages.append({
        "role": "user",
        "content": user_message
    })

    with st.chat_message("user"):

        st.markdown(user_message)


    # -------------------------
    # Agent response
    # -------------------------

    with st.chat_message("assistant"):

        with st.spinner("Analyzing candidates..."):

            try:

                response = recruiter_agent(
                    user_message
                )

                st.markdown(response)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response
                })

            except Exception as e:

                error_message = (
                    "The assistant could not complete the request. "
                    f"Error: {str(e)}"
                )

                st.error(error_message)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_message
                })