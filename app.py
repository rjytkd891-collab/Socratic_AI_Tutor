
# ============================================================
# SOCRATIC AI TUTOR — THE LITTLE THINKING GARDEN
# ============================================================

from pathlib import Path
import streamlit as st
from socratic_engine import SocraticEngine


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Socratic AI Tutor",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# 2. SESSION STATE
# ============================================================

DEFAULTS = {
    "messages": [],
    "draft_question": "",
    "draft_version": 0,
    "editing_suggestion": False,
    "show_project": False,
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# 3. INITIALIZE SOCRATIC ENGINE
# ============================================================

@st.cache_resource
def get_engine():
    return SocraticEngine()


try:
    engine = get_engine()
    engine_error = None
except Exception as exc:
    engine = None
    engine_error = str(exc)


# ============================================================
# 4. DESIGN SYSTEM — SAGE GREEN & CREAM
# ============================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700&family=Lora:wght@500;600;700&display=swap');

    :root {
        --sage: #82977B;
        --sage-dark: #52684F;
        --sage-light: #E7EDE2;
        --cream: #F8F6EF;
        --cream-dark: #EEEBDD;
        --ink: #29372D;
        --muted: #687267;
        --border: #DCE2D5;
    }

    html, body, [class*="css"] {
        font-family: 'Be Vietnam Pro', sans-serif;
        color: var(--ink);
    }

    .stApp {
        background: var(--cream);
    }

    h1, h2, h3 {
        font-family: 'Lora', serif !important;
        color: var(--ink);
    }

    [data-testid="stSidebar"] {
        background: #EDF0E7;
        border-right: 1px solid var(--border);
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1.5rem;
    }

    [data-testid="stSidebar"] .stButton > button {
        width: 100%;
        text-align: left;
        border: 1px solid #DCE2D5;
        border-radius: 14px;
        background: rgba(255,255,255,0.68);
        color: var(--ink);
        min-height: 43px;
        transition: all 0.2s ease;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        border-color: var(--sage);
        background: #FFFFFF;
        color: var(--sage-dark);
    }

    .garden-header {
        padding: 1.3rem 1.5rem;
        border-radius: 22px;
        background: linear-gradient(120deg, #E8EEE2, #F6F2E6);
        border: 1px solid var(--border);
        margin-bottom: 1.1rem;
    }

    .garden-eyebrow {
        color: var(--sage-dark);
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        margin-bottom: 0.45rem;
    }

    .garden-title {
        font-family: 'Lora', serif;
        font-size: clamp(1.6rem, 3vw, 2.35rem);
        font-weight: 700;
        line-height: 1.3;
        color: #304332;
        margin: 0;
    }

    .garden-subtitle {
        color: #586658;
        font-size: 0.95rem;
        margin-top: 0.55rem;
        line-height: 1.7;
    }

    .welcome-card {
        background: #FFFFFF;
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 1.35rem 1.5rem;
        margin: 0.8rem 0 1rem 0;
        box-shadow: 0 3px 14px rgba(53, 72, 48, 0.035);
    }

    .welcome-title {
        font-family: 'Lora', serif;
        font-size: 1.45rem;
        font-weight: 700;
        color: #304332;
        margin-bottom: 0.5rem;
    }

    .welcome-text {
        color: #59665A;
        font-size: 0.95rem;
        line-height: 1.8;
    }

    .mascot-title {
        font-family: 'Lora', serif;
        font-size: 1.45rem;
        font-weight: 700;
        text-align: center;
        color: #304332;
        margin-top: 0.65rem;
    }

    .mascot-subtitle {
        text-align: center;
        color: var(--muted);
        font-size: 0.88rem;
        margin-top: 0.15rem;
        margin-bottom: 1rem;
    }

    [data-testid="stChatMessage"] {
        background: #FFFFFF;
        border: 1px solid #E1E5DC;
        border-radius: 18px;
        padding: 1rem;
        margin-bottom: 0.8rem;
    }

    [data-testid="stChatMessage"] p {
        line-height: 1.8;
        font-size: 0.96rem;
    }

    [data-testid="stChatInput"] {
        border-color: #CAD5C4;
        border-radius: 18px;
    }

    [data-testid="stChatInput"]:focus-within {
        border-color: var(--sage);
        box-shadow: 0 0 0 1px var(--sage);
    }

    .stButton > button {
        border-radius: 13px;
        min-height: 42px;
    }

    div[data-testid="stExpander"] {
        border: 1px solid var(--border);
        border-radius: 15px;
        background: rgba(255,255,255,0.55);
    }

    [data-testid="stCaptionContainer"] {
        color: #687267;
    }

    @media (max-width: 768px) {
        .garden-header {
            padding: 1rem;
            border-radius: 17px;
        }

        .welcome-card {
            padding: 1rem;
        }

        .garden-subtitle,
        .welcome-text {
            font-size: 0.9rem;
        }

        [data-testid="stChatMessage"] {
            padding: 0.75rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 5. SIDEBAR — MASCOT AND NAVIGATION
# ============================================================

with st.sidebar:

    mascot_path = (
        Path(__file__).parent
        / "assets"
        / "mascotsidebar.png"
    )

    # Center the mascot in the sidebar.
    if mascot_path.is_file():
        _, center, _ = st.columns([1, 3, 1])

        with center:
            st.image(
                str(mascot_path),
                width=170,
            )
    else:
        st.markdown(
            '<div style="font-size:48px; text-align:center;">🐱</div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="mascot-title">Socratic AI Tutor</div>
        <div class="mascot-subtitle">Gia sư gợi mở 🌱</div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    if st.button("💬  Trò chuyện", use_container_width=True):
        st.session_state.editing_suggestion = False
        st.session_state.draft_question = ""
        st.rerun()

    if st.button("📖  Về dự án", use_container_width=True):
        st.session_state.show_project = (
            not st.session_state.show_project
        )
        st.rerun()

    if st.button("＋  Cuộc trò chuyện mới", use_container_width=True):
        st.session_state.messages = []
        st.session_state.draft_question = ""
        st.session_state.editing_suggestion = False
        st.session_state.draft_version += 1
        st.session_state.show_project = False
        st.rerun()

    if st.session_state.show_project:
        st.markdown("### 🌱 Về dự án")
        st.write(
            "Socratic AI Tutor là gia sư AI gợi mở, "
            "hướng dẫn học sinh tự suy nghĩ, đặt câu hỏi "
            "và xây dựng câu trả lời của riêng mình."
        )
        st.caption(
            "Mục tiêu: phát triển năng lực tự học "
            "và tư duy phản biện."
        )

    st.divider()
    st.markdown("### 🕰️ Lịch sử gần đây")

    user_questions = [
        message["content"]
        for message in st.session_state.messages
        if message["role"] == "user"
    ]

    if user_questions:
        for question in reversed(user_questions[-5:]):
            short_question = (
                question[:42] + "..."
                if len(question) > 42
                else question
            )
            st.caption("💬 " + short_question)
    else:
        st.caption("Những câu hỏi của cậu sẽ xuất hiện ở đây.")

    st.divider()
    st.caption("Một câu hỏi tốt có thể mở ra nhiều cách nghĩ.")


# ============================================================
# 6. MAIN HEADER
# ============================================================

st.markdown(
    """
    <div class="garden-header">
        <div class="garden-title">Socratic AI Tutor 🌱</div>
        <div class="garden-subtitle">
            Không vội đưa đáp án — cùng cậu nuôi dưỡng
            những câu hỏi và tìm ra lời giải bằng chính tư duy của mình.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 7. FIVE SOCRATIC LEVELS
# ============================================================

with st.expander(
    "🔍 Xem 5 cấp độ câu hỏi Socratic của Trợ lý",
    expanded=False,
):
    levels = [
        (
            "01 · Làm rõ vấn đề",
            "Giúp cậu xác định điều đang được hỏi, "
            "khái niệm và ý nghĩa của vấn đề.",
        ),
        (
            "02 · Khám phá giả định",
            "Nhận diện những điều đang được mặc định "
            "là đúng và xem xét chúng.",
        ),
        (
            "03 · Phân tích bằng chứng",
            "Tìm căn cứ, dữ kiện và lý do hỗ trợ "
            "cho một nhận định.",
        ),
        (
            "04 · Góc nhìn đa chiều",
            "Xem xét vấn đề từ những góc nhìn "
            "và lập luận khác nhau.",
        ),
        (
            "05 · Đánh giá hệ quả",
            "Kết nối các ý tưởng, đánh giá hệ quả "
            "và tự tổng hợp kết luận.",
        ),
    ]

    for title, description in levels:
        st.markdown(f"**{title}**")
        st.write(description)


# ============================================================
# 8. PROJECT VIEW
# ============================================================

if st.session_state.show_project:
    st.markdown(
        """
        <div class="welcome-card">
            <div class="welcome-title">🌿 Một khu vườn của tư duy</div>
            <div class="welcome-text">
                Socratic AI Tutor được xây dựng để hỗ trợ học sinh
                chủ động học tập thông qua câu hỏi gợi mở.
                Thay vì làm bài thay người học, trợ lý khuyến khích
                cậu giải thích suy nghĩ, xem xét bằng chứng,
                nhận ra giả định và tự xây dựng kết luận.
                <br><br>
                Mỗi cuộc trò chuyện là một cơ hội để luyện tập
                khả năng tự học và tư duy phản biện.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# 9. WELCOME CARD
# ============================================================

if not st.session_state.messages and not st.session_state.show_project:
    st.markdown(
        """
        <div class="welcome-card">
            <div class="welcome-title">Chào cậu! 🌱</div>
            <div class="welcome-text">
                Cậu đang muốn tìm hiểu điều gì hôm nay?
                <br>
                Hãy bắt đầu bằng một câu hỏi, một ý tưởng
                hoặc điều cậu đang cảm thấy khó hiểu.
                Tớ sẽ cùng cậu suy nghĩ từng bước.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# 10. CHAT HISTORY
# ============================================================

for message in st.session_state.messages:
    role = message["role"]
    avatar = "🌱" if role == "assistant" else "🧑‍🎓"

    with st.chat_message(role, avatar=avatar):
        st.markdown(message["content"])


# ============================================================
# 11. QUESTION SUGGESTIONS
# ============================================================

with st.expander("💡 Gợi ý câu hỏi để bắt đầu", expanded=False):
    suggestions = [
        "Giúp mình phân tích một tác phẩm văn học "
        "mà không viết bài thay mình.",

        "Làm thế nào để nhận biết một lập luận "
        "có bằng chứng thuyết phục?",

        "Mình chưa hiểu bài học hôm nay. "
        "Hãy giúp mình tìm ra phần chưa hiểu.",

        "Hãy giúp mình nhìn một vấn đề "
        "từ nhiều góc độ khác nhau.",
    ]

    for index, suggestion in enumerate(suggestions):
        if st.button(
            suggestion,
            key=f"suggestion_{index}",
            use_container_width=True,
        ):
            st.session_state.draft_question = suggestion
            st.session_state.editing_suggestion = True
            st.session_state.draft_version += 1
            st.rerun()


# ============================================================
# 12. INPUT — EDITABLE SUGGESTION OR NORMAL CHAT
# ============================================================

question = None

if (
    st.session_state.editing_suggestion
    and not st.session_state.show_project
):
    st.markdown("#### ✏️ Chỉnh sửa câu hỏi của cậu")

    with st.form(
        key=f"suggestion_form_{st.session_state.draft_version}"
    ):
        edited_question = st.text_area(
            "Cậu có thể sửa câu hỏi trước khi gửi:",
            value=st.session_state.draft_question,
            height=110,
            placeholder="Nhập câu hỏi của cậu...",
        )

        col_send, col_cancel = st.columns(2)

        with col_send:
            submitted = st.form_submit_button(
                "🌱 Gửi câu hỏi",
                use_container_width=True,
            )

        with col_cancel:
            cancelled = st.form_submit_button(
                "Hủy",
                use_container_width=True,
            )

    if cancelled:
        st.session_state.editing_suggestion = False
        st.session_state.draft_question = ""
        st.rerun()

    if submitted:
        if edited_question.strip():
            question = edited_question.strip()
            st.session_state.editing_suggestion = False
            st.session_state.draft_question = ""
        else:
            st.warning("Cậu nhập câu hỏi trước khi gửi nha.")

elif not st.session_state.show_project:
    question = st.chat_input(
        "Nhập câu hỏi hoặc điều cậu đang băn khoăn...",
        key="chat_input",
    )


# ============================================================
# 13. GENERATE SOCRATIC RESPONSE
# ============================================================

if question:
    if engine is None:
        st.error(
            "Trợ lý chưa khởi tạo được. "
            "Cậu kiểm tra cấu hình API và khởi động lại ứng dụng nhé."
        )
        if engine_error:
            st.caption(f"Chi tiết lỗi: {engine_error}")

    else:
        st.session_state.messages.append(
            {
                "role": "user",
                "content": question,
            }
        )

        with st.chat_message("user", avatar="🧑‍🎓"):
            st.markdown(question)

        with st.chat_message("assistant", avatar="🌱"):
            response_placeholder = st.empty()
            full_response = ""

            try:
                history = st.session_state.messages[:-1]

                stream = engine.ask_stream(
                    question=question,
                    history=history,
                )

                for chunk in stream:
                    if chunk:
                        full_response += str(chunk)
                        response_placeholder.markdown(
                            full_response + " ▌"
                        )

                if full_response.strip():
                    response_placeholder.markdown(full_response)

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": full_response,
                        }
                    )
                else:
                    response_placeholder.warning(
                        "Trợ lý chưa tạo được phản hồi. "
                        "Cậu thử gửi lại câu hỏi nhé."
                    )

            except Exception as exc:
                error_text = str(exc)
                error_lower = error_text.lower()

                if (
                    "429" in error_text
                    or "quota" in error_lower
                    or "resource_exhausted" in error_lower
                ):
                    friendly_error = (
                        "API đang vượt giới hạn sử dụng hoặc hết quota. "
                        "Cậu kiểm tra hạn mức và thử lại sau nhé."
                    )

                elif (
                    "503" in error_text
                    or "unavailable" in error_lower
                ):
                    friendly_error = (
                        "Dịch vụ AI hiện đang bận. "
                        "Cậu đợi một chút rồi thử lại nha."
                    )

                elif (
                    "timeout" in error_lower
                    or "timed out" in error_lower
                ):
                    friendly_error = (
                        "Trợ lý phản hồi quá lâu. "
                        "Cậu thử lại với câu hỏi ngắn hơn nhé."
                    )

                else:
                    friendly_error = (
                        "Đã xảy ra lỗi khi xử lý câu hỏi. "
                        "Cậu kiểm tra kết nối và cấu hình API nhé."
                    )

                if full_response.strip():
                    response_placeholder.markdown(full_response)

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": full_response,
                        }
                    )

                st.error(friendly_error)
                st.caption(f"Chi tiết kỹ thuật: {error_text}")

